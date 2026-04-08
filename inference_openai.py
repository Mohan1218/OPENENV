import os
import json
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def run():
    print("[START] OpenAI inference started")

    res = requests.get(f"{API_BASE_URL}/reset")
    obs = res.json()

    total_score = 0
    step_num = 0

    while True:
        step_num += 1

        prompt = f"""
You are a customer support agent.

Conversation: {obs.get("conversation")}
Customer Type: {obs.get("customer_type")}
Sentiment: {obs.get("sentiment")}
Time: {obs.get("time")}

Choose best action:

Return ONLY JSON:
{{
  "department": "billing/tech/support",
  "priority": "low/medium/high",
  "response_type": "auto_reply/escalate/resolve",
  "tone": "empathetic/formal/urgent"
}}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content

# 🔥 OpenAI call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Return JSON action only"},
        {"role": "user", "content": str(obs)}
    ]
)

content = response.choices[0].message.content

# 🔥 Existing logic (keep this)
try:
    action = json.loads(content)
except:
    action = {
        "department": "support",
        "priority": "medium",
        "response_type": "resolve",
        "tone": "empathetic"
    }

        res = requests.post(f"{API_BASE_URL}/step", json=action)
        data = res.json()

        reward = data["reward"]
        done = data["done"]

        total_score += reward

        print(f"[STEP] {step_num} | reward={reward} | action={action}")

        if done:
            break

        obs = data.get("next_state", {})

    print(f"[END] total_score={total_score}")


if __name__ == "__main__":
    run()
