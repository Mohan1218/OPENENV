"""
UPGRADED: Email Classification Task Data with Realistic Scenarios
"""

EMAIL_CLASSIFICATION_EASY_DATA = [
    {
        "email_subject": "Account verification required",
        "email_body": "We need to verify your identity. Please click the link below to complete verification within 24 hours. This is required to keep your account secure.",
        "sender_domain": "security@yourbank.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 45,
        "correct_classification": "important",
        "difficulty": "easy",
        "confidence_hint": 0.95
    },
    {
        "email_subject": "🔥 FLASH SALE: 70% OFF - Last 2 Hours Only!",
        "email_body": "Limited stock! DON'T MISS OUT. Flash sale ends in 2 hours. Click here NOW to shop before items sell out. Use code FLASH70 for additional 10% off!",
        "sender_domain": "promotions@retailstore.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "promotional",
        "difficulty": "easy",
        "confidence_hint": 0.90
    },
    {
        "email_subject": "URGENT: Claim Your Amazon Gift Card NOW",
        "email_body": "Congratulations! You have won a $500 Amazon gift card. Click here immediately to claim your prize. This offer expires in 24 hours. Verify your account now.",
        "sender_domain": "noreply@amazons-promo.tk",
        "has_links": True,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "spam",
        "difficulty": "easy",
        "confidence_hint": 0.85
    },
    {
        "email_subject": "Your payment failed - immediate action needed",
        "email_body": "Your recent payment attempt failed. Please update your billing information immediately. Your services may be interrupted if payment is not received within 48 hours. Click here to update payment.",
        "sender_domain": "billing@servicecompany.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 50,
        "correct_classification": "important",
        "difficulty": "easy",
        "confidence_hint": 0.88
    },
    {
        "email_subject": "Your order #AB-12345 is being prepared",
        "email_body": "Thank you for your purchase! We are preparing your order for shipment. You will receive a tracking number within 24 hours. Estimated delivery is 3-5 business days.",
        "sender_domain": "orders@ecommerce-platform.com",
        "has_links": False,
        "has_attachments": False,
        "word_count": 45,
        "correct_classification": "important",
        "difficulty": "easy",
        "confidence_hint": 0.92
    },
    {
        "email_subject": "New Luxury Products - Exclusive Member Offer",
        "email_body": "As a valued member, get early access to our new luxury collection. Browse the latest arrivals and enjoy free shipping on orders over $100. Limited quantity available. Shop now.",
        "sender_domain": "marketing@luxurybrand.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "promotional",
        "difficulty": "easy",
        "confidence_hint": 0.87
    },
]

EMAIL_CLASSIFICATION_MEDIUM_DATA = [
    {
        "email_subject": "Re: Project deadline update",
        "email_body": "Thanks for your email. The project deadline has been moved to Friday. However, I also saw your promotional email about the conference. Please remove me from that distribution list.",
        "sender_domain": "colleague@company.com",
        "has_links": False,
        "has_attachments": True,
        "word_count": 50,
        "correct_classification": "important",
        "difficulty": "medium",
        "confidence_hint": 0.75
    },
    {
        "email_subject": "Congratulations on reaching 1M points!",
        "email_body": "You have accumulated 1 million loyalty points! Redeem them now for exclusive rewards. Visit your account to see available options. Valid for 30 days.",
        "sender_domain": "rewards@loyaltyprogram.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "promotional",
        "difficulty": "medium",
        "confidence_hint": 0.80
    },
    {
        "email_subject": "System maintenance notice - services will be down",
        "email_body": "Scheduled server maintenance on Saturday 2-6 AM UTC. All services will be unavailable during this time. Thank you for your patience. For urgent support, contact...",
        "sender_domain": "notifications@serviceapi.com",
        "has_links": False,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "important",
        "difficulty": "medium",
        "confidence_hint": 0.70
    },
    {
        "email_subject": "FINAL NOTICE: Update Your Payment Information",
        "email_body": "This is the FINAL NOTICE before we cancel your account. Your account has been flagged for non-payment. Update now or lose access. Serious consequences may apply.",
        "sender_domain": "billing@unknowndomain.ru",
        "has_links": True,
        "has_attachments": False,
        "word_count": 35,
        "correct_classification": "spam",
        "difficulty": "medium",
        "confidence_hint": 0.72
    },
]

EMAIL_CLASSIFICATION_HARD_DATA = [
    {
        "email_subject": "Weekly newsletter: Industry insights",
        "email_body": "This week's top stories: AI advances, market trends, and upcoming events. Plus, check out our special offers on premium courses. Subscribe to our newsletter for weekly updates. Curated content just for you.",
        "sender_domain": "newsletter@industrynews.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 55,
        "correct_classification": "promotional",
        "difficulty": "hard",
        "confidence_hint": 0.65,
        "note": "Tricky: contains promotional content but also valuable information"
    },
    {
        "email_subject": "Unusual login attempt from new device",
        "email_body": "We detected a login to your account from a Samsung device in Tokyo at 3:45 AM. If this was you, no action needed. However, if you don't recognize this, please change your password immediately.",
        "sender_domain": "security@cloudservice.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 50,
        "correct_classification": "important",
        "difficulty": "hard",
        "confidence_hint": 0.70,
        "note": "Contains optional action but IS security-critical"
    },
    {
        "email_subject": "Special offer: Get $50 credit on your next purchase",
        "email_body": "As an apology for the recent service disruption, we're offering $50 credit. Seems like a promotional email, but this is actually our way of compensating customers. No code needed - automatically applied.",
        "sender_domain": "customer-care@mainservice.com",
        "has_links": False,
        "has_attachments": False,
        "word_count": 50,
        "correct_classification": "important",
        "difficulty": "hard",
        "confidence_hint": 0.60,
        "note": "Looks promotional but is actually important customer service"
    },
]

EMAIL_CLASSIFICATION_MEDIUM_DATA_EXTENDED = EMAIL_CLASSIFICATION_MEDIUM_DATA + [
    {
        "email_subject": "Your feedback matters - rate our service",
        "email_body": "We would love to hear from you! Please take 2 minutes to rate your recent experience with our support team. Your feedback helps us improve. Click here to provide feedback.",
        "sender_domain": "feedback@company.com",
        "has_links": True,
        "has_attachments": False,
        "word_count": 40,
        "correct_classification": "promotional",
        "difficulty": "medium",
        "confidence_hint": 0.78
    },
]

EMAIL_CLASSIFICATION_HARD_DATA_EXTENDED = EMAIL_CLASSIFICATION_HARD_DATA + [
    {
        "email_subject": "Payment received - invoice #INV-2024-001",
        "email_body": "Thank you for your payment of $1,299. We have received and processed your payment. Invoice details attached. For billing questions, contact our finance team at billing@company.com.",
        "sender_domain": "invoices@company.com",
        "has_links": False,
        "has_attachments": True,
        "word_count": 40,
        "correct_classification": "important",
        "difficulty": "hard",
        "confidence_hint": 0.88
    },
]
