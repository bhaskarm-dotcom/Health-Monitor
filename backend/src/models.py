from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"  # 80-100
    WATCH = "watch"  # 60-79
    AT_RISK = "at_risk"  # < 60


class Task(BaseModel):
    id: str
    title: str
    status: TaskStatus
    assignee_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    is_blocked: bool = False
    is_reopened: bool = False
    comments: List[str] = []
    tags: List[str] = []


class TeamMember(BaseModel):
    id: str
    name: str
    email: str
    tasks: List[str] = []  # Task IDs


class Communication(BaseModel):
    id: str
    source: str  # "email", "slack", "comment", "bug"
    author: str
    content: str
    timestamp: datetime
    sentiment: Optional[str] = None  # "positive", "neutral", "negative"


class Project(BaseModel):
    id: str
    name: str
    description: str
    tasks: List[Task] = []
    team_members: List[TeamMember] = []
    communications: List[Communication] = []
    created_at: datetime


class DimensionScore(BaseModel):
    name: str
    score: float  # 0-100
    weight: float
    details: Dict = {}


class HealthScore(BaseModel):
    overall_score: float  # 0-100
    status: HealthStatus
    dimensions: List[DimensionScore]
    calculated_at: datetime
    previous_score: Optional[float] = None
    trend: Optional[str] = None  # "improving", "declining", "stable"


class Risk(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # "high", "medium", "low"
    category: str  # "delivery", "workload", "sentiment", "risk", "momentum"
    detected_at: datetime


class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    category: str
    impact: str  # Expected impact on health score


class HealthReport(BaseModel):
    project_id: str
    project_name: str
    health_score: HealthScore
    risks: List[Risk]
    recommendations: List[Recommendation]
    generated_at: datetime

