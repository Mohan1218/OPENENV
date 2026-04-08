"""
Inference script for OpenEnv
Evaluates models within the environment using the FastAPI interface
Reads API credentials from HF_TOKEN environment variable
"""
import os
import requests
import json
from typing import Dict, Any

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "rule-based-baseline")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Will use for API calls if needed


class BaselineAgent:
    """Simple rule-based agent for inference"""
    
    @staticmethod
    def get_email_action(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate email classification action"""
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
    def get_code_action(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code review action"""
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
            "priority": "high" if severity == "critical" else "low"
        }
    
    @staticmethod
    def get_support_action(obs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate support routing action"""
        description = obs.get("ticket_description", "").lower()
        sentiment = obs.get("sentiment", "neutral")
        customer_type = obs.get("customer_type", "free")
        
        # Department
        if "pay" in description or "refund" in description or "charged" in description:
            department = "billing"
        elif "crash" in description or "error" in description or "slow" in description:
            department = "tech_support"
        else:
            department = "general_support"
        
        # Priority
        if sentiment == "angry" or customer_type == "premium":
            priority = "urgent"
        elif sentiment == "frustrated":
            priority = "high"
        else:
            priority = "medium"
        
        # Response type
        if priority == "urgent":
            response_type = "escalate"
        elif sentiment == "positive":
            response_type = "auto_reply"
        else:
            response_type = "human_review"
        
        # Tone
        if sentiment == "angry":
            tone = "empathetic"
        elif customer_type == "premium":
            tone = "formal"
        else:
            tone = "casual"
        
        return {
            "department": department,
            "priority": priority,
            "response_type": response_type,
            "tone": tone,
            "estimated_resolution_time_hours": 2 if priority == "urgent" else 24
        }


def run_task_inference(task_id: str = "support_routing", difficulty: str = "easy"):
    """Run inference on a specific task"""
    print(f"\n{'='*60}")
    print(f"Running inference: {task_id} ({difficulty})")
    print(f"Model: {MODEL_NAME}")
    print(f"{'='*60}\n")
    
    # Initialize environment
    init_response = requests.post(
        f"{API_BASE_URL}/init",
        params={"task_id": task_id, "difficulty": difficulty}
    )
    
    if init_response.status_code != 200:
        print(f"Error initializing environment: {init_response.text}")
        return None
    
    # Reset environment
    reset_response = requests.get(f"{API_BASE_URL}/reset")
    obs = reset_response.json()
    
    total_score = 0.0
    step_count = 0
    
    while True:
        step_count += 1
        
        if not obs or obs == {}:
            break
        
        # Get action based on task type
        if task_id == "email_classification":
            action = BaselineAgent.get_email_action(obs)
        elif task_id == "code_review":
            action = BaselineAgent.get_code_action(obs)
        elif task_id == "support_routing":
            action = BaselineAgent.get_support_action(obs)
        else:
            print(f"Unknown task: {task_id}")
            break
        
        # Step environment
        step_response = requests.post(
            f"{API_BASE_URL}/step",
            json={"task_id": task_id, "difficulty": difficulty, "data": action}
        )
        
        if step_response.status_code != 200:
            print(f"Error stepping environment: {step_response.text}")
            break
        
        step_data = step_response.json()
        reward = step_data.get("reward", 0.0)
        done = step_data.get("done", False)
        info = step_data.get("info", {})
        obs = step_data.get("next_state", {})
        
        total_score += reward
        
        if "grade" in info and "reasoning" in info["grade"]:
            reasoning = info["grade"]["reasoning"][:60]
            print(f"  Step {step_count}: reward={reward:.2f} | {reasoning}...")
        else:
            print(f"  Step {step_count}: reward={reward:.2f}")
        
        if done:
            break
    
    print(f"\n✓ Episode complete!")
    print(f"  Total Score: {total_score:.2f}")
    print(f"  Total Steps: {step_count}")
    print(f"  Avg Reward/Step: {total_score/step_count:.2f}\n")
    
    return {
        "task_id": task_id,
        "difficulty": difficulty,
        "total_score": total_score,
        "steps": step_count,
        "avg_reward": total_score / step_count if step_count > 0 else 0.0
    }


def run_all_inference():
    """Run inference on all tasks"""
    print("\n" + "="*60)
    print("OpenEnv Baseline Inference")
    print("="*60)
    
    results = {
        "model": MODEL_NAME,
        "api_url": API_BASE_URL,
        "tasks": []
    }
    
    tasks = [
        ("email_classification", "easy"),
        ("code_review", "medium"),
        ("support_routing", "hard")
    ]
    
    total_score = 0.0
    
    for task_id, difficulty in tasks:
        try:
            result = run_task_inference(task_id, difficulty)
            if result:
                results["tasks"].append(result)
                total_score += result["avg_reward"]
        except Exception as e:
            print(f"Error running inference: {e}")
    
    if results["tasks"]:
        results["overall_avg_reward"] = total_score / len(results["tasks"])
    
    print("\n" + "="*60)
    print("INFERENCE SUMMARY")
    print("="*60)
    for task in results["tasks"]:
        print(f"{task['task_id']} ({task['difficulty']}):")
        print(f"  Score: {task['total_score']:.2f}")
        print(f"  Steps: {task['steps']}")
        print(f"  Avg/Step: {task['avg_reward']:.2f}")
    
    if "overall_avg_reward" in results:
        print(f"\nOverall Average Reward: {results['overall_avg_reward']:.2f}")
    
    return results


if __name__ == "__main__":
    # Run all task inference
    results = run_all_inference()
    
    # Print JSON
    print("\nJSON Results:")
    print(json.dumps(results, indent=2))

