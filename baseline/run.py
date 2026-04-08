"""
Baseline Inference Script for OpenEnv
Uses OpenAI API client to evaluate models within the environment
Credentials read from OPENAI_API_KEY environment variable
"""
import os
import json
from typing import Dict, Any
from env.environment import create_env


def get_openai_client():
    """Get OpenAI client"""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        print("Warning: OpenAI client not available, using rule-based baseline")
        return None


def _parse_openai_json(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(content[start:end + 1])
            except Exception:
                return {}
        return {}


def get_openai_action(client, task_id: str, obs: Dict[str, Any]) -> Dict[str, Any]:
    """Generate action using OpenAI API with deterministic decoding."""
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if task_id == "email_classification":
        schema_hint = (
            '{"classification":"important|spam|promotional","confidence":0.0}'
        )
    elif task_id == "code_review":
        schema_hint = (
            '{"issue_types":["security|style|logic|performance|none"],'
            '"severity":"critical|major|minor|none","priority":"high|medium|low"}'
        )
    else:
        schema_hint = (
            '{"department":"billing|tech_support|general_support|escalation",'
            '"priority":"low|medium|high|urgent","response_type":"auto_reply|human_review|escalate",'
            '"tone":"empathetic|formal|urgent|casual","estimated_resolution_time_hours":1}'
        )

    prompt = (
        "You are an environment agent. Return only valid JSON with no markdown. "
        f"Task: {task_id}. Observation: {json.dumps(obs)}. "
        f"Output schema example: {schema_hint}."
    )

    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return only compact JSON."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    return _parse_openai_json(content)


class RuleBasedBaseline:
    """Rule-based baseline for each task"""
    
    @staticmethod
    def email_classification(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based email classification"""
        email_body = obs.get("email_body", "").lower()
        subject = obs.get("email_subject", "").lower()
        
        # Check for promotional keywords
        promo_keywords = ["sale", "discount", "offer", "free", "save", "limited", "now", "today"]
        spam_keywords = ["click here", "claim", "prize", "won", "verify account", "confirm identity"]
        
        for keyword in spam_keywords:
            if keyword in email_body or keyword in subject:
                return {"classification": "spam", "confidence": 0.8}
        
        for keyword in promo_keywords:
            if keyword in email_body or keyword in subject:
                return {"classification": "promotional", "confidence": 0.7}
        
        return {"classification": "important", "confidence": 0.6}
    
    @staticmethod
    def code_review(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based code review"""
        code = obs.get("code_snippet", "").lower()
        
        issues = []
        severity = "none"
        
        # Security checks
        if "eval(" in code or "exec(" in code:
            issues.append("security")
            severity = "critical"
        elif "password" in code or "secret" in code:
            issues.append("security")
            severity = "critical"
        elif "select *" in code or "' + " in code:
            issues.append("security")
            severity = "critical"
        
        # Performance checks
        if "for " in code and code.count("for ") > 1:
            if "security" not in issues:
                issues.append("performance")
                severity = "major"
        
        # Style checks
        if "  =" in code or "= " not in code:
            if not issues:
                issues.append("style")
                severity = "minor"
        
        return {
            "issue_types": issues if issues else ["none"],
            "severity": severity,
            "priority": "high" if severity == "critical" else "medium"
        }
    
    @staticmethod
    def support_routing(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Simple rule-based support routing"""
        description = obs.get("ticket_description", "").lower()
        subject = obs.get("ticket_subject", "").lower()
        sentiment = obs.get("sentiment", "neutral")
        customer_type = obs.get("customer_type", "free")
        
        # Determine department
        if "pay" in description or "refund" in description or "charged" in description or "bill" in description:
            department = "billing"
        elif "crash" in description or "error" in description or "slow" in description or "login" in description:
            department = "tech_support"
        else:
            department = "general_support"
        
        # Determine priority
        is_vip = obs.get("is_vip", False)
        if is_vip or sentiment == "angry":
            priority = "urgent"
        elif sentiment == "frustrated":
            priority = "high"
        else:
            priority = "medium"
        
        # Determine response type
        if is_vip or priority == "urgent":
            response_type = "escalate"
        elif sentiment == "positive":
            response_type = "auto_reply"
        else:
            response_type = "human_review"
        
        # Determine tone
        if sentiment == "angry":
            tone = "empathetic"
        elif customer_type == "premium":
            tone = "formal"
        elif priority == "urgent":
            tone = "urgent"
        else:
            tone = "casual"
        
        return {
            "department": department,
            "priority": priority,
            "response_type": response_type,
            "tone": tone,
            "estimated_resolution_time_hours": 2 if priority == "urgent" else 24
        }


def run_baseline_inference(task_id: str = "support_routing", difficulty: str = "easy", num_episodes: int = 1) -> Dict[str, Any]:
    """
    Run baseline inference on a task
    
    Args:
        task_id: Task to evaluate (email_classification, code_review, support_routing)
        difficulty: Difficulty level (easy, medium, hard)
        num_episodes: Number of episodes to run
        
    Returns:
        dict with performance metrics
    """
    print(f"\n{'='*60}")
    print(f"Running baseline inference: {task_id} ({difficulty})")
    print(f"{'='*60}\n")
    
    client = get_openai_client()
    using_openai = client is not None

    results = {
        "task_id": task_id,
        "difficulty": difficulty,
        "num_episodes": num_episodes,
        "policy": "openai" if using_openai else "rule_based",
        "episodes": [],
        "total_reward": 0.0,
        "average_reward": 0.0,
        "average_steps": 0.0,
        "average_reward_per_step": 0.0,
    }
    
    for episode_num in range(num_episodes):
        env = create_env(task_id, difficulty)
        obs = env.reset()
        episode_reward = 0.0
        steps = 0
        
        print(f"Episode {episode_num + 1}/{num_episodes}")
        
        while True:
            if not obs:
                break
            
            # Get action from baseline
            if using_openai:
                try:
                    action = get_openai_action(client, task_id, obs)
                except Exception:
                    using_openai = False
                    print("  OpenAI call failed, falling back to rule-based policy.")

            if not using_openai:
                if task_id == "email_classification":
                    action = RuleBasedBaseline.email_classification(obs)
                elif task_id == "code_review":
                    action = RuleBasedBaseline.code_review(obs)
                elif task_id == "support_routing":
                    action = RuleBasedBaseline.support_routing(obs)
                else:
                    break
            
            # Take step
            next_obs, reward, done, info = env.step(action)
            episode_reward += reward
            steps += 1
            
            # Print step info
            if "grade" in info:
                grade = info["grade"]
                print(f"  Step {steps}: reward={reward:.2f}, {grade['reasoning'][:60]}...")
            
            obs = next_obs
            
            if done:
                break
        
        episode_data = {
            "episode": episode_num + 1,
            "total_steps": steps,
            "total_reward": episode_reward,
            "average_reward_per_step": episode_reward / steps if steps > 0 else 0.0
        }
        results["episodes"].append(episode_data)
        results["total_reward"] += episode_reward
        results["average_steps"] += steps
        
        print(f"  ✓ Episode complete: total_reward={episode_reward:.2f}, steps={steps}\n")
    
    results["average_reward"] = results["total_reward"] / num_episodes if num_episodes > 0 else 0.0
    results["average_steps"] = results["average_steps"] / num_episodes if num_episodes > 0 else 0.0
    results["average_reward_per_step"] = (
        results["average_reward"] / results["average_steps"] if results["average_steps"] > 0 else 0.0
    )
    
    return results


def run_all_tasks_baseline(num_episodes_per_task: int = 1) -> Dict[str, Any]:
    """
    Run baseline inference across all tasks
    
    Returns:
        dict with results for all tasks
    """
    all_results = {
        "timestamp": str(os.popen("date").read().strip()),
        "num_episodes": num_episodes_per_task,
        "tasks": {}
    }
    
    tasks = [
        ("email_classification", "easy"),
        ("code_review", "medium"),
        ("support_routing", "hard")
    ]
    
    for task_id, default_difficulty in tasks:
        # Run each difficulty level
        for difficulty in ["easy", "medium", "hard"]:
            key = f"{task_id}_{difficulty}"
            result = run_baseline_inference(task_id, difficulty, num_episodes_per_task)
            all_results["tasks"][key] = result
    
    # Print summary
    print(f"\n{'='*60}")
    print("BASELINE PERFORMANCE SUMMARY")
    print(f"{'='*60}\n")
    
    total_avg_reward = 0.0
    total_avg_reward_per_step = 0.0
    count = 0
    
    for task_key, result in all_results["tasks"].items():
        print(f"{task_key}:")
        print(f"  Average Reward: {result['average_reward']:.3f}")
        print(f"  Average Steps: {result['average_steps']:.1f}")
        print(f"  Average Reward/Step: {result['average_reward_per_step']:.3f}")
        print()
        
        total_avg_reward += result["average_reward"]
        total_avg_reward_per_step += result["average_reward_per_step"]
        count += 1
    
    overall_avg = total_avg_reward / count if count > 0 else 0.0
    overall_avg_per_step = total_avg_reward_per_step / count if count > 0 else 0.0
    all_results["overall_average_reward"] = overall_avg
    all_results["overall_average_reward_per_step"] = overall_avg_per_step
    
    print(f"Overall Average Reward: {overall_avg:.3f}\n")
    print(f"Overall Average Reward/Step: {overall_avg_per_step:.3f}\n")
    
    return all_results


def run_baseline():
    """Legacy function for backward compatibility"""
    return run_all_tasks_baseline(num_episodes_per_task=1)


if __name__ == "__main__":
    # Run baseline for all tasks
    results = run_all_tasks_baseline(num_episodes_per_task=2)
    print(json.dumps(results, indent=2))

