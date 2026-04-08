"""
OpenEnv Pydantic Models for Three Real-World Tasks
"""
from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any, Optional
from enum import Enum


# ============================================================================
# TASK 1: EMAIL CLASSIFICATION (Easy)
# ============================================================================

class EmailClassificationAction(BaseModel):
    """Action for email classification task"""
    classification: Literal["important", "spam", "promotional"]
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")


class EmailClassificationObservation(BaseModel):
    """Observation for email classification task"""
    email_subject: str
    email_body: str
    sender_domain: str
    has_links: bool
    has_attachments: bool
    word_count: int


class EmailClassificationReward(BaseModel):
    """Reward structure for email classification"""
    step_reward: float = Field(..., ge=-1.0, le=1.0)
    reasoning: str


# ============================================================================
# TASK 2: CODE REVIEW (Medium)
# ============================================================================

class CodeReviewIssueType(str, Enum):
    SECURITY = "security"
    STYLE = "style"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    NONE = "none"


class CodeReviewAction(BaseModel):
    """Action for code review task"""
    issue_types: List[CodeReviewIssueType]
    severity: Literal["critical", "major", "minor", "none"]
    suggested_fix: Optional[str] = None
    priority: Literal["high", "medium", "low"]


class CodeReviewObservation(BaseModel):
    """Observation for code review task"""
    code_snippet: str
    language: str
    context: str
    function_name: str
    lines_of_code: int


class CodeReviewReward(BaseModel):
    """Reward structure for code review"""
    step_reward: float = Field(..., ge=-1.0, le=1.0)
    reasoning: str


# ============================================================================
# TASK 3: CUSTOMER SUPPORT ROUTING (Hard)
# ============================================================================

class SupportRoutingAction(BaseModel):
    """Action for customer support routing task"""
    department: Literal["billing", "tech_support", "general_support", "escalation"]
    priority: Literal["low", "medium", "high", "urgent"]
    response_type: Literal["auto_reply", "human_review", "escalate"]
    tone: Literal["empathetic", "formal", "urgent", "casual"]
    estimated_resolution_time_hours: int = Field(..., ge=1, le=72)


class SupportRoutingObservation(BaseModel):
    """Observation for customer support routing task"""
    ticket_subject: str
    ticket_description: str
    customer_type: Literal["free", "standard", "premium"]
    sentiment: Literal["positive", "neutral", "frustrated", "angry"]
    issue_category: Literal["billing", "technical", "general", "mixed"]
    previous_interactions: int
    account_age_days: int
    is_vip: bool


class SupportRoutingReward(BaseModel):
    """Reward structure for support routing"""
    step_reward: float = Field(..., ge=-1.0, le=1.0)
    reasoning: str


# ============================================================================
# GENERIC OPENENV MODELS
# ============================================================================

class GenericObservation(BaseModel):
    """Generic observation wrapper that can contain any task observation"""
    task_id: Literal["email_classification", "code_review", "support_routing"]
    data: Dict[str, Any]
    step: int
    episode_length: int


class GenericAction(BaseModel):
    """Generic action wrapper that can contain any task action"""
    task_id: Literal["email_classification", "code_review", "support_routing"]
    data: Dict[str, Any]


class GenericReward(BaseModel):
    """Generic reward wrapper"""
    task_id: Literal["email_classification", "code_review", "support_routing"]
    step_reward: float = Field(..., ge=-1.0, le=1.0)
    cumulative_reward: float
    reasoning: str
    done: bool


class EnvironmentInfo(BaseModel):
    """Additional information returned from environment"""
    task_id: str
    step_count: int
    episode_length: int
    total_reward: float
    done: bool
    reason: Optional[str] = None
