"""
OpenEnv Inference Script with OpenAI Integration
Uses OpenAI API to generate agent actions
"""
import os
import requests
import json
import sys
from openai import OpenAI

# =========================
# CONFIG
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (optional - will fallback if not available)
client = None
if API_KEY:
    try:
        client = OpenAI(api_key=API_KEY)
    except Exception:
        print("[WARNING] Could not initialize OpenAI client", file=sys.stderr)
        client = None

# =========================
# GET ACTION FROM LLM
# =========================
def get_action(obs):
    """Get action from OpenAI LLM"""
    
    # Determine task from observation
    task_type = "support_routing"
    if "email_subject" in obs:
        task_type = "email_classification"
    elif "code_snippet" in obs:
        task_type = "code_review"
    
    # Build task-specific prompt
    if task_type == "email_classification":
        prompt = f"""You are an email classifier.
Given this email:
Subject: {obs.get('email_subject', '')}
Body: {obs.get('email_body', '')}

Classify it as: important, spam, or promotional
Return ONLY valid JSON:
{{"classification": "important|spam|promotional", "confidence": 0.0}}"""
    
    elif task_type == "code_review":
        prompt = f"""You are a code reviewer.
Review this code:
{obs.get('code_snippet', '')}

Identify issues: security, style, logic, performance, or none
Return ONLY valid JSON:
{{"issue_types": ["security|style|logic|performance|none"], "severity": "critical|major|minor|none", "priority": "high|medium|low"}}"""
    
    else:  # support_routing
        prompt = f"""You are a support routing agent.
Route this ticket:
Description: {obs.get('ticket_description', '')}
Customer: {obs.get('customer_type', '')}
Sentiment: {obs.get('sentiment', '')}

Return ONLY valid JSON:
{{"department": "billing|tech_support|general_support|escalation", "priority": "low|medium|high|urgent", "response_type": "auto_reply|human_review|escalate", "tone": "empathetic|formal|urgent|casual"}}"""
    
    try:
        # Use OpenAI if available, otherwise return fallback
        if not client:
            raise Exception("OpenAI client not available")
            
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500
        )
        
        text = response.choices[0].message.content
        return json.loads(text)
    except Exception as e:
        print(f"[WARNING] OpenAI call failed: {e}", file=sys.stderr)
        # Fallback action
        if task_type == "email_classification":
            return {"classification": "important", "confidence": 0.5}
        elif task_type == "code_review":
            return {"issue_types": ["none"], "severity": "none", "priority": "low"}
        else:
            return {
                "department": "general_support",
                "priority": "medium",
                "response_type": "human_review",
                "tone": "formal"
            }

# =========================
# MAIN LOOP
# =========================
def run_inference(task_id="support_routing", difficulty="easy", num_steps=10):
    """Run inference with OpenAI agent"""
    
    print(f"[START] task={task_id} difficulty={difficulty}")
    sys.stdout.flush()
    
    try:
        # Reset environment
        reset_response = requests.post(f"{API_BASE_URL}/reset")
        obs = reset_response.json()
        
        total_score = 0.0
        step_num = 0
        
        while step_num < num_steps:
            step_num += 1
            
            # Get action from OpenAI
            action = get_action(obs)
            
            # Take step in environment
            step_response = requests.post(
                f"{API_BASE_URL}/step",
                json={
                    "task_id": task_id,
                    "difficulty": difficulty,
                    "data": action
                }
            )
            
            data = step_response.json()
            
            reward = data.get("reward", 0.0)
            done = data.get("done", False)
            
            total_score += reward
            
            # Log step
            action_str = json.dumps(action).replace('"', "'")[:60]
            print(f"[STEP] step={step_num} reward={reward:.3f} action={action_str}")
            sys.stdout.flush()
            
            if done:
                break
            
            obs = data.get("next_state", {})
        
        # Final log
        print(f"[END] total_score={total_score:.3f}")
        sys.stdout.flush()
        
        return total_score
        
    except Exception as e:
        print(f"[ERROR] Inference failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 0.0


if __name__ == "__main__":
    try:
        # Run single episode
        score = run_inference(
            task_id=os.getenv("TASK_ID", "support_routing"),
            difficulty=os.getenv("DIFFICULTY", "easy"),
            num_steps=int(os.getenv("NUM_STEPS", "10"))
        )
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Script failed: {e}", file=sys.stderr)
        sys.exit(1)
