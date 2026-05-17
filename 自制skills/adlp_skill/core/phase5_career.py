"""ADLP 阶段五：产出导向的求职准备"""

from datetime import datetime
from typing import List, Dict, Optional

from .models import UserProfile, TargetPosition, LearningPath, ProgressRecord, Skill, SkillLevel


class CareerPreparer:

    def __init__(self, config: dict):
        self.config = config

    def prepare(
        self,
        user: UserProfile,
        target: TargetPosition,
        path: Optional[LearningPath],
        records: List[ProgressRecord]
    ) -> Dict:
        projects: List[Dict] = []
        skills_learned: List[str] = []

        if path:
            for phase in path.phases:
                for proj in phase.projects:
                    projects.append(proj)
                for skill in phase.skills_to_learn:
                    if skill not in skills_learned:
                        skills_learned.append(skill)

        total_hours = sum(r.hours_spent for r in records)

        portfolio = self._build_portfolio(user, target, projects, skills_learned)
        resume = self._build_resume_inline(user, target, projects)
        interview = self._build_interview_inline(target, skills_learned)
        strategy = self._build_strategy_inline(target, user)

        return {
            "portfolio": portfolio,
            "resume": resume,
            "interview": interview,
            "strategy": strategy,
            "summary": {
                "user_name": user.name,
                "target_position": target.title,
                "total_learning_hours": total_hours,
                "skills_count": len(skills_learned),
                "projects_count": len(projects),
                "generated_at": datetime.now().isoformat()
            }
        }

    def _build_portfolio(
        self,
        user: UserProfile,
        target: TargetPosition,
        projects: List[Dict],
        skills: List[str]
    ) -> Dict:
        return {
            "personal_brand": {
                "suggested_title": f"{target.title}工程师",
                "tagline": f"从{user.current_role}转行{target.title}",
                "github_optimization": [
                    "完善 GitHub Profile README，展示技术栈和核心项目",
                    "为每个项目编写清晰的 README（含架构图、Demo链接、快速开始指南）",
                    "保持 commit 记录活跃，体现学习成长曲线",
                    "Star 相关领域优质开源项目并参与讨论"
                ],
                "blog_suggestions": [
                    f"《我是如何从零开始学习{skills[0] if skills else '编程'}的》",
                    f"《{target.title}入门路线与避坑指南》",
                    "《从项目实战中总结的N条经验》",
                    f"《{target.title}面试常见问题与解答》"
                ]
            },
            "project_showcase": {
                "recommended_order": [p.get("name", "") for p in projects],
                "presentation_tips": [
                    "每个项目用 STAR 法则描述（情境、任务、行动、结果）",
                    "附上在线 Demo 链接或截图",
                    "列出技术栈标签便于招聘方快速识别",
                    "突出个人贡献和解决的难点"
                ]
            },
            "online_presence": {
                "platforms": ["GitHub", "掘金", "知乎", "LinkedIn"],
                "content_calendar": [
                    "第1周：发布第一篇学习总结文章",
                    "第3周：发布一个项目复盘",
                    "持续参与技术社区讨论，每周至少回答2个问题"
                ]
            }
        }

    def build_resume(
        self,
        user: UserProfile,
        target: TargetPosition,
        projects: Optional[List[Dict]] = None
    ) -> str:
        return self._build_resume_inline(user, target, projects or [])

    def _build_resume_inline(
        self,
        user: UserProfile,
        target: TargetPosition,
        projects: List[Dict]
    ) -> str:
        lines: List[str] = []
        lines.append(f"# {user.name}")
        lines.append("")
        lines.append(f"📧 邮箱：your_email@example.com　|　📱 电话：138xxxx8888")
        lines.append(f"🎯 求职意向：{target.title}　|　📍 期望城市：北京/上海/深圳")
        lines.append(f"💼 工作经验：{user.experience_years} 年　|　🎓 学历：{user.education}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 💡 专业技能")
        lines.append("")

        all_required = target.required_skills or []
        all_preferred = target.preferred_skills or []
        all_skills = [s.name for s in (all_required + all_preferred)]

        if all_skills:
            lines.append(f"- **核心技术**：{'、'.join(all_skills[:6])}")
        if len(all_skills) > 6:
            lines.append(f"- **其他技能**：{'、'.join(all_skills[6:])}")
        lines.append(f"- **开发工具**：Git、VS Code、Docker、CI/CD")
        lines.append(f"- **语言能力**：英语（读写熟练）、普通话（母语）")
        lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 🚀 项目经验")
        lines.append("")

        for idx, proj in enumerate(projects, 1):
            name = proj.get("name", f"项目{idx}")
            desc = proj.get("description", "")
            skills_used = proj.get("skills_covered", [])
            deliverables = proj.get("deliverables", [])
            lines.append(f"### {name}")
            lines.append(f"**技术栈**：{'、'.join(skills_used)}")
            lines.append("")
            lines.append(f"**项目描述**：{desc}")
            lines.append("")
            if deliverables:
                lines.append(f"**主要成果**：")
                for d in deliverables:
                    lines.append(f"- {d}")
            lines.append(f"**个人贡献**：独立完成项目的需求分析、技术方案设计、核心功能开发与上线部署")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 💼 工作经历")
        lines.append("")
        lines.append(f"### {user.current_role}")
        lines.append(f"**{user.background}**")
        lines.append("")
        lines.append(f"- 拥有 {user.experience_years} 年工作经验，具备良好的沟通协作和问题解决能力")
        lines.append(f"- 自主学习能力强，已完成 {target.title} 相关技能的系统学习和项目实践")
        lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 🎓 教育背景")
        lines.append("")
        lines.append(f"- **{user.education}** | 计算机/软件工程相关专业")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🏆 自我评价")
        lines.append("")
        lines.append(f"- 拥有扎实的{target.title}技术基础，具备独立开发和解决问题的能力")
        lines.append(f"- 坚持通过项目驱动的方式学习，积累了丰富的实战经验")
        lines.append(f"- 有较强的自驱力和学习能力，能够快速适应新技术和团队协作")
        lines.append("")

        return "\n".join(lines)

    def prepare_interview(
        self,
        target: TargetPosition,
        tech_stack: Optional[List[str]] = None
    ) -> Dict:
        skills = tech_stack or [s.name for s in target.required_skills + target.preferred_skills]
        return self._build_interview_inline(target, skills)

    def _build_interview_inline(
        self,
        target: TargetPosition,
        skills: List[str]
    ) -> Dict:
        return {
            "技术基础": {
                "description": "考察计算机基础知识和核心技能掌握程度",
                "questions": [
                    {
                        "question": f"请介绍你对 {'、'.join(skills[:2]) if skills else '核心技术栈'} 的理解",
                        "tips": "从概念定义、核心原理、实际应用三个层次回答，结合项目经验举例"
                    },
                    {
                        "question": f"在项目中遇到的最大的技术挑战是什么？你是如何解决的？",
                        "tips": "使用STAR法则，突出分析过程和解决问题的思路"
                    },
                    {
                        "question": "请解释你在项目中用到的核心设计模式及其应用场景",
                        "tips": "选择2-3个最熟悉的模式，说明为什么选择它以及带来的收益"
                    },
                    {
                        "question": "如何进行代码质量管理和技术债务控制？",
                        "tips": "提及代码审查、自动化测试、重构策略等实践"
                    }
                ]
            },
            "项目经验": {
                "description": "深入考察项目实战能力和问题解决经验",
                "questions": [
                    {
                        "question": "请详细介绍你最有成就感的项目，包括架构设计和关键决策",
                        "tips": "准备架构图（白板画出），说明技术选型理由，数据流设计"
                    },
                    {
                        "question": "项目中如何处理性能瓶颈？请举例说明",
                        "tips": "从发现问题→定位原因→多种方案对比→最终实施→效果验证完整描述"
                    },
                    {
                        "question": "如果重新做这个项目，你会做出哪些不同的决策？",
                        "tips": "展示反思能力和成长思维，诚实分析不足之处"
                    }
                ]
            },
            "系统设计": {
                "description": "考察系统架构设计和方案评估能力",
                "questions": [
                    {
                        "question": f"设计一个{target.title}相关的核心系统，请描述你的设计思路",
                        "tips": "从需求分析→系统架构→模块设计→数据流→扩展性考虑，展现系统性思维"
                    },
                    {
                        "question": "如何处理系统的高可用和高并发？",
                        "tips": "从负载均衡、缓存策略、数据库优化、服务降级等维度回答"
                    },
                    {
                        "question": "设计一个完整的CI/CD流水线，需要考虑哪些方面？",
                        "tips": "覆盖代码管理、构建、测试、部署、监控各环节"
                    }
                ]
            },
            "行为面试": {
                "description": "考察软技能和文化匹配度",
                "questions": [
                    {
                        "question": "为什么想从原岗位转到 {target.title} 领域？",
                        "tips": "展现真实的动机、长期的职业规划和对行业的热情"
                    },
                    {
                        "question": "分享一次你克服困难完成目标的经历",
                        "tips": "用具体的例子展示毅力、学习能力和解决问题的方法"
                    },
                    {
                        "question": "你如何保持技术学习的持续性和深度？",
                        "tips": "说明学习方法论、学习资源获取渠道和时间管理策略"
                    },
                    {
                        "question": "在团队协作中如何处理分歧？请举例",
                        "tips": "表现沟通能力、同理心和以结果为导向的合作态度"
                    }
                ]
            },
            "薪资谈判": {
                "description": "薪资谈判策略和话术准备",
                "questions": [
                    {
                        "question": "你对薪资的期望是多少？",
                        "tips": f"提前调研 {target.title} 的市场薪资范围（{target.avg_salary_range[0]/10000:.1f}万-{target.avg_salary_range[1]/10000:.1f}万/月），给出合理区间而非固定数字"
                    },
                    {
                        "question": "除了薪资还看重哪些方面？",
                        "tips": "提及技术成长空间、团队文化、业务方向、工作生活平衡等"
                    },
                    {
                        "question": "如果收到多个offer，你的选择标准是什么？",
                        "tips": "展现成熟的职业价值观，避免单一关注薪资"
                    }
                ]
            }
        }

    def suggest_continuous_learning(
        self,
        user: UserProfile,
        target: TargetPosition
    ) -> Dict:
        required_names = [s.name for s in target.required_skills]
        preferred_names = [s.name for s in target.preferred_skills]
        all_target_skills = required_names + preferred_names

        depth_path: List[Dict] = []
        for skill_name in all_target_skills[:3]:
            depth_path.append({
                "skill": skill_name,
                "current_focus": "熟练应用",
                "next_milestone": "精通原理",
                "future_milestone": "贡献开源/发表文章",
                "suggested_resources": [
                    f"{skill_name} 官方源码阅读",
                    f"{skill_name} 高级编程书籍",
                    "相关技术会议和论文"
                ]
            })

        breadth_path: List[Dict] = []
        adjacent_skills = ["系统设计", "性能优化", "安全编程", "云原生", "AI/ML基础"]
        for skill in adjacent_skills:
            breadth_path.append({
                "skill": skill,
                "relevance_to_target": f"拓展{target.title}工程师的能力边界",
                "suggested_resources": [
                    f"{skill} 入门课程",
                    f"{skill} 实战项目"
                ],
                "estimated_months": 2
            })

        community = {
            "online_communities": [
                {"name": "GitHub", "activity": "Star优质项目, 提Issue/PR, 维护个人项目"},
                {"name": "Stack Overflow", "activity": "每周回答2-5个技术问题"},
                {"name": "掘金/知乎", "activity": "每月发布1-2篇技术文章"},
                {"name": "技术社区（如V2EX）", "activity": "参与行业讨论，建立专业人脉"}
            ],
            "offline_activities": [
                "参加本地的技术Meetup和技术大会",
                "主动在团队内部做技术分享",
                "报名参加 Hackathon 锻炼实战能力"
            ]
        }

        certifications = []
        for cert_name, relevance in [
            ("AWS/Azure/GCP 云认证", "云计算是现代技术栈的基础设施"),
            ("PMP/ACP 项目管理认证", "提升项目管理和团队协作能力"),
            ("对应技术栈的官方认证", f"增强{target.title}领域的专业可信度"),
        ]:
            certifications.append({
                "name": cert_name,
                "relevance": relevance,
                "time_investment": "3-6个月",
                "priority": "中等" if "云" not in cert_name else "高"
            })

        return {
            "depth_path": depth_path,
            "breadth_path": breadth_path,
            "community_involvement": community,
            "certification_recommendations": certifications,
            "one_year_roadmap": {
                "Q1": "巩固入职后的核心技能，快速适应团队技术栈",
                "Q2": "开始深度方向探索，选择1个技术领域深耕",
                "Q3": "横向拓展1-2个相邻技能，参加技术大会",
                "Q4": "整理年度成果，争取晋升/跳槽更优机会"
            },
            "three_year_vision": {
                "technical": "成为团队中的技术骨干，具备架构设计和技术决策能力",
                "influence": "在技术社区建立个人品牌，定期输出高质量内容",
                "career": f"晋升为高级{target.title}工程师或技术负责人"
            }
        }

    def generate_job_search_strategy(self, target: TargetPosition) -> Dict:
        return self._build_strategy_inline(target, UserProfile(
            name="",
            background="",
            current_role=""
        ))

    def _build_strategy_inline(
        self,
        target: TargetPosition,
        user: UserProfile
    ) -> Dict:
        return {
            "channels": [
                {
                    "name": "BOSS直聘/拉勾",
                    "type": "主动投递",
                    "priority": "高",
                    "strategy": "每天主动联系10-15家目标公司，使用个性化招呼语",
                    "tips": "优化在线简历关键词，提升被搜索率"
                },
                {
                    "name": "LinkedIn/脉脉",
                    "type": "人脉推荐",
                    "priority": "高",
                    "strategy": "完善个人资料，添加目标公司HR和技术负责人",
                    "tips": "定期发布技术内容，展示专业度"
                },
                {
                    "name": "企业官网/内推",
                    "type": "精准投递",
                    "priority": "中",
                    "strategy": "直接访问目标公司招聘页面投递，寻找内部员工内推",
                    "tips": "内推可以显著提升简历通过率"
                },
                {
                    "name": "猎头渠道",
                    "type": "被动招聘",
                    "priority": "中",
                    "strategy": "保持LinkedIn资料更新，等待猎头联系",
                    "tips": "明确表达职业方向和期望"
                },
                {
                    "name": "技术社区/线下活动",
                    "type": "社交求职",
                    "priority": "低",
                    "strategy": "参加行业活动结识业内人士，了解隐性岗位机会",
                    "tips": "准备简洁的自我介绍（电梯演讲）"
                }
            ],
            "timeline": {
                "第1-2周": [
                    "完成简历定稿和作品集上线",
                    "在各招聘平台完善个人资料",
                    "开始投递非首选公司练手"
                ],
                "第3-4周": [
                    "根据反馈优化简历和面试表现",
                    "向目标公司发起投递",
                    "安排模拟面试巩固弱项"
                ],
                "第5-6周": [
                    "进入密集面试阶段",
                    "记录每次面试问题并复盘",
                    "开始收到offer并进行比较"
                ],
                "第7-8周": [
                    "进入薪资谈判阶段",
                    "综合评估offer并做出决策",
                    "准备入职材料"
                ]
            },
            "target_companies": {
                "tier1_top": {
                    "description": "行业头部公司，竞争激烈但回报丰厚",
                    "examples": self._get_company_examples(target, "top"),
                    "application_strategy": "准备充分后再投递，争取内推机会"
                },
                "tier2_growth": {
                    "description": "快速成长的独角兽/中等规模公司",
                    "examples": self._get_company_examples(target, "mid"),
                    "application_strategy": "重点关注技术和业务匹配度"
                },
                "tier3_startup": {
                    "description": "创业公司，适合快速成长",
                    "examples": self._get_company_examples(target, "startup"),
                    "application_strategy": "关注公司发展阶段和团队背景"
                }
            },
            "salary_negotiation": {
                "target_salary_range": f"{target.avg_salary_range[0]/10000:.1f}万 - {target.avg_salary_range[1]/10000:.1f}万/月",
                "negotiation_tips": [
                    "先让对方出价，避免先暴露底牌",
                    "强调自身价值和项目成果，而非工作经验年限",
                    "考虑总包而非仅看月薪（期权、年终、福利等）",
                    "有多个offer时合理竞争，但要保持诚信"
                ]
            },
            "kpi_metrics": {
                "简历投递数": "50-100份（前2周广泛投递）",
                "面试邀约率": "目标10-20%",
                "一面通过率": "目标50%以上",
                "最终offer数": "目标获得2-3个可比较的offer",
                "求职周期": "预计4-8周"
            }
        }

    def _get_company_examples(self, target: TargetPosition, tier: str) -> List[str]:
        industry = target.industry
        if tier == "top":
            if "互联网" in industry:
                return ["字节跳动", "阿里巴巴", "腾讯", "美团", "百度"]
            elif "金融" in industry:
                return ["蚂蚁集团", "微众银行", "招商银行科技", "中国平安科技"]
            else:
                return ["华为", "字节跳动", "阿里巴巴", "腾讯"]
        elif tier == "mid":
            return ["小红书", "B站", "快手", "得物", "米哈游"]
        else:
            return ["各类A轮到C轮的创业公司", "垂直领域技术服务商"]
