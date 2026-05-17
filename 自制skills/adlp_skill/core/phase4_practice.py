"""ADLP 阶段四：项目驱动实践学习"""

from datetime import datetime
from typing import List, Dict

from .models import LearningPath, ProgressRecord, LearningPhase


class ProjectPracticeManager:

    def __init__(self, config: dict):
        self.config = config
        self._tier_configs = [
            ("入门实战", 1, 2, "入门"),
            ("核心项目", 2, 3, "中等"),
            ("综合挑战", 1, 2, "困难"),
            ("展示作品", 1, 1, "中等"),
        ]

    def generate_project_ladder(self, path: LearningPath) -> List[Dict]:
        all_skills: List[str] = []
        for phase in path.phases:
            for skill in phase.skills_to_learn:
                if skill not in all_skills:
                    all_skills.append(skill)

        target_title = path.target_position.title
        ladder: List[Dict] = []

        for tier_name, min_count, max_count, difficulty in self._tier_configs:
            projects_in_tier: List[Dict] = []

            if tier_name == "入门实战":
                for i in range(min_count):
                    skill = all_skills[i % len(all_skills)] if all_skills else "基础编程"
                    projects_in_tier.append({
                        "tier": tier_name,
                        "name": f"{skill}入门练习项目",
                        "description": f"通过小型项目熟悉 {skill} 的基本用法和最佳实践",
                        "difficulty": difficulty,
                        "estimated_hours": 8,
                        "skills_covered": [skill],
                        "deliverables": [f"可运行的 {skill} 练习代码", "学习笔记与踩坑记录"],
                        "success_criteria": [
                            "代码能正常运行并产生预期结果",
                            "理解核心API和基本概念",
                            "完成至少2个基础功能的实现"
                        ]
                    })

            elif tier_name == "核心项目":
                for i in range(min_count):
                    skill_slice = all_skills[i*2:(i+1)*2] if len(all_skills) >= (i+1)*2 else all_skills[i:]
                    if not skill_slice:
                        skill_slice = all_skills[:1]
                    projects_in_tier.append({
                        "tier": tier_name,
                        "name": f"{target_title}核心功能模块 #{i+1}",
                        "description": f"综合运用 {'、'.join(skill_slice)} 开发{target_title}的核心功能模块",
                        "difficulty": difficulty,
                        "estimated_hours": 20,
                        "skills_covered": skill_slice,
                        "deliverables": [
                            "完整的功能模块源码",
                            "单元测试代码",
                            "模块使用文档"
                        ],
                        "success_criteria": [
                            "模块功能完整且通过单元测试",
                            "代码结构清晰，注释规范",
                            "文档清晰可读"
                        ]
                    })

            elif tier_name == "综合挑战":
                all_skills_slice = all_skills[:6] if len(all_skills) >= 6 else all_skills
                for i in range(min_count):
                    projects_in_tier.append({
                        "tier": tier_name,
                        "name": f"{target_title}端到端综合项目",
                        "description": f"从零开始构建一个完整的{target_title}应用，覆盖全栈技能",
                        "difficulty": difficulty,
                        "estimated_hours": 40,
                        "skills_covered": all_skills_slice,
                        "deliverables": [
                            "完整项目源码（GitHub仓库）",
                            "架构设计与技术方案文档",
                            "部署上线链接",
                            "项目演示视频"
                        ],
                        "success_criteria": [
                            "项目功能完整，可以上线运行",
                            "代码质量达到生产级标准",
                            "具备完整的CI/CD流程",
                            "能作为面试作品展示"
                        ]
                    })

            elif tier_name == "展示作品":
                projects_in_tier.append({
                    "tier": tier_name,
                    "name": "个人技术品牌展示页",
                    "description": "打造专业的个人技术作品集，展示所有项目成果",
                    "difficulty": difficulty,
                    "estimated_hours": 20,
                    "skills_covered": ["HTML/CSS", "前端框架", "文档写作"],
                    "deliverables": [
                        "个人作品集网站（在线可访问）",
                        "GitHub Profile README优化",
                        "项目成果展示PPT",
                        "技术博客（至少2篇）"
                    ],
                    "success_criteria": [
                        "作品集页面专业美观",
                        "所有核心项目都有完善的README",
                        "至少发布2篇高质量技术文章",
                        "简历中可引用的项目成果"
                    ]
                })

            ladder.extend(projects_in_tier)

        return ladder

    def create_weekly_plan(self, path: LearningPath, week: int) -> Dict:
        if week not in path.weekly_schedule:
            return {
                "week": week,
                "error": f"未找到第 {week} 周的日程安排",
                "total_planned_hours": 0,
                "daily_breakdown": []
            }

        week_data = path.weekly_schedule[week]
        daily_breakdown: List[Dict] = []

        for task in week_data.get("tasks", []):
            daily_breakdown.append({
                "day": task.get("day", ""),
                "hours": task.get("hours", 0),
                "type": task.get("type", "学习"),
                "content": task.get("content", ""),
                "resource": task.get("resource", ""),
                "checklist": self._generate_daily_checklist(task)
            })

        current_phase = week_data.get("phase", "")
        phase_detail = None
        for phase in path.phases:
            if phase.name == current_phase:
                phase_detail = {
                    "name": phase.name,
                    "goals": phase.goals,
                    "skills_to_learn": phase.skills_to_learn,
                    "projects": phase.projects,
                    "checkpoints": phase.checkpoints
                }
                break

        return {
            "week": week,
            "phase": current_phase,
            "phase_detail": phase_detail,
            "total_planned_hours": week_data.get("planned_hours", 0),
            "daily_breakdown": daily_breakdown,
            "week_checkpoints": week_data.get("checkpoints", []),
            "weekly_goals": phase_detail["goals"] if phase_detail else [],
            "tips": self._generate_weekly_tips(week, current_phase)
        }

    def _generate_daily_checklist(self, task: Dict) -> List[str]:
        task_type = task.get("type", "")
        if "学习" in task_type:
            return [
                "完成理论学习内容并做笔记",
                "动手练习至少1个代码示例",
                "记录学习中的疑问"
            ]
        elif "编码" in task_type or "开发" in task_type:
            return [
                "明确今日要完成的开发目标",
                "编写代码并提交到版本控制",
                "编写或更新对应测试用例"
            ]
        elif "总结" in task_type or "复盘" in task_type:
            return [
                "回顾本周学习成果",
                "整理遗留问题和解决方案",
                "规划下周学习重点"
            ]
        elif "面试" in task_type:
            return [
                "完成至少3道算法/设计题",
                "整理答题思路和要点",
                "模拟回答并录音自评"
            ]
        elif "简历" in task_type:
            return [
                "更新简历对应模块",
                "针对1个目标岗位调整简历",
                "检查简历关键词匹配度"
            ]
        else:
            return [
                "设定今日目标",
                "完成主要任务",
                "记录完成情况和心得"
            ]

    def _generate_weekly_tips(self, week: int, phase_name: str) -> List[str]:
        tips: List[str] = []
        if week == 1:
            tips.append("制定固定的每日学习时间，建立学习习惯")
            tips.append("准备好开发环境和学习资料")
        if week % 2 == 0:
            tips.append("本周安排一次知识回顾，巩固已学内容")
        if week % 4 == 0:
            tips.append("进行阶段性自测，评估学习效果")
        if "基础" in phase_name:
            tips.append("打好基础是关键，不要急于求成")
        if "核心" in phase_name:
            tips.append("注重理论与实践结合，每学一个概念都要动手验证")
        if "进阶" in phase_name:
            tips.append("尝试阅读优秀开源项目源码，学习架构思路")
        if "求职" in phase_name:
            tips.append("模拟面试环境，提前适应面试节奏")
        tips.append("保持规律的作息，保证充足的休息时间")
        return tips

    def generate_report(self, path: LearningPath, records: List[ProgressRecord]) -> str:
        if not records:
            return "暂无学习记录，无法生成报告。"

        total_hours = sum(r.hours_spent for r in records)
        completed_projects: List[str] = []
        all_challenges: List[str] = []
        mood_scores: List[int] = []

        for r in records:
            completed_projects.extend(r.projects_completed)
            all_challenges.extend(r.challenges)
            mood_scores.append(r.mood_score)

        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else 0
        latest_record = records[-1]
        weeks_completed = max(r.week_number for r in records)

        unique_projects = list(dict.fromkeys(completed_projects))

        lines: List[str] = []
        lines.append(f"# 📊 学习进度报告")
        lines.append("")
        lines.append(f"**报告时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**学习者**：{path.user_profile.name}")
        lines.append(f"**目标岗位**：{path.target_position.title}")
        lines.append("")
        lines.append("## 📈 总体概览")
        lines.append("")
        lines.append(f"- **已完成周数**：{weeks_completed} / {path.total_weeks}")
        lines.append(f"- **累计学习时长**：{total_hours:.1f} 小时")
        lines.append(f"- **已完成项目数**：{len(unique_projects)} 个")
        lines.append(f"- **平均心情评分**：{avg_mood:.1f} / 10")
        lines.append(f"- **学习进度**：{weeks_completed / path.total_weeks * 100:.1f}%")
        lines.append("")

        if unique_projects:
            lines.append("## ✅ 已完成项目")
            lines.append("")
            for proj in unique_projects:
                lines.append(f"- {proj}")
            lines.append("")

        if all_challenges:
            lines.append("## ⚠️ 遇到的挑战")
            lines.append("")
            seen_challenges: List[str] = []
            for c in all_challenges:
                if c not in seen_challenges:
                    seen_challenges.append(c)
                    lines.append(f"- {c}")
            lines.append("")

        lines.append("## 📝 最近记录")
        lines.append("")
        lines.append(f"- **日期**：{latest_record.date}")
        lines.append(f"- **本周时长**：{latest_record.hours_spent:.1f} 小时")
        lines.append(f"- **练习技能**：{'、'.join(latest_record.skills_practiced) if latest_record.skills_practiced else '无'}")
        lines.append(f"- **成就**：{'、'.join(latest_record.achievements) if latest_record.achievements else '无'}")
        lines.append(f"- **心情评分**：{latest_record.mood_score} / 10")
        if latest_record.next_week_plan:
            lines.append(f"- **下周计划**：{latest_record.next_week_plan}")
        if latest_record.notes:
            lines.append(f"- **备注**：{latest_record.notes}")
        lines.append("")

        lines.append("## 💡 建议")
        lines.append("")
        if avg_mood < 5:
            lines.append("- ⚠️ 近期心情评分偏低，建议适当降低学习强度，增加休息时间")
        if weeks_completed / path.total_weeks < 0.5:
            lines.append("- 📌 处于学习前期阶段，保持当前节奏，逐步建立知识体系")
        else:
            lines.append("- 🎯 已进入学习后期阶段，建议开始关注求职准备和项目整理")
        if total_hours / max(1, weeks_completed) < 10:
            lines.append("- ⚡ 每周学习时长偏低，建议适当增加投入时间以确保按时完成计划")

        return "\n".join(lines)

    def suggest_adjustment(
        self,
        path: LearningPath,
        current_week: int,
        actual_hours: float,
        planned_hours: float
    ) -> Dict:
        deviation = (actual_hours - planned_hours) / planned_hours if planned_hours > 0 else 0
        remaining_weeks = max(1, path.total_weeks - current_week)

        suggestion: Dict = {
            "current_week": current_week,
            "remaining_weeks": remaining_weeks,
            "actual_hours": actual_hours,
            "planned_hours": planned_hours,
            "deviation": round(deviation, 2),
            "status": "on_track",
            "severity": "low",
            "recommendations": [],
            "adjusted_schedule": {}
        }

        if deviation < -0.3:
            suggestion["status"] = "falling_behind"
            suggestion["severity"] = "high"
            suggestion["recommendations"] = [
                "当前学习进度严重落后于计划，需立即调整策略",
                "重新评估技能优先级，暂时搁置非核心技能",
                f"建议将每周学习时间从 {planned_hours} 小时提升至 {planned_hours * 1.3:.0f} 小时",
                "考虑延长学习周期或申请学习假期",
                "将部分项目从「开发」降级为「阅读源码+笔记」以减少时间投入"
            ]
            suggestion["adjusted_schedule"] = {
                "recommended_daily_hours": round(planned_hours * 1.3 / 7, 1),
                "focus_skills": self._get_critical_skills(path),
                "skip_if_needed": self._get_non_critical_skills(path)
            }

        elif deviation < -0.1:
            suggestion["status"] = "slightly_behind"
            suggestion["severity"] = "medium"
            suggestion["recommendations"] = [
                f"学习进度略慢于计划，偏差约 {abs(deviation)*100:.0f}%",
                "适当压缩周末休息时间用于赶进度",
                "识别当前阶段哪些任务可以加速完成",
                "检查是否存在分心或效率低下的情况"
            ]
            suggestion["adjusted_schedule"] = {
                "recommended_daily_hours": round(planned_hours * 1.15 / 7, 1),
                "focus_skills": self._get_critical_skills(path),
                "skip_if_needed": []
            }

        elif deviation < 0.1:
            suggestion["status"] = "on_track"
            suggestion["severity"] = "low"
            suggestion["recommendations"] = [
                "当前学习进度与计划基本一致，继续保持",
                "可以在完成计划任务后适当拓展学习深度",
                "建议每周保留1-2小时用于技术前沿探索"
            ]

        elif deviation <= 0.3:
            suggestion["status"] = "slightly_ahead"
            suggestion["severity"] = "low"
            suggestion["recommendations"] = [
                f"当前学习进度超前于计划，领先约 {deviation*100:.0f}%",
                "可以利用富余时间深化已学技能",
                "开始准备下一阶段的学习资料",
                "考虑增加可选项目以拓展能力边界"
            ]

        else:
            suggestion["status"] = "significantly_ahead"
            suggestion["severity"] = "medium"
            suggestion["recommendations"] = [
                f"学习进度显著超前，领先约 {deviation*100:.0f}%",
                "审视是否有跳步学习导致基础不牢的风险",
                "建议用额外时间做知识深挖和横向拓展",
                "可以提前进入求职准备阶段"
            ]

        suggestion["adjusted_total_weeks"] = self._recalculate_weeks(
            path.total_weeks, current_week, actual_hours, planned_hours
        )

        return suggestion

    def _get_critical_skills(self, path: LearningPath) -> List[str]:
        for phase in path.phases:
            if phase.order == 2:
                return phase.skills_to_learn[:3]
        all_skills: List[str] = []
        for phase in path.phases:
            all_skills.extend(phase.skills_to_learn[:2])
        return all_skills[:4]

    def _get_non_critical_skills(self, path: LearningPath) -> List[str]:
        all_skills: List[str] = []
        for phase in path.phases:
            all_skills.extend(phase.skills_to_learn)
        critical = set(self._get_critical_skills(path))
        return [s for s in all_skills[-4:] if s not in critical]

    def _recalculate_weeks(
        self,
        total_weeks: int,
        current_week: int,
        actual_hours: float,
        planned_hours: float
    ) -> int:
        if actual_hours <= 0 or planned_hours <= 0:
            return total_weeks
        efficiency = actual_hours / planned_hours
        remaining = total_weeks - current_week
        adjusted_remaining = max(1, round(remaining / efficiency))
        return current_week + adjusted_remaining
