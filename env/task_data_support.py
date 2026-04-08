"""
Support Routing Task Data - Hard Difficulty
"""

SUPPORT_ROUTING_EASY_DATA = [
    {
        "ticket_subject": "How to reset my password?",
        "ticket_description": "I forgot my password and need to reset it.",
        "customer_type": "free",
        "sentiment": "neutral",
        "issue_category": "general",
        "previous_interactions": 0,
        "account_age_days": 30,
        "is_vip": False,
        "correct_department": "general_support",
        "correct_priority": "low",
        "correct_response_type": "auto_reply",
        "correct_tone": "casual",
        "difficulty": "easy"
    },
    {
        "ticket_subject": "I was charged twice!",
        "ticket_description": "My credit card was charged twice for the same order.",
        "customer_type": "premium",
        "sentiment": "angry",
        "issue_category": "billing",
        "previous_interactions": 2,
        "account_age_days": 365,
        "is_vip": True,
        "correct_department": "billing",
        "correct_priority": "urgent",
        "correct_response_type": "escalate",
        "correct_tone": "empathetic",
        "difficulty": "easy"
    },
    {
        "ticket_subject": "App keeps crashing",
        "ticket_description": "The app crashes every time I try to login.",
        "customer_type": "standard",
        "sentiment": "frustrated",
        "issue_category": "technical",
        "previous_interactions": 1,
        "account_age_days": 90,
        "is_vip": False,
        "correct_department": "tech_support",
        "correct_priority": "high",
        "correct_response_type": "human_review",
        "correct_tone": "urgent",
        "difficulty": "easy"
    }
]

SUPPORT_ROUTING_MEDIUM_DATA = [
    {
        "ticket_subject": "Refund status inquiry",
        "ticket_description": "I requested a refund 5 days ago but haven't received it yet.",
        "customer_type": "standard",
        "sentiment": "neutral",
        "issue_category": "billing",
        "previous_interactions": 3,
        "account_age_days": 180,
        "is_vip": False,
        "correct_department": "billing",
        "correct_priority": "medium",
        "correct_response_type": "human_review",
        "correct_tone": "formal",
        "difficulty": "medium"
    },
    {
        "ticket_subject": "Feature request: Dark mode",
        "ticket_description": "It would be nice if the app had a dark mode option.",
        "customer_type": "free",
        "sentiment": "positive",
        "issue_category": "general",
        "previous_interactions": 0,
        "account_age_days": 14,
        "is_vip": False,
        "correct_department": "general_support",
        "correct_priority": "low",
        "correct_response_type": "auto_reply",
        "correct_tone": "casual",
        "difficulty": "medium"
    },
    {
        "ticket_subject": "Payment method not working",
        "ticket_description": "My card is valid but the payment keeps declining.",
        "customer_type": "premium",
        "sentiment": "frustrated",
        "issue_category": "mixed",
        "previous_interactions": 5,
        "account_age_days": 720,
        "is_vip": True,
        "correct_department": "billing",
        "correct_priority": "high",
        "correct_response_type": "escalate",
        "correct_tone": "empathetic",
        "difficulty": "medium"
    }
]

SUPPORT_ROUTING_HARD_DATA = [
    {
        "ticket_subject": "Can't access my account after password change",
        "ticket_description": "After changing my password, I can't login. I also see unexpected charges.",
        "customer_type": "premium",
        "sentiment": "angry",
        "issue_category": "mixed",
        "previous_interactions": 10,
        "account_age_days": 600,
        "is_vip": True,
        "correct_department": "escalation",
        "correct_priority": "urgent",
        "correct_response_type": "escalate",
        "correct_tone": "empathetic",
        "difficulty": "hard"
    },
    {
        "ticket_subject": "Slow app performance and occasional crashes",
        "ticket_description": "The app has been slow for a week. Sometimes it crashes when loading data.",
        "customer_type": "standard",
        "sentiment": "frustrated",
        "issue_category": "technical",
        "previous_interactions": 4,
        "account_age_days": 450,
        "is_vip": False,
        "correct_department": "tech_support",
        "correct_priority": "high",
        "correct_response_type": "human_review",
        "correct_tone": "urgent",
        "difficulty": "hard"
    },
    {
        "ticket_subject": "Billing discrepancy and service not working",
        "ticket_description": "I was billed but the premium features aren't available. Need immediate help.",
        "customer_type": "premium",
        "sentiment": "angry",
        "issue_category": "mixed",
        "previous_interactions": 2,
        "account_age_days": 120,
        "is_vip": False,
        "correct_department": "escalation",
        "correct_priority": "urgent",
        "correct_response_type": "escalate",
        "correct_tone": "empathetic",
        "difficulty": "hard"
    },
    {
        "ticket_subject": "Feature not working as expected",
        "ticket_description": "The export feature doesn't include all the data I selected.",
        "customer_type": "free",
        "sentiment": "neutral",
        "issue_category": "technical",
        "previous_interactions": 0,
        "account_age_days": 7,
        "is_vip": False,
        "correct_department": "tech_support",
        "correct_priority": "low",
        "correct_response_type": "human_review",
        "correct_tone": "casual",
        "difficulty": "hard"
    }
]
