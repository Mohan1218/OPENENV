"""
OpenEnv Benchmark Inference Script
Evaluates agent performance on OpenEnv tasks using OpenAI API
Uses API_BASE_URL, MODEL_NAME, and HF_TOKEN environment variables
Outputs structured logs in [START], [STEP], [END] format
"""
import os
import json
import sys
from typing import Dict, Any, Optional
from datetime import datetime

# Initialize OpenAI client with proper environment variables
def get_openai_client():
    """Initialize OpenAI client with API_BASE_URL, MODEL_NAME, and HF_TOKEN"""
    try:
        from openai import OpenAI
        
        api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
        api_key = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("[ERROR] HF_TOKEN or OPENAI_API_KEY environment variable not set", file=sys.stderr)
            return None
        
        client = OpenAI(
            api_key=api_key,
            base_url=api_base if api_base != "https://api.openai.com/v1" else None
        )
        return client
    except ImportError:
        print("[ERROR] OpenAI package not installed", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[ERROR] Failed to initialize OpenAI client: {e}", file=sys.stderr)
        return None


def get_model_name() -> str:
    """Get model name from environment or use default"""
    return os.getenv("MODEL_NAME", "gpt-4o-mini")


def _parse_openai_json(content: str) -> Dict[str, Any]:
    """Parse JSON from OpenAI response with error handling"""
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
    """Generate action using OpenAI API with deterministic decoding"""
    model_name = get_model_name()
    
    if task_id == "email_classification":
        schema_hint = (
            '{"classification":"important|spam|promotional","confidence":0.0}'
        )
    elif task_id == "code_review":
        schema_hint = (
            '{"issue_types":["security|style|logic|performance|none"],'
            '"severity":"critical|major|minor|none","priority":"high|medium|low"}'
        )
    else:  # support_routing
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
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Return only compact JSON."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            timeout=30
        )
        content = response.choices[0].message.content or "{}"
        return _parse_openai_json(content)
    except Exception as e:
        print(f"[WARNING] OpenAI API call failed: {e}", file=sys.stderr)
        return {}


