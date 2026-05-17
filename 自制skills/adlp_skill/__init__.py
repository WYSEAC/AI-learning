# AI-Driven Learning Project Framework (ADLP)
# Version: 1.0.0
# Description: 通过AI辅助，将复杂的学习目标拆解为可执行的项目，通过数据驱动决策，实现高效学习转型

__version__ = "1.0.0"
__author__ = "ADLP Framework"

from .core.engine import ADLPEngine
from .core.profile import UserProfile, TargetPosition, SkillGap
from .core.path_designer import LearningPathDesigner
from .core.project_manager import ProjectManager
from .core.career_prep import CareerPreparation

__all__ = [
    'ADLPEngine',
    'UserProfile',
    'TargetPosition',
    'SkillGap',
    'LearningPathDesigner',
    'ProjectManager',
    'CareerPreparation',
]
