"""
Email Classification Task Data - Easy Difficulty
"""

EMAIL_CLASSIFICATION_EASY_DATA = [
    {
        "email_subject": "Welcome to our service!",
        "email_body": "Thank you for signing up. Please verify your email to get started.",
        "sender_domain": "noreply@ourcompany.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 25,
        "correct_classification": "important",
        "difficulty": "easy"
    },
    {
        "email_subject": "LIMITED TIME: 50% off everything!!",
        "email_body": "Click here now to get our massive sale. Act fast, expires soon!!!",
        "sender_domain": "marketing@store.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 20,
        "correct_classification": "promotional",
        "difficulty": "easy"
    },
    {
        "email_subject": "You've won $1,000,000! Claim now",
        "email_body": "Congratulations! You have been selected. Click link to claim prize.",
        "sender_domain": "random@suspiciousdomain.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 18,
        "correct_classification": "spam",
        "difficulty": "easy"
    },
    {
        "email_subject": "Your order #12345 has shipped",
        "email_body": "Your package is on its way! Track it here.",
        "sender_domain": "orders@shop.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 15,
        "correct_classification": "important",
        "difficulty": "easy"
    },
    {
        "email_subject": "URGENT: Verify your account now",
        "email_body": "Your account will be closed if you don't verify. Click here immediately.",
        "sender_domain": "security@fakebank.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 20,
        "correct_classification": "spam",
        "difficulty": "easy"
    },
    {
        "email_subject": "New blog post: 5 tips for productivity",
        "email_body": "Read our latest article on improving your workflow.",
        "sender_domain": "blog@ourcompany.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 16,
        "correct_classification": "promotional",
        "difficulty": "easy"
    }
]

EMAIL_CLASSIFICATION_MEDIUM_DATA = [
    {
        "email_subject": "Re: Project update",
        "email_body": "Thanks for the feedback. I've addressed your concerns in the latest version.",
        "sender_domain": "colleague@ourcompany.com",
        "has_links": False,
        "has_attachments": True,
        "word_count": 20,
        "correct_classification": "important",
        "difficulty": "medium"
    },
    {
        "email_subject": "Free trial! Access premium features",
        "email_body": "Limited time offer just for you. No credit card required.",
        "sender_domain": "trials@service.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 15,
        "correct_classification": "promotional",
        "difficulty": "medium"
    },
    {
        "email_subject": "Unusual activity detected",
        "email_body": "Someone tried to access your account from a new location.",
        "sender_domain": "security@platform.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 18,
        "correct_classification": "important",
        "difficulty": "medium"
    },
    {
        "email_subject": "Make $5000 working from home",
        "email_body": "Simple tasks that pay instantly. No experience needed.",
        "sender_domain": "money@quickcash.net",
        "has_links": True,
        "has_attachments": False,
        "word_count": 16,
        "correct_classification": "spam",
        "difficulty": "medium"
    }
]

EMAIL_CLASSIFICATION_HARD_DATA = [
    {
        "email_subject": "Meeting tomorrow at 2 PM",
        "email_body": "Don't forget about our discussion. Also check out this new feature.",
        "sender_domain": "team@ourcompany.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 22,
        "correct_classification": "important",
        "difficulty": "hard"
    },
    {
        "email_subject": "Subscribe now and save 20%",
        "email_body": "Hi there! We have a special offer just for subscribers. Read more.",
        "sender_domain": "marketing@ourcompany.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 21,
        "correct_classification": "promotional",
        "difficulty": "hard"
    },
    {
        "email_subject": "Invoice #2024-001",
        "email_body": "Please find the attached invoice for services rendered.",
        "sender_domain": "accounting@vendor.com",
        "has_links": False,
        "has_attachments": True,
        "word_count": 13,
        "correct_classification": "important",
        "difficulty": "hard"
    }
]