class RuleBasedBaseline:
    """Rule-based fallback baseline for each task"""
    
    @staticmethod
    def email_classification(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based email classification"""
        email_body = obs.get("email_body", "").lower()
        subject = obs.get("email_subject", "").lower()
        
        promo_keywords = ["sale", "discount", "offer", "free", "save", "limited"]
        spam_keywords = ["click here", "claim", "prize", "won", "verify"]
        
        for keyword in spam_keywords:
            if keyword in email_body or keyword in subject:
                return {"classification": "spam", "confidence": 0.8}
        
        for keyword in promo_keywords:
            if keyword in email_body or keyword in subject:
                return {"classification": "promotional", "confidence": 0.7}
        
        return {"classification": "important", "confidence": 0.6}
    
    @staticmethod
    def code_review(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based code review"""
        code = obs.get("code_snippet", "").lower()
        
        issues = []
        severity = "none"
        
        if "eval(" in code or "exec(" in code or "password" in code:
            issues.append("security")
            severity = "critical"
        elif "for " in code and code.count("for ") > 1:
            issues.append("performance")
            severity = "major"
        
        return {
            "issue_types": issues if issues else ["none"],
            "severity": severity,
            "priority": "high" if severity == "critical" else "medium"
        }
    
    @staticmethod
    def support_routing(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based support routing"""
        description = obs.get("ticket_description", "").lower()
        sentiment = obs.get("sentiment", "neutral")
        is_vip = obs.get("is_vip", False)
        
        if any(x in description for x in ["refund", "bill", "charge"]):
            department = "billing"
        elif any(x in description for x in ["error", "crash", "slow"]):
            department = "tech_support"
        else:
            department = "general_support"
        
        if is_vip or sentiment == "angry":
            priority = "urgent"
        else:
            priority = "medium"
        
        return {
            "department": department,
            "priority": priority,
            "response_type": "escalate" if is_vip else "human_review",
            "tone": "empathetic" if sentiment == "angry" else "casual",
            "estimated_resolution_time_hours": 2 if priority == "urgent" else 24
        }


def run_task_inference(task_id: str, difficulty: str, num_episodes: int = 1) -> Dict[str, Any]:
    """
    Run inference on a single task with structured logging
    
    [START] task_id=..., difficulty=..., num_episodes=...
    [STEP] episode=..., step=..., action=..., reward=...
    [END] task_id=..., difficulty=..., average_reward=..., average_reward_per_step=...
    """
    from env.environment import create_env
    
    # Print START marker
    print(f"[START] task_id={task_id}, difficulty={difficulty}, num_episodes={num_episodes}")
    sys.stdout.flush()
    
    client = get_openai_client()
    using_openai = client is not None
    
    results = {
        "task_id": task_id,
        "difficulty": difficulty,
        "num_episodes": num_episodes,
        "policy": "openai" if using_openai else "rule_based",
        "total_reward": 0.0,
        "total_steps": 0,
        "episodes": []
    }
    
    for episode_num in range(num_episodes):
        env = create_env(task_id, difficulty)
        obs = env.reset()
        episode_reward = 0.0
        steps = 0
        
        while obs:
            # Get action
            if using_openai:
                try:
                    action = get_openai_action(client, task_id, obs)
                except Exception:
                    using_openai = False
                    action = {}
            
            if not using_openai or not action:
                if task_id == "email_classification":
                    action = RuleBasedBaseline.email_classification(obs)
                elif task_id == "code_review":
                    action = RuleBasedBaseline.code_review(obs)
                elif task_id == "support_routing":
                    action = RuleBasedBaseline.support_routing(obs)
                else:
                    break
            
            # Take step
            try:
                next_obs, reward, done, info = env.step(action)
                episode_reward += reward
                steps += 1
                
                # Print STEP marker
                action_str = json.dumps(action).replace('"', "'")[:60]
                print(f"[STEP] episode={episode_num + 1}, step={steps}, reward={reward:.3f}, action={action_str}")
                sys.stdout.flush()
                
                obs = next_obs
                
                if done:
                    break
            except Exception as e:
                print(f"[ERROR] Step failed: {e}", file=sys.stderr)
                break
        
        episode_data = {
            "episode": episode_num + 1,
            "total_reward": episode_reward,
            "total_steps": steps
        }
        results["episodes"].append(episode_data)
        results["total_reward"] += episode_reward
        results["total_steps"] += steps
    
    # Calculate averages
    num_total_episodes = num_episodes
    avg_reward = results["total_reward"] / num_total_episodes if num_total_episodes > 0 else 0.0
    avg_reward_per_step = results["total_reward"] / results["total_steps"] if results["total_steps"] > 0 else 0.0
    
    results["average_reward"] = avg_reward
    results["average_reward_per_step"] = avg_reward_per_step
    
    # Print END marker
    print(f"[END] task_id={task_id}, difficulty={difficulty}, average_reward={avg_reward:.3f}, average_reward_per_step={avg_reward_per_step:.3f}")
    sys.stdout.flush()
    
    return results


def run_all_benchmarks(num_episodes: int = 1) -> Dict[str, Any]:
    """Run inference on all tasks and difficulties"""
    print(f"[INFO] Starting OpenEnv benchmark evaluation", file=sys.stderr)
    print(f"[INFO] Using model: {get_model_name()}", file=sys.stderr)
    print(f"[INFO] Using API base: {os.getenv('API_BASE_URL', 'https://api.openai.com/v1')}", file=sys.stderr)
    print()
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "model": get_model_name(),
        "num_episodes": num_episodes,
        "tasks": {}
    }
    
    # Run all task-difficulty combinations
    tasks = [
        "email_classification",
        "code_review",
        "support_routing"
    ]
    
    difficulties = ["easy", "medium", "hard"]
    
    for task_id in tasks:
        for difficulty in difficulties:
            key = f"{task_id}_{difficulty}"
            result = run_task_inference(task_id, difficulty, num_episodes)
            all_results["tasks"][key] = result
            print()
    
    # Summary statistics
    total_reward = sum(r["total_reward"] for r in all_results["tasks"].values())
    total_episodes = sum(r["num_episodes"] for r in all_results["tasks"].values())
    total_steps = sum(r["total_steps"] for r in all_results["tasks"].values())
    
    avg_reward_per_step = total_reward / total_steps if total_steps > 0 else 0.0
    
    all_results["summary"] = {
        "total_episodes": total_episodes,
        "total_steps": total_steps,
        "total_reward": total_reward,
        "average_reward_per_step": avg_reward_per_step
    }
    
    print(f"[INFO] Benchmark complete. Overall average reward/step: {avg_reward_per_step:.3f}", file=sys.stderr)
    
    return all_results


if __name__ == "__main__":
    try:
        num_episodes = int(os.getenv("NUM_EPISODES", "1"))
        results = run_all_benchmarks(num_episodes=num_episodes)
        
        # Output final results as JSON to stdout
        print("\n[JSON_RESULTS]")
        print(json.dumps(results, indent=2))
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Inference script failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
