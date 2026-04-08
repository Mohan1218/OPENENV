from env.environment import SupportEnv


def run_baseline():
    env = SupportEnv()
    obs = env.reset()

    total_score = 0
    correct_count = 0
    total = 0

    while True:
        msg = " ".join(obs["conversation"]).lower()

        # simple rule-based logic
        if "payment" in msg or "refund" in msg or "charged" in msg:
            dept = "billing"
        elif "login" in msg or "crash" in msg or "app" in msg:
            dept = "tech"
        else:
            dept = "support"

        action = {
            "department": dept,
            "priority": "high",
            "response_type": "escalate",
            "tone": "empathetic"   # ✅ IMPORTANT
        }

        obs, reward, done, _ = env.step(action)

        total_score += reward

        if reward > 0:
            correct_count += 1

        total += 1

        if done:
            break

    return {
        "baseline_score": total_score,
        "accuracy": correct_count / total if total > 0 else 0
    }
