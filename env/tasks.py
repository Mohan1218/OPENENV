"""
OpenEnv Task Definitions
Defines three real-world tasks with varying difficulty
"""

def get_tasks():
    """Return all available tasks"""
    return {
        "tasks": [
            {
                "task_id": "email_classification",
                "name": "Email Classification",
                "description": "Classify incoming emails as important, spam, or promotional",
                "difficulty": "easy",
                "max_steps": 6,
                "observation_space": {
                    "email_subject": "string",
                    "email_body": "string",
                    "sender_domain": "string",
                    "has_links": "boolean",
                    "has_attachments": "boolean",
                    "word_count": "integer"
                },
                "action_space": {
                    "classification": ["important", "spam", "promotional"],
                    "confidence": "float[0.0-1.0]"
                },
                "reward_range": [-1.0, 1.0],
                "success_criteria": "Correctly classify emails with high confidence"
            },
            {
                "task_id": "code_review",
                "name": "Code Review",
                "description": "Review code snippets and identify security, style, logic, and performance issues",
                "difficulty": "medium",
                "max_steps": 4,
                "observation_space": {
                    "code_snippet": "string",
                    "language": "string",
                    "context": "string",
                    "function_name": "string",
                    "lines_of_code": "integer"
                },
                "action_space": {
                    "issue_types": ["security", "style", "logic", "performance", "none"],
                    "severity": ["critical", "major", "minor", "none"],
                    "suggested_fix": "optional string",
                    "priority": ["high", "medium", "low"]
                },
                "reward_range": [-1.0, 1.0],
                "success_criteria": "Correctly identify all issues and their severity levels"
            },
            {
                "task_id": "support_routing",
                "name": "Customer Support Routing",
                "description": "Route support tickets to appropriate departments with correct priority and response type",
                "difficulty": "hard",
                "max_steps": 4,
                "observation_space": {
                    "ticket_subject": "string",
                    "ticket_description": "string",
                    "customer_type": ["free", "standard", "premium"],
                    "sentiment": ["positive", "neutral", "frustrated", "angry"],
                    "issue_category": ["billing", "technical", "general", "mixed"],
                    "previous_interactions": "integer",
                    "account_age_days": "integer",
                    "is_vip": "boolean"
                },
                "action_space": {
                    "department": ["billing", "tech_support", "general_support", "escalation"],
                    "priority": ["low", "medium", "high", "urgent"],
                    "response_type": ["auto_reply", "human_review", "escalate"],
                    "tone": ["empathetic", "formal", "urgent", "casual"],
                    "estimated_resolution_time_hours": "integer[1-72]"
                },
                "reward_range": [-1.0, 1.0],
                "success_criteria": "Route tickets with correct department, priority, and response type"
            }
        ],
        "metadata": {
            "total_tasks": 3,
            "total_episodes_per_task": 3,
            "episode_types": ["easy", "medium", "hard"]
        }
    }


def get_task_by_id(task_id):
    """Get specific task by ID"""
    tasks = get_tasks()["tasks"]
    for task in tasks:
        if task["task_id"] == task_id:
            return task
    return None

