from enum import Enum
from typing import Any, Dict, List, Tuple

from env.grader import compute_score
from env.task_data_code_review import (
    CODE_REVIEW_EASY_DATA,
    CODE_REVIEW_HARD_DATA,
    CODE_REVIEW_MEDIUM_DATA,
)
from env.task_data_email import (
    EMAIL_CLASSIFICATION_EASY_DATA,
    EMAIL_CLASSIFICATION_HARD_DATA,
    EMAIL_CLASSIFICATION_MEDIUM_DATA,
)
from env.task_data_support import (
    SUPPORT_ROUTING_EASY_DATA,
    SUPPORT_ROUTING_HARD_DATA,
    SUPPORT_ROUTING_MEDIUM_DATA,
)


class TaskDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class BaseTaskEnv:
    def __init__(self, task_id: str, difficulty: TaskDifficulty):
        self.task_id = task_id
        self.difficulty = difficulty
        self.data: List[Dict[str, Any]] = self._load_data()
        self.index = 0
        self.total_score = 0.0

    def _load_data(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def reset(self) -> Dict[str, Any]:
        self.index = 0
        self.total_score = 0.0
        return self.state()

    def state(self) -> Dict[str, Any]:
        if self.index >= len(self.data):
            return {}

        item = self.data[self.index]
        obs = self._build_observation(item)
        obs["task_id"] = self.task_id
        obs["step"] = self.index
        obs["episode_length"] = len(self.data)
        return obs

    def _build_observation(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def _build_correct(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def _required_action_keys(self) -> List[str]:
        raise NotImplementedError

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        if self.index >= len(self.data):
            return {}, 0.0, True, {
                "task_id": self.task_id,
                "total_score": self.total_score,
                "reason": "episode_complete",
            }

        if not isinstance(action, dict):
            self.index += 1
            done = self.index >= len(self.data)
            reward = 0.0
            self.total_score += reward
            next_obs = {} if done else self.state()
            return next_obs, reward, done, {
                "task_id": self.task_id,
                "difficulty": self.difficulty.value,
                "step": self.index,
                "episode_length": len(self.data),
                "total_score": self.total_score,
                "grade": {
                    "score": reward,
                    "reasoning": "Invalid action type; expected object/dict",
                },
            }

        current = self.data[self.index]
        required_keys = self._required_action_keys()
        missing_keys = [key for key in required_keys if key not in action]

        grading_payload: Dict[str, Any] = {
            "task_id": self.task_id,
            "predicted": action,
            "correct": self._build_correct(current),
        }

        if self.task_id == "support_routing":
            grading_payload["sentiment"] = current.get("sentiment")
            grading_payload["customer_type"] = current.get("customer_type")

        grade = compute_score(grading_payload)
        base_reward = float(grade.get("score", 0.0))

        # Penalize invalid / incomplete behavior while keeping reward in [0, 1]
        missing_penalty = min(0.5, 0.2 * len(missing_keys))
        unexpected_keys = [key for key in action.keys() if key not in required_keys]
        unexpected_penalty = min(0.2, 0.05 * len(unexpected_keys))
        reward = max(0.0, min(1.0, base_reward - missing_penalty - unexpected_penalty))

        if missing_keys or unexpected_keys:
            details: List[str] = []
            if missing_keys:
                details.append(f"missing action keys: {', '.join(missing_keys)}")
            if unexpected_keys:
                details.append(f"unexpected action keys: {', '.join(unexpected_keys)}")
            grade["reasoning"] = f"{grade.get('reasoning', '')} | penalty: {'; '.join(details)}".strip()
            grade["score"] = reward

        self.total_score += reward
        self.index += 1

        done = self.index >= len(self.data)
        next_obs = {} if done else self.state()

        return next_obs, reward, done, {
            "task_id": self.task_id,
            "difficulty": self.difficulty.value,
            "step": self.index,
            "episode_length": len(self.data),
            "total_score": self.total_score,
            "grade": grade,
        }


class EmailEnv(BaseTaskEnv):
    def __init__(self, difficulty: TaskDifficulty = TaskDifficulty.EASY):
        super().__init__("email_classification", difficulty)

    def _load_data(self) -> List[Dict[str, Any]]:
        if self.difficulty == TaskDifficulty.EASY:
            return EMAIL_CLASSIFICATION_EASY_DATA.copy()
        if self.difficulty == TaskDifficulty.MEDIUM:
            return EMAIL_CLASSIFICATION_MEDIUM_DATA.copy()
        return EMAIL_CLASSIFICATION_HARD_DATA.copy()

    def _build_observation(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "email_subject": item["email_subject"],
            "email_body": item["email_body"],
            "sender_domain": item["sender_domain"],
            "has_links": item["has_links"],
            "has_attachments": item["has_attachments"],
            "word_count": item["word_count"],
        }

    def _build_correct(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {"classification": item["correct_classification"]}

    def _required_action_keys(self) -> List[str]:
        return ["classification", "confidence"]


class CodeReviewEnv(BaseTaskEnv):
    def __init__(self, difficulty: TaskDifficulty = TaskDifficulty.MEDIUM):
        super().__init__("code_review", difficulty)

    def _load_data(self) -> List[Dict[str, Any]]:
        if self.difficulty == TaskDifficulty.EASY:
            return CODE_REVIEW_EASY_DATA.copy()
        if self.difficulty == TaskDifficulty.MEDIUM:
            return CODE_REVIEW_MEDIUM_DATA.copy()
        return CODE_REVIEW_HARD_DATA.copy()

    def _build_observation(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "code_snippet": item["code_snippet"],
            "language": item["language"],
            "context": item["context"],
            "function_name": item["function_name"],
            "lines_of_code": item["lines_of_code"],
        }

    def _build_correct(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "issue_types": item["correct_issues"],
            "severity": item["correct_severity"],
        }

    def _required_action_keys(self) -> List[str]:
        return ["issue_types", "severity", "priority"]


class SupportEnv(BaseTaskEnv):
    def __init__(self, difficulty: TaskDifficulty = TaskDifficulty.EASY, task_id: str = "support_routing"):
        super().__init__(task_id, difficulty)

    def _load_data(self) -> List[Dict[str, Any]]:
        if self.difficulty == TaskDifficulty.EASY:
            return SUPPORT_ROUTING_EASY_DATA.copy()
        if self.difficulty == TaskDifficulty.MEDIUM:
            return SUPPORT_ROUTING_MEDIUM_DATA.copy()
        return SUPPORT_ROUTING_HARD_DATA.copy()

    def _build_observation(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ticket_subject": item["ticket_subject"],
            "ticket_description": item["ticket_description"],
            "customer_type": item["customer_type"],
            "sentiment": item["sentiment"],
            "issue_category": item["issue_category"],
            "previous_interactions": item["previous_interactions"],
            "account_age_days": item["account_age_days"],
            "is_vip": item["is_vip"],
        }

    def _build_correct(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "department": item["correct_department"],
            "priority": item["correct_priority"],
            "response_type": item["correct_response_type"],
            "tone": item["correct_tone"],
        }

    def _required_action_keys(self) -> List[str]:
        return [
            "department",
            "priority",
            "response_type",
            "tone",
            "estimated_resolution_time_hours",
        ]


def create_env(task_id: str, difficulty: str = "easy") -> BaseTaskEnv:
    try:
        parsed_difficulty = TaskDifficulty(difficulty.lower().strip())
    except ValueError as exc:
        raise ValueError(f"Invalid difficulty: {difficulty}. Use easy|medium|hard") from exc

    if task_id == "email_classification":
        return EmailEnv(parsed_difficulty)
    if task_id == "code_review":
        return CodeReviewEnv(parsed_difficulty)
    if task_id == "support_routing":
        return SupportEnv(parsed_difficulty)

    raise ValueError(f"Unknown task_id: {task_id}")
