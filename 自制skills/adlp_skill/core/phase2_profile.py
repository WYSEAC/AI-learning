import random
from typing import List, Dict, Any, Optional

from .models import (UserProfile, TargetPosition, SkillGap, Skill,
                     SkillLevel, LearningStyle, RiskLevel)


class ProfileAnalyzer:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @staticmethod
    def _level_to_int(level: SkillLevel) -> int:
        return {
            SkillLevel.BEGINNER: 1,
            SkillLevel.INTERMEDIATE: 2,
            SkillLevel.ADVANCED: 3,
            SkillLevel.EXPERT: 4,
        }[level]

    @staticmethod
    def _auto_level(name: str) -> SkillLevel:
        n = name.lower()
        if any(kw in n for kw in ("高级", "精通", "expert")):
            return SkillLevel.ADVANCED
        if any(kw in n for kw in ("中级", "熟练", "intermediate")):
            return SkillLevel.INTERMEDIATE
        return SkillLevel.BEGINNER

    @staticmethod
    def _parse_learning_style(style: str) -> LearningStyle:
        mapping = {
            "visual": LearningStyle.VISUAL,
            "auditory": LearningStyle.AUDITORY,
            "reading": LearningStyle.READING,
            "kinesthetic": LearningStyle.KINESTHETIC,
            "mixed": LearningStyle.MIXED,
        }
        return mapping.get(style.lower(), LearningStyle.MIXED)

    @staticmethod
    def _estimate_hours(gap_size: int) -> int:
        ranges = {1: (20, 40), 2: (60, 120), 3: (150, 200), 4: (200, 300)}
        lo, hi = ranges.get(gap_size, (20, 40))
        return random.randint(lo, hi)

    def build_profile(self, **kwargs: Any) -> UserProfile:
        skill_names: List[str] = list(kwargs.pop("current_skills", []))
        skills: List[Skill] = []
        for name in skill_names:
            level = self._auto_level(name)
            skills.append(Skill(name=name, level=level))

        style_str: str = str(kwargs.pop("learning_style", "mixed"))
        learning_style = self._parse_learning_style(style_str)

        return UserProfile(
            name=str(kwargs.get("name", "")),
            background=str(kwargs.get("background", "")),
            current_role=str(kwargs.get("current_role", "")),
            experience_years=float(kwargs.get("experience_years", 0)),
            education=str(kwargs.get("education", "本科")),
            current_skills=skills,
            learning_style=learning_style,
            weekly_available_hours=int(kwargs.get("weekly_hours", 20)),
            motivation_level=int(kwargs.get("motivation", 7)),
            persistence_level=int(kwargs.get("persistence", 6)),
        )

    def analyze_gaps(self, user: UserProfile, target: TargetPosition) -> List[SkillGap]:
        user_skill_map: Dict[str, Skill] = {s.name: s for s in user.current_skills}
        gaps: List[SkillGap] = []

        def _process(skills: List[Skill], is_critical: bool) -> None:
            for ts in skills:
                us = user_skill_map.get(ts.name)
                current_level = us.level if us else SkillLevel.BEGINNER
                current_val = self._level_to_int(current_level) if us else 0
                target_val = self._level_to_int(ts.level)

                raw_gap = target_val - current_val
                gap_size = max(1, min(4, raw_gap))

                estimated_hours = self._estimate_hours(gap_size)

                priority = min(5, gap_size + (1 if is_critical else 0))
                if ts.level == SkillLevel.EXPERT:
                    priority = min(5, priority + 1)

                gaps.append(SkillGap(
                    skill_name=ts.name,
                    current_level=current_level,
                    target_level=ts.level,
                    gap_size=gap_size,
                    priority=priority,
                    estimated_hours=estimated_hours,
                    is_critical=is_critical,
                ))

        _process(target.required_skills, True)
        _process(target.preferred_skills, False)

        gaps.sort(key=lambda g: (-g.priority, -g.gap_size))
        return gaps

    def build_radar_data(self, user: UserProfile, target: TargetPosition,
                         gaps: List[SkillGap]) -> Dict[str, Any]:
        skill_coverage: float = 0.0
        if target.required_skills:
            user_skill_names = {s.name for s in user.current_skills}
            target_skill_names = {s.name for s in target.required_skills}
            covered = len(user_skill_names & target_skill_names)
            skill_coverage = round(covered / len(target_skill_names) * 100, 1)

        experience_match: float = 100.0
        if target.min_experience_years > 0:
            ratio = user.experience_years / target.min_experience_years
            experience_match = round(min(100.0, ratio * 100), 1)

        education_match: float = 100.0 if user.education == target.education_requirement else 50.0

        motivation: float = user.motivation_level * 10.0
        persistence: float = user.persistence_level * 10.0
        time_availability: float = round(min(100.0, user.weekly_available_hours / 20.0 * 100), 1)

        return {
            "dimensions": ["技能覆盖率", "经验匹配度", "教育匹配度", "学习动力", "时间充裕度", "坚持能力"],
            "values": [
                skill_coverage,
                experience_match,
                education_match,
                motivation,
                time_availability,
                persistence,
            ],
            "max_value": 100,
            "gap_count": len(gaps),
            "critical_gap_count": sum(1 for g in gaps if g.is_critical),
        }

    def generate_profile_report(self, user: UserProfile, target: TargetPosition,
                                gaps: List[SkillGap]) -> str:
        readiness = self.get_readiness_score(user, target)

        lines: List[str] = [
            f"# 📊 个性化学习画像报告",
            "",
            f"## 基本信息",
            f"- **姓名**: {user.name}",
            f"- **当前岗位**: {user.current_role}",
            f"- **目标岗位**: {target.title}",
            f"- **工作年限**: {user.experience_years} 年",
            f"- **学历**: {user.education}",
            f"- **学习风格**: {user.learning_style.value}",
            f"- **每周可用时间**: {user.weekly_available_hours} 小时",
            f"- **学习动力**: {user.motivation_level}/10",
            f"- **坚持能力**: {user.persistence_level}/10",
            "",
            f"## 综合就绪度: {readiness}/100",
            "",
            f"## 技能缺口分析",
            f"共识别 **{len(gaps)}** 个技能缺口：",
            "",
            "| 技能 | 当前水平 | 目标水平 | 缺口 | 优先级 | 预计学时 | 关键 |",
            "|------|----------|----------|------|--------|----------|------|",
        ]

        for g in gaps:
            critical = "⚠️" if g.is_critical else ""
            lines.append(
                f"| {g.skill_name} | {g.current_level.value} | {g.target_level.value} "
                f"| {g.gap_size} | {g.priority} | {g.estimated_hours}h | {critical} |"
            )

        lines.append("")
        lines.append("## 当前技能清单")
        if user.current_skills:
            for s in user.current_skills:
                lines.append(f"- **{s.name}**: {s.level.value}")
        else:
            lines.append("暂无记录技能")

        return "\n".join(lines)

    def get_readiness_score(self, user: UserProfile, target: TargetPosition) -> float:
        user_skill_map: Dict[str, Skill] = {s.name: s for s in user.current_skills}

        skill_scores: List[float] = []

        for ts in target.required_skills:
            us = user_skill_map.get(ts.name)
            current_val = self._level_to_int(us.level) if us else 0
            target_val = self._level_to_int(ts.level)
            gap = max(0, target_val - current_val)
            skill_scores.append(max(0.0, 100.0 - gap * 25.0))

        for ts in target.preferred_skills:
            us = user_skill_map.get(ts.name)
            current_val = self._level_to_int(us.level) if us else 0
            target_val = self._level_to_int(ts.level)
            gap = max(0, target_val - current_val)
            skill_scores.append(max(0.0, 100.0 - gap * 25.0))

        all_skills = len(target.required_skills) + len(target.preferred_skills)
        if all_skills > 0:
            skill_score = sum(skill_scores) / all_skills
        else:
            skill_score = 100.0

        if target.min_experience_years > 0:
            ratio = user.experience_years / target.min_experience_years
            experience_score = min(100.0, ratio * 100.0)
        else:
            experience_score = 100.0

        education_score = 100.0 if user.education == target.education_requirement else 50.0

        motivation_score = user.motivation_level * 10.0
        persistence_score = user.persistence_level * 10.0
        time_score = min(100.0, user.weekly_available_hours / 20.0 * 100.0)

        score = (
            skill_score * 0.40
            + experience_score * 0.20
            + education_score * 0.05
            + motivation_score * 0.15
            + time_score * 0.10
            + persistence_score * 0.10
        )

        return round(score, 1)
