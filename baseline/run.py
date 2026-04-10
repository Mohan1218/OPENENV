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
    """Smart rule-based baseline with domain-aware heuristics"""
    
    @staticmethod
    def email_classification(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Smart email classification with domain reputation and content analysis"""
        email_body = obs.get("email_body", "").lower()
        subject = obs.get("email_subject", "").lower()
        sender_domain = obs.get("sender_domain", "").lower()
        
        # SPAM DETECTION: High confidence spam indicators
        high_confidence_spam = [
            "claim prize", "won prize", "congratulations won", "click here immediately",
            "verify account", "confirm identity", "update payment", "suspended account",
            "unusual activity", "urgent action required", "act now", "limited offer",
            "too good to be true", "too good", "rare opportunity", "exclusive offer now"
        ]
        
        for spam_phrase in high_confidence_spam:
            if spam_phrase in email_body or spam_phrase in subject:
                return {"classification": "spam", "confidence": 0.95}
        
        # PHISHING DETECTION: Check for suspicious sender/link patterns
        phishing_indicators = [
            ("paypa1.com", "paypal phishing"),
            ("amaz0n.com", "amazon phishing"),
            ("microsft.com", "microsoft phishing"),
            ("your-bank.com", "bank phishing")
        ]
        
        for indicator, _ in phishing_indicators:
            if indicator in sender_domain:
                return {"classification": "spam", "confidence": 0.92}
        
        # Check for typo squatting
        if "click" in email_body and ("link" in email_body or "http" in email_body):
            if "@" in email_body or "[" in email_body:  # Suspicious patterns
                return {"classification": "spam", "confidence": 0.85}
        
        # PROMOTIONAL DETECTION: Clear promotional keywords
        strong_promo = [
            "sale", "discount", "save now", "limited time", "50%", "%off", "free shipping",
            "flash sale", "special offer", "today only", "while supplies last"
        ]
        
        moderate_promo = [
            "promotion", "offer", "deal", "shop now", "buy now", "order today",
            "exclusive", "limited", "urgent offer"
        ]
        
        for promo in strong_promo:
            if promo in subject or promo in email_body:
                confidence = 0.9 if "unsubscribe" not in email_body else 0.75
                return {"classification": "promotional", "confidence": confidence}
        
        # Check sender reputation
        trusted_domains = [
            "yourbank.com", "paypal.com", "amazon.com", "apple.com", "google.com",
            "microsoft.com", "github.com", "stripe.com"
        ]
        
        for trusted_domain in trusted_domains:
            if trusted_domain in sender_domain:
                return {"classification": "important", "confidence": 0.9}
        
        # IMPORTANT INDICATORS: Account, transaction, security related
        important_keywords = [
            "account verification", "payment received", "order confirmed", "shipment",
            "appointment", "confirmation", "receipt", "invoice", "transaction",
            "security alert", "password reset", "login attempt", "new device"
        ]
        
        for keyword in important_keywords:
            if keyword in subject or keyword in email_body:
                # High confidence for security alerts
                if "security" in keyword or "alert" in keyword:
                    return {"classification": "important", "confidence": 0.95}
                return {"classification": "important", "confidence": 0.85}
        
        # DEFAULT: Moderate confidence important for unknown emails
        return {"classification": "important", "confidence": 0.55}
    
    @staticmethod
    def code_review(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Smart code review with realistic issue detection and confidence scoring"""
        code = obs.get("code_snippet", "").lower()
        code_original = obs.get("code_snippet", "")
        lines = code_original.split("\n")
        
        issues = set()
        severity = "none"
        priority = "low"
        confidence = 0.5  # Base confidence
        
        # CRITICAL SECURITY ISSUES
        critical_security = [
            ("eval(", "dynamic code execution"),
            ("exec(", "dynamic code execution"),
            ("__import__", "unsafe import"),
            ("os.system(", "shell injection"),
            ("subprocess.call(", "shell injection")
        ]
        
        for pattern, _ in critical_security:
            if pattern in code:
                issues.add("security")
                severity = "critical"
                priority = "high"
                confidence = 0.95  # High confidence for obvious issues
                break
        
        # HIGH SECURITY: Credentials and SQL
        if severity != "critical":
            if any(p in code for p in ["password", "api_key", "secret_key", "token ="]):
                if "=" in code and any(p in code for p in ["\"", "'"]):
                    issues.add("security")
                    severity = "critical"
                    priority = "high"
                    confidence = 0.90
            
            if "select *" in code or ("' +" in code and "select" in code):
                issues.add("security")
                severity = "critical"
                priority = "high"
                confidence = 0.92
        
        # PERFORMANCE ISSUES: Nested loops, inefficient patterns
        if severity != "critical":
            for_count = code.count("for ")
            if_count = code.count("if ")
            
            # Nested loops detected
            if for_count > 1 and "for " in code:
                # Check for actual nesting (simple heuristic)
                for line in lines:
                    if "for " in line.lower():
                        indent = len(line) - len(line.lstrip())
                        if indent > 4:  # Likely nested
                            issues.add("performance")
                            if "security" not in issues:
                                severity = "major" if severity == "none" else severity
                            confidence = 0.75
                            break
        
        # STYLE/CODE QUALITY ISSUES
        if "  =" in code or "= " not in code:
            if "security" not in issues and "performance" not in issues:
                issues.add("style")
                if severity == "none":
                    severity = "minor"
                confidence = 0.60
        
        # Add format issues
        if "TODO" in code_original or "FIXME" in code_original:
            issues.add("style")
        
        # Default return
        final_severity = severity if severity != "none" else "minor" if issues else "none"
        final_priority = priority if priority != "low" else ("medium" if issues else "low")
        
        return {
            "issue_types": list(issues) if issues else ["none"],
            "severity": final_severity,
            "priority": final_priority,
            "confidence": confidence  # WOW FACTOR: Confidence score
        }
    
    @staticmethod
    def support_routing(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Smart support routing with context awareness and confidence scoring"""
        description = obs.get("ticket_description", "").lower()
        subject = obs.get("ticket_subject", "").lower()
        sentiment = obs.get("sentiment", "neutral")
        customer_type = obs.get("customer_type", "standard")
        is_vip = obs.get("is_vip", False)
        previous_interactions = obs.get("previous_interactions", 0)
        urgency = obs.get("urgency", "normal")
        
        confidence = 0.5  # Base confidence
        
        # ESCALATION TRIGGERS: Check for critical conditions
        escalation_triggers = [
            "security" in description,
            "unauthorized" in description,
            "account compromised" in description,
            is_vip and previous_interactions > 5,
            sentiment == "angry" and previous_interactions > 2,
            urgency == "critical"
        ]
        
        if any(escalation_triggers):
            confidence = 0.90  # High confidence for escalation cases
            return {
                "department": "escalation",
                "priority": "urgent",
                "response_type": "escalate",
                "tone": "urgent",
                "estimated_resolution_time_hours": 1,
                "confidence": confidence  # WOW FACTOR: Confidence score
            }
        
        # DEPARTMENT ROUTING: Content-based classification
        billing_keywords = [
            "refund", "payment", "charged", "bill", "invoice", "subscription",
            "charge", "credit card", "duplicate", "overcharge", "billing"
        ]
        
        tech_keywords = [
            "crash", "error", "bug", "slow", "login", "app", "connection",
            "password reset", "access denied", "not working", "broken", "webhook"
        ]
        
        enterprise_keywords = [
            "enterprise", "integration", "api", "webhook", "setup", "large org",
            "organization", "custom", "500+ employees"
        ]
        
        department = "general_support"
        
        if any(k in description or k in subject for k in enterprise_keywords):
            department = "escalation"
            confidence = 0.88
        elif any(k in description or k in subject for k in billing_keywords):
            department = "billing"
            confidence = 0.85
        elif any(k in description or k in subject for k in tech_keywords):
            department = "tech_support"
            confidence = 0.82
        else:
            confidence = 0.65
        
        # PRIORITY ASSESSMENT: Multi-factor
        priority = "medium"
        
        if urgency == "critical":
            priority = "urgent"
            confidence = min(0.95, confidence + 0.15)
        elif is_vip and sentiment in ["angry", "frustrated"]:
            priority = "urgent"
            confidence = min(0.92, confidence + 0.12)
        elif sentiment == "angry":
            priority = "high"
            confidence = min(0.90, confidence + 0.10)
        elif sentiment == "frustrated" or is_vip:
            priority = "high"
            confidence = min(0.88, confidence + 0.08)
        elif sentiment == "neutral" and customer_type == "free":
            priority = "low"
            confidence = min(0.75, confidence + 0.05)
        
        # RESPONSE TYPE: Based on priority and customer type
        if department == "escalation" or priority == "urgent":
            response_type = "escalate"
        elif priority == "high" or is_vip:
            response_type = "human_review"
        elif sentiment == "neutral" and customer_type == "free":
            response_type = "auto_reply"
        else:
            response_type = "human_review"
        
        # TONE: Context-aware
        if sentiment == "angry" or urgency == "critical":
            tone = "empathetic" if sentiment == "angry" else "urgent"
        elif is_vip or customer_type == "premium":
            tone = "formal"
        elif priority == "urgent":
            tone = "urgent"
        elif sentiment == "neutral":
            tone = "formal"
        else:
            tone = "casual"
        
        # Cap confidence at [0.0, 1.0]
        confidence = max(0.0, min(1.0, confidence))
        
        return {
            "department": department,
            "priority": priority,
            "response_type": response_type,
            "tone": tone,
            "estimated_resolution_time_hours": 1 if priority == "urgent" else (4 if priority == "high" else 24),
            "confidence": confidence  # WOW FACTOR: Confidence score
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

