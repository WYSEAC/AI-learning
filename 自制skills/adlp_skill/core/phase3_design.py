"""ADLP 阶段三：结构化学习路径设计"""

import json
import math
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import asdict

from .models import (
    UserProfile, TargetPosition, SkillGap, LearningPath,
    LearningPhase, SkillLevel, RiskLevel
)


class PathDesigner:

    def __init__(self, config: dict):
        self.config = config
        self._phase_configs = [
            ("基础奠基", 0.25, 1),
            ("核心强化", 0.35, 2),
            ("进阶突破", 0.25, 3),
            ("求职冲刺", 0.15, 4),
        ]

    def design(
        self,
        user: UserProfile,
        target: TargetPosition,
        gaps: List[SkillGap],
        total_weeks: int
    ) -> LearningPath:
        sorted_gaps = sorted(gaps, key=lambda g: (-g.priority, g.gap_size))

        phases: List[LearningPhase] = []
        skill_index = 0
        week_cursor = 1

        for phase_name, ratio, order in self._phase_configs:
            duration = max(1, math.floor(total_weeks * ratio))
            if order == len(self._phase_configs):
                duration = total_weeks - sum(p.duration_weeks for p in phases)

            phase_skills: List[str] = []
            phase_projects: List[Dict] = []
            phase_resources: List[Dict] = []
            phase_goals: List[str] = []
            phase_checkpoints: List[str] = []

            if phase_name == "基础奠基":
                foundational = [g for g in sorted_gaps if g.gap_size <= 2 and g.skill_name not in phase_skills]
                critical = [g for g in sorted_gaps if g.is_critical and g.skill_name not in phase_skills]
                assigned = (foundational + critical)[:max(3, duration)]
                for g in assigned:
                    phase_skills.append(g.skill_name)
                phase_goals = [f"掌握 {s} 的基础概念和核心用法" for s in phase_skills]
                phase_projects = self._build_basic_projects(phase_skills)
                phase_checkpoints = [f"完成 {s} 基础练习并提交代码" for s in phase_skills]

            elif phase_name == "核心强化":
                remaining = [g for g in sorted_gaps if g.skill_name not in self._all_skills(phases)]
                assigned = remaining[:max(4, duration)]
                for g in assigned:
                    phase_skills.append(g.skill_name)
                phase_goals = [f"深入理解 {s} 并能在实际项目中灵活运用" for s in phase_skills]
                phase_projects = self._build_core_projects(phase_skills, target)
                phase_checkpoints = [f"完成 {s} 核心项目并通过自测" for s in phase_skills]

            elif phase_name == "进阶突破":
                remaining = [g for g in sorted_gaps if g.skill_name not in self._all_skills(phases)]
                assigned = remaining[:max(3, duration)]
                for g in assigned:
                    phase_skills.append(g.skill_name)
                phase_goals = [f"在 {target.title} 场景下深度应用 {s}" for s in phase_skills]
                phase_projects = self._build_advanced_projects(phase_skills, target)
                phase_checkpoints = [f"完成 {s} 综合项目并产出可展示成果" for s in phase_skills]

            elif phase_name == "求职冲刺":
                review_skills = self._all_skills(phases)
                phase_skills = review_skills[:max(6, len(review_skills))]
                phase_goals = [
                    f"系统复习全部技能栈",
                    "完成简历优化和作品集整理",
                    "模拟面试训练达到自信水平"
                ]
                phase_projects = self._build_career_projects(phase_skills, target)
                phase_checkpoints = [
                    "完成至少3次模拟面试",
                    "投递简历并获得至少1次面试机会",
                    "整理完整的作品集并上线"
                ]

            phase = LearningPhase(
                name=phase_name,
                order=order,
                duration_weeks=duration,
                goals=phase_goals,
                skills_to_learn=phase_skills,
                projects=phase_projects,
                resources=phase_resources,
                checkpoints=phase_checkpoints,
                success_criteria=[f"完成{phase_name}阶段全部任务且自评合格"]
            )
            phases.append(phase)

        weekly_schedule = self._generate_weekly_schedule(phases, total_weeks, user, target)

        risks = self._identify_risks(user, target, gaps, total_weeks)

        path = LearningPath(
            target_position=target,
            user_profile=user,
            phases=phases,
            total_weeks=total_weeks,
            weekly_schedule=weekly_schedule,
            risks=risks
        )
        return path

    def _all_skills(self, phases: List[LearningPhase]) -> List[str]:
        seen: List[str] = []
        for p in phases:
            for s in p.skills_to_learn:
                if s not in seen:
                    seen.append(s)
        return seen

    def _build_basic_projects(self, skills: List[str]) -> List[Dict]:
        projects = []
        for i, skill in enumerate(skills):
            projects.append({
                "name": f"{skill}入门实战",
                "description": f"通过小项目掌握 {skill} 的基础用法",
                "difficulty": "入门",
                "estimated_hours": 8,
                "skills_covered": [skill],
                "deliverables": [f"{skill}练习代码", "学习笔记"],
                "success_criteria": [f"能独立使用 {skill} 完成基础功能"]
            })
        return projects

    def _build_core_projects(self, skills: List[str], target: TargetPosition) -> List[Dict]:
        projects = []
        if len(skills) >= 2:
            projects.append({
                "name": f"{target.title}核心模块开发",
                "description": f"结合 {' 和 '.join(skills[:3])} 开发一个{target.title}相关功能模块",
                "difficulty": "中等",
                "estimated_hours": 20,
                "skills_covered": skills[:3],
                "deliverables": ["完整源码", "技术文档", "演示DEMO"],
                "success_criteria": ["功能完整可用", "代码规范清晰"]
            })
        for skill in skills[3:]:
            projects.append({
                "name": f"{skill}专项提升",
                "description": f"针对 {skill} 的专项强化训练",
                "difficulty": "中等",
                "estimated_hours": 12,
                "skills_covered": [skill],
                "deliverables": [f"{skill}专项项目代码"],
                "success_criteria": [f"能够用 {skill} 解决中等复杂度问题"]
            })
        return projects

    def _build_advanced_projects(self, skills: List[str], target: TargetPosition) -> List[Dict]:
        return [{
            "name": f"{target.title}综合实战项目",
            "description": f"综合运用 {'、'.join(skills)} 完成一个完整的{target.title}项目",
            "difficulty": "困难",
            "estimated_hours": 30,
            "skills_covered": skills,
            "deliverables": ["完整项目源码", "架构设计文档", "部署文档", "演示视频"],
            "success_criteria": ["项目功能完整", "代码质量高", "具备上线标准"]
        }]

    def _build_career_projects(self, skills: List[str], target: TargetPosition) -> List[Dict]:
        return [
            {
                "name": "个人作品集整理",
                "description": "整合所有学习项目成果为专业作品集",
                "difficulty": "中等",
                "estimated_hours": 15,
                "skills_covered": skills[:5],
                "deliverables": ["在线作品集网站", "项目README完善", "成果展示PPT"],
                "success_criteria": ["作品集专业美观", "至少包含3个完整项目"]
            },
            {
                "name": f"{target.title}模拟面试冲刺",
                "description": "系统整理面试知识点并进行模拟面试训练",
                "difficulty": "中等",
                "estimated_hours": 20,
                "skills_covered": skills,
                "deliverables": ["面试题集整理", "模拟面试记录", "个人面试话术"],
                "success_criteria": ["能流利回答80%以上面试题", "模拟面试评分达到B+"]
            }
        ]

    def _generate_weekly_schedule(
        self,
        phases: List[LearningPhase],
        total_weeks: int,
        user: UserProfile,
        target: TargetPosition
    ) -> Dict[int, Dict]:
        schedule: Dict[int, Dict] = {}
        week = 1
        available_hours = user.weekly_available_hours

        for phase in phases:
            for _ in range(phase.duration_weeks):
                tasks = []
                if phase.name == "基础奠基":
                    tasks = self._week_tasks_foundation(week, phase, available_hours)
                elif phase.name == "核心强化":
                    tasks = self._week_tasks_core(week, phase, available_hours)
                elif phase.name == "进阶突破":
                    tasks = self._week_tasks_advanced(week, phase, available_hours)
                elif phase.name == "求职冲刺":
                    tasks = self._week_tasks_career(week, phase, available_hours)

                schedule[week] = {
                    "phase": phase.name,
                    "week_number": week,
                    "planned_hours": available_hours,
                    "tasks": tasks,
                    "checkpoints": phase.checkpoints[:2]
                }
                week += 1

        return schedule

    def _week_tasks_foundation(self, week: int, phase: LearningPhase, hours: int) -> List[Dict]:
        skills = phase.skills_to_learn
        tasks = []
        daily_hours = max(1, hours // 7)
        for day_idx, day_name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day_idx < 5:
                skill = skills[day_idx % len(skills)] if skills else "基础学习"
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "学习",
                    "content": f"{skill} 理论学习与基础练习",
                    "resource": "官方文档 / 入门教程"
                })
            else:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "实践",
                    "content": "本周知识回顾与小项目实践",
                    "resource": "练习题 / 小型项目"
                })
        return tasks

    def _week_tasks_core(self, week: int, phase: LearningPhase, hours: int) -> List[Dict]:
        skills = phase.skills_to_learn
        tasks = []
        daily_hours = max(1, hours // 7)
        for day_idx, day_name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day_idx < 5:
                skill = skills[day_idx % len(skills)] if skills else "核心学习"
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "学习+编码",
                    "content": f"{skill} 深度学习与项目开发",
                    "resource": "官方文档 / 源码分析 / 实战项目"
                })
            elif day_idx == 5:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "总结",
                    "content": "代码审查与学习总结",
                    "resource": ""
                })
            else:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "拓展",
                    "content": "技术博客阅读 / 开源项目贡献",
                    "resource": "GitHub / 技术社区"
                })
        return tasks

    def _week_tasks_advanced(self, week: int, phase: LearningPhase, hours: int) -> List[Dict]:
        tasks = []
        daily_hours = max(1, hours // 7)
        for day_idx, day_name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day_idx < 5:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "综合开发",
                    "content": "综合项目开发 - 功能实现与优化",
                    "resource": "项目需求文档 / 技术文档"
                })
            elif day_idx == 5:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "复盘",
                    "content": "项目进度复盘与技术难点攻克",
                    "resource": ""
                })
            else:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "文档",
                    "content": "项目文档编写与成果整理",
                    "resource": ""
                })
        return tasks

    def _week_tasks_career(self, week: int, phase: LearningPhase, hours: int) -> List[Dict]:
        tasks = []
        daily_hours = max(1, hours // 7)
        for day_idx, day_name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day_idx < 3:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "面试准备",
                    "content": "技术面试题刷题与系统复习",
                    "resource": "LeetCode / 面试宝典"
                })
            elif day_idx < 5:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "简历优化",
                    "content": "简历投递与作品集优化",
                    "resource": "招聘平台 / 作品集工具"
                })
            else:
                tasks.append({
                    "day": day_name,
                    "hours": daily_hours,
                    "type": "模拟面试",
                    "content": "模拟面试与反馈改进",
                    "resource": "面试模拟平台 / 录音回放"
                })
        return tasks

    def _identify_risks(
        self,
        user: UserProfile,
        target: TargetPosition,
        gaps: List[SkillGap],
        total_weeks: int
    ) -> List[Dict]:
        risks: List[Dict] = []

        total_estimated_hours = sum(g.estimated_hours for g in gaps)
        available_hours = user.weekly_available_hours * total_weeks
        if total_estimated_hours > available_hours:
            risks.append({
                "type": "时间不足",
                "level": RiskLevel.HIGH.value,
                "description": f"技能学习预计需要 {total_estimated_hours} 小时，但可用时间仅 {available_hours} 小时",
                "mitigation": "优先学习关键技能，降低非核心技能的深度要求；考虑延长学习周期或增加每日投入时间",
                "affected_skills": [g.skill_name for g in gaps if g.is_critical]
            })

        hard_gaps = [g for g in gaps if g.gap_size >= 3]
        if hard_gaps:
            risks.append({
                "type": "技术难度",
                "level": RiskLevel.MEDIUM.value,
                "description": f"{', '.join(g.skill_name for g in hard_gaps)} 与当前水平差距较大",
                "mitigation": "增加基础铺垫环节，寻找导师指导，分阶段设定小目标",
                "affected_skills": [g.skill_name for g in hard_gaps]
            })

        if user.motivation_level < 5:
            risks.append({
                "type": "动力不足",
                "level": RiskLevel.HIGH.value,
                "description": f"当前自我评估动力水平为 {user.motivation_level}/10，存在中途放弃风险",
                "mitigation": "设置短期激励目标，加入学习社群互相监督，定期记录成就和进步",
                "affected_skills": []
            })

        if user.stress_tolerance < 4:
            risks.append({
                "type": "健康隐患",
                "level": RiskLevel.MEDIUM.value,
                "description": f"压力承受能力偏低 ({user.stress_tolerance}/10)，高强度学习可能导致倦怠",
                "mitigation": "合理安排休息时间，保持运动习惯，每周至少安排1天完全休息",
                "affected_skills": []
            })

        risks.append({
            "type": "资源可用性",
            "level": RiskLevel.LOW.value,
            "description": "学习资源获取、开发环境配置等因素可能影响学习进度",
            "mitigation": "提前准备学习资料清单，确认开发环境可正常使用，建议准备备用学习资源",
            "affected_skills": []
        })

        return risks

    def export_markdown(self, path: LearningPath, output_path: Optional[str] = None) -> str:
        lines: List[str] = []
        lines.append(f"# 🎯 ADLP 学习路径 - {path.user_profile.name}")
        lines.append("")
        lines.append(f"> 目标岗位：**{path.target_position.title}**  ")
        lines.append(f"> 总周期：**{path.total_weeks} 周**  ")
        lines.append(f"> 生成时间：{path.created_at}")
        lines.append("")

        lines.append("## 📋 阶段概览")
        lines.append("")
        lines.append("| 阶段 | 周数 | 技能 | 项目数 |")
        lines.append("|------|------|------|--------|")
        for phase in path.phases:
            lines.append(
                f"| {phase.name} | {phase.duration_weeks} | "
                f"{len(phase.skills_to_learn)} | {len(phase.projects)} |"
            )
        lines.append("")

        for phase in path.phases:
            lines.append(f"## 📐 {phase.name} 阶段（第 {phase.order} 阶段）")
            lines.append("")
            lines.append(f"**周期**：{phase.duration_weeks} 周")
            lines.append("")
            lines.append("### 🎯 学习目标")
            for goal in phase.goals:
                lines.append(f"- {goal}")
            lines.append("")
            lines.append("### 📚 学习技能")
            for skill in phase.skills_to_learn:
                lines.append(f"- {skill}")
            lines.append("")
            lines.append("### 🚀 项目任务")
            for proj in phase.projects:
                lines.append(f"#### {proj.get('name', '未命名项目')}")
                lines.append(f"- **描述**：{proj.get('description', '')}")
                lines.append(f"- **难度**：{proj.get('difficulty', '')}")
                lines.append(f"- **预计时长**：{proj.get('estimated_hours', 0)} 小时")
                deliver = proj.get('deliverables', [])
                if deliver:
                    lines.append(f"- **交付物**：{'、'.join(deliver)}")
                criteria = proj.get('success_criteria', [])
                if criteria:
                    lines.append(f"- **成功标准**：{'；'.join(criteria)}")
                lines.append("")
            lines.append("### ✅ 检查点")
            for cp in phase.checkpoints:
                lines.append(f"- {cp}")
            lines.append("")

        lines.append("## ⚠️ 风险提示")
        lines.append("")
        for risk in path.risks:
            lines.append(f"### {risk['type']}（{risk['level']}）")
            lines.append(f"- **描述**：{risk['description']}")
            lines.append(f"- **缓解措施**：{risk['mitigation']}")
            lines.append("")

        lines.append("## 📅 周度计划")
        lines.append("")
        for week_num in sorted(path.weekly_schedule.keys()):
            week_data = path.weekly_schedule[week_num]
            lines.append(f"### 第 {week_num} 周 - {week_data.get('phase', '')}")
            for task in week_data.get('tasks', []):
                lines.append(f"- **{task.get('day', '')}**（{task.get('hours', 0)}h）：{task.get('content', '')}")
            lines.append("")

        md_content = "\n".join(lines)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md_content, encoding="utf-8")

        return md_content

    def export_json(self, path: LearningPath, output_path: Optional[str] = None) -> str:
        def _convert(obj):
            if hasattr(obj, '__dataclass_fields__'):
                result = {}
                for f_name in obj.__dataclass_fields__:
                    value = getattr(obj, f_name)
                    if hasattr(value, 'value'):
                        value = value.value
                    result[f_name] = _convert(value)
                return result
            elif isinstance(obj, (list, tuple)):
                return [_convert(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): _convert(v) for k, v in obj.items()}
            elif isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return obj

        j = json.dumps(_convert(path), ensure_ascii=False, indent=2)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(j, encoding="utf-8")

        return j

    def adjust_path(self, path: LearningPath, actual_progress: float) -> LearningPath:
        if actual_progress <= 0 or actual_progress > 1:
            actual_progress = max(0.01, min(1.0, actual_progress))

        remaining_weeks = math.ceil(path.total_weeks * (1 - actual_progress))
        if remaining_weeks < 1:
            remaining_weeks = 1

        new_phases: List[LearningPhase] = []
        passed_weeks = path.total_weeks - remaining_weeks

        for phase in path.phases:
            proportion = phase.duration_weeks / path.total_weeks
            completed_weeks = max(0, phase.duration_weeks - math.ceil(remaining_weeks * proportion))
            remaining_phase_weeks = max(1, math.ceil(remaining_weeks * proportion))

            adjusted_phase = LearningPhase(
                name=f"{phase.name}（已调整）",
                order=phase.order,
                duration_weeks=remaining_phase_weeks,
                goals=[f"[加速] {g}" for g in phase.goals],
                skills_to_learn=phase.skills_to_learn,
                projects=[{**p, "estimated_hours": max(4, p.get("estimated_hours", 10) // 2)}
                          for p in phase.projects],
                resources=phase.resources,
                checkpoints=[f"[调整] {c}" for c in phase.checkpoints],
                success_criteria=phase.success_criteria
            )
            new_phases.append(adjusted_phase)

        adjusted_path = LearningPath(
            target_position=path.target_position,
            user_profile=path.user_profile,
            phases=new_phases,
            total_weeks=path.total_weeks,
            weekly_schedule=path.weekly_schedule,
            risks=[
                {**r, "description": f"[已调整进度 {actual_progress:.0%}] {r['description']}"}
                if r.get("type") == "时间不足" else r
                for r in path.risks
            ],
            created_at=datetime.now().isoformat()
        )

        return adjusted_path
