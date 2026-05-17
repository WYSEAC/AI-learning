# ADLP Framework 核心数据类型

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class SkillLevel(Enum):
    BEGINNER = "入门"
    INTERMEDIATE = "进阶"
    ADVANCED = "高级"
    EXPERT = "专家"


class LearningStyle(Enum):
    VISUAL = "视觉型"
    AUDITORY = "听觉型"
    READING = "阅读型"
    KINESTHETIC = "实践型"
    MIXED = "混合型"


class RiskLevel(Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "极高"


@dataclass
class Skill:
    name: str
    level: SkillLevel = SkillLevel.BEGINNER
    target_level: SkillLevel = SkillLevel.INTERMEDIATE
    category: str = "通用"
    dependencies: List[str] = field(default_factory=list)
    resources: List[Dict] = field(default_factory=list)
    projects: List[Dict] = field(default_factory=list)
    estimated_hours: int = 40
    priority: int = 3


@dataclass
class UserProfile:
    name: str
    background: str
    current_role: str
    experience_years: float = 0
    education: str = "本科"
    
    current_skills: List[Skill] = field(default_factory=list)
    learning_style: LearningStyle = LearningStyle.MIXED
    weekly_available_hours: int = 20
    monthly_budget: float = 500
    
    motivation_level: int = 7  # 1-10
    stress_tolerance: int = 5   # 1-10
    persistence_level: int = 6  # 1-10
    
    constraints: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TargetPosition:
    title: str
    industry: str = "互联网"
    required_skills: List[Skill] = field(default_factory=list)
    preferred_skills: List[Skill] = field(default_factory=list)
    min_experience_years: float = 1
    avg_salary_range: List[float] = field(default_factory=lambda: [15000, 35000])
    education_requirement: str = "本科"
    job_count: int = 0
    growth_outlook: str = "中等"
    entry_barrier: str = "中等"


@dataclass 
class SkillGap:
    skill_name: str
    current_level: SkillLevel
    target_level: SkillLevel
    gap_size: int  # 1-4
    priority: int   # 1-5
    estimated_hours: int
    learning_path: List[Dict] = field(default_factory=list)
    is_critical: bool = False


@dataclass
class LearningPhase:
    name: str
    order: int
    duration_weeks: int
    goals: List[str] = field(default_factory=list)
    skills_to_learn: List[str] = field(default_factory=list)
    projects: List[Dict] = field(default_factory=list)
    resources: List[Dict] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)


@dataclass
class LearningPath:
    target_position: TargetPosition
    user_profile: UserProfile
    phases: List[LearningPhase] = field(default_factory=list)
    total_weeks: int = 12
    weekly_schedule: Dict[int, Dict] = field(default_factory=dict)
    risks: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Project:
    name: str
    description: str
    difficulty: str = "入门"
    estimated_hours: int = 10
    skills_covered: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    status: str = "规划中"
    progress: float = 0.0


@dataclass
class ProgressRecord:
    date: str
    week_number: int
    hours_spent: float
    skills_practiced: List[str]
    projects_completed: List[str]
    challenges: List[str]
    achievements: List[str]
    mood_score: int  # 1-10
    next_week_plan: str = ""
    notes: str = ""


@dataclass
class MarketData:
    keyword: str
    total_jobs: int = 0
    avg_salary: float = 0
    top_skills: List[Dict] = field(default_factory=list)
    top_companies: List[str] = field(default_factory=list)
    experience_distribution: Dict[str, int] = field(default_factory=dict)
    education_distribution: Dict[str, int] = field(default_factory=dict)
    city_distribution: Dict[str, int] = field(default_factory=dict)
    source: str = ""
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())
