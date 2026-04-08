from typing import Dict, Any


class SupportEnv:
    def __init__(self):
        self.data = []
        self.index = 0
        self.total_score = 0
        self._load_data()

    def _load_data(self):
        """Load simple working data"""

        self.data = [
            {
                "conversation": ["Payment failed but money deducted"],
                "customer_type": "premium",
                "sentiment": "angry",
                "time": "urgent",
                "correct": {
                    "department": "billing",
                    "priority": "high",
                    "response_type": "escalate"
                }
            },
            {
                "conversation": ["App crashes during login"],
                "customer_type": "free",
                "sentiment": "frustrated",
                "time": "medium",
                "correct": {
                    "department": "tech",
                    "priority": "high",
                    "response_type": "escalate"
                }
            },
            {
                "conversation": ["How to change password?"],
                "customer_type": "free",
                "sentiment": "neutral",
                "time": "low",
                "correct": {
                    "department": "support",
                    "priority": "low",
                    "response_type": "auto_reply"
                }
            }
        ]

    def reset(self) -> Dict[str, Any]:
        self.index = 0
        self.total_score = 0
        return self.state()

    def state(self) -> Dict[str, Any]:
        if self.index >= len(self.data):
            return {
                "conversation": [],
                "customer_type": "free",
                "sentiment": "neutral",
                "time": "low"
            }

        ticket = self.data[self.index]

        return {
            "conversation": ticket.get("conversation", []),
            "customer_type": ticket.get("customer_type", "free"),
            "sentiment": ticket.get("sentiment", "neutral"),
            "time": ticket.get("time", "low")
        }

    def step(self, action: Dict[str, Any]):
        if self.index >= len(self.data):
            return {}, 0, True, {"total_score": self.total_score}

        current = self.data[self.index]
        correct = current["correct"]

        score = 0

        if action.get("department") == correct["department"]:
            score += 0.4
        else:
            score -= 0.4

        if action.get("priority") == correct["priority"]:
            score += 0.3
        else:
            score -= 0.2

        if action.get("response_type") == correct["response_type"]:
            score += 0.3
        else:
            score -= 0.2

        if current["sentiment"] == "angry" and action.get("tone") != "empathetic":
            score -= 0.3

        if current["customer_type"] == "premium" and action.get("tone") != "formal":
            score -= 0.2

        self.total_score += score
        self.index += 1

        done = self.index >= len(self.data)

        return (
            {} if done else self.state(),
            score,
            done,
            {"total_score": self.total_score}
        )


def create_env(task_id="support_routing", difficulty="easy"):
    return SupportEnv()
