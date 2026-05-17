import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

from .models import MarketData, TargetPosition, Skill, SkillLevel

BUILTIN_POSITIONS: Dict[str, Dict[str, Any]] = {
    "AI工程师": {
        "avg_salary": 35000,
        "total_jobs": 8500,
        "skills": ["Python", "ML", "DL", "PyTorch", "TensorFlow"],
        "entry_barrier": "中等",
        "growth_outlook": "高",
        "top_companies": ["字节跳动", "腾讯", "阿里巴巴", "百度", "华为"],
        "experience_distribution": {"应届": 15, "1-3年": 35, "3-5年": 30, "5-10年": 15, "10年+": 5},
        "education_distribution": {"本科": 55, "硕士": 35, "博士": 5, "大专": 5},
        "city_distribution": {"北京": 30, "上海": 25, "深圳": 20, "杭州": 15, "其他": 10},
    },
    "机器学习工程师": {
        "avg_salary": 45000,
        "total_jobs": 6200,
        "skills": ["Python", "ML", "数据挖掘", "SQL", "统计学"],
        "entry_barrier": "较高",
        "growth_outlook": "高",
        "top_companies": ["字节跳动", "阿里巴巴", "腾讯", "美团", "京东"],
        "experience_distribution": {"应届": 10, "1-3年": 30, "3-5年": 35, "5-10年": 20, "10年+": 5},
        "education_distribution": {"本科": 40, "硕士": 50, "博士": 8, "大专": 2},
        "city_distribution": {"北京": 32, "上海": 24, "深圳": 18, "杭州": 14, "其他": 12},
    },
    "深度学习工程师": {
        "avg_salary": 55000,
        "total_jobs": 3100,
        "skills": ["Python", "PyTorch", "TensorFlow", "DL", "神经网络"],
        "entry_barrier": "很高",
        "growth_outlook": "很高",
        "top_companies": ["字节跳动", "百度", "商汤科技", "旷视科技", "华为"],
        "experience_distribution": {"应届": 5, "1-3年": 20, "3-5年": 40, "5-10年": 25, "10年+": 10},
        "education_distribution": {"本科": 15, "硕士": 55, "博士": 25, "大专": 5},
        "city_distribution": {"北京": 35, "上海": 22, "深圳": 18, "杭州": 12, "其他": 13},
    },
    "NLP工程师": {
        "avg_salary": 55000,
        "total_jobs": 2800,
        "skills": ["Python", "NLP", "Transformer", "BERT", "大模型"],
        "entry_barrier": "很高",
        "growth_outlook": "很高",
        "top_companies": ["百度", "字节跳动", "腾讯", "科大讯飞", "阿里巴巴"],
        "experience_distribution": {"应届": 5, "1-3年": 18, "3-5年": 38, "5-10年": 28, "10年+": 11},
        "education_distribution": {"本科": 12, "硕士": 58, "博士": 28, "大专": 2},
        "city_distribution": {"北京": 38, "上海": 20, "深圳": 15, "杭州": 14, "其他": 13},
    },
    "AI产品经理": {
        "avg_salary": 35000,
        "total_jobs": 4200,
        "skills": ["产品设计", "AI理解", "数据分析"],
        "entry_barrier": "较低",
        "growth_outlook": "高",
        "top_companies": ["字节跳动", "腾讯", "阿里巴巴", "百度", "京东"],
        "experience_distribution": {"应届": 8, "1-3年": 25, "3-5年": 42, "5-10年": 20, "10年+": 5},
        "education_distribution": {"本科": 60, "硕士": 30, "博士": 2, "大专": 8},
        "city_distribution": {"北京": 28, "上海": 23, "深圳": 22, "杭州": 15, "其他": 12},
    },
    "AI训练师": {
        "avg_salary": 20000,
        "total_jobs": 5500,
        "skills": ["数据处理", "标注工具", "AI基础"],
        "entry_barrier": "低",
        "growth_outlook": "中等",
        "top_companies": ["字节跳动", "百度", "数据堂", "海天瑞声", "腾讯"],
        "experience_distribution": {"应届": 25, "1-3年": 45, "3-5年": 20, "5-10年": 8, "10年+": 2},
        "education_distribution": {"本科": 50, "硕士": 15, "博士": 2, "大专": 33},
        "city_distribution": {"北京": 20, "上海": 18, "深圳": 15, "成都": 18, "其他": 29},
    },
    "推荐算法工程师": {
        "avg_salary": 40000,
        "total_jobs": 3800,
        "skills": ["Python", "ML", "推荐算法", "Spark", "SQL"],
        "entry_barrier": "较高",
        "growth_outlook": "高",
        "top_companies": ["字节跳动", "快手", "腾讯", "阿里巴巴", "美团"],
        "experience_distribution": {"应届": 8, "1-3年": 28, "3-5年": 38, "5-10年": 22, "10年+": 4},
        "education_distribution": {"本科": 35, "硕士": 50, "博士": 10, "大专": 5},
        "city_distribution": {"北京": 35, "上海": 20, "深圳": 18, "杭州": 15, "其他": 12},
    },
    "计算机视觉工程师": {
        "avg_salary": 45000,
        "total_jobs": 2900,
        "skills": ["Python", "OpenCV", "DL", "CNN"],
        "entry_barrier": "较高",
        "growth_outlook": "较高",
        "top_companies": ["商汤科技", "旷视科技", "海康威视", "字节跳动", "华为"],
        "experience_distribution": {"应届": 7, "1-3年": 25, "3-5年": 38, "5-10年": 23, "10年+": 7},
        "education_distribution": {"本科": 20, "硕士": 52, "博士": 20, "大专": 8},
        "city_distribution": {"北京": 28, "上海": 24, "深圳": 22, "杭州": 14, "其他": 12},
    },
}

ALIAS_MAP: Dict[str, str] = {
    "ai": "AI工程师",
    "ml": "机器学习工程师",
    "机器学习": "机器学习工程师",
    "dl": "深度学习工程师",
    "深度学习": "深度学习工程师",
    "nlp": "NLP工程师",
    "自然语言处理": "NLP工程师",
    "产品经理": "AI产品经理",
    "pm": "AI产品经理",
    "训练师": "AI训练师",
    "数据标注": "AI训练师",
    "推荐": "推荐算法工程师",
    "推荐系统": "推荐算法工程师",
    "cv": "计算机视觉工程师",
    "视觉": "计算机视觉工程师",
    "计算机视觉": "计算机视觉工程师",
}

MARKET_TRENDS: Dict[str, Any] = {
    "demand_trends": {
        "大模型/LLM": "爆发式增长 (+320%)",
        "AIGC": "高速增长 (+180%)",
        "自动驾驶": "稳定增长 (+45%)",
        "传统ML": "平稳 (0%)",
        "数据分析": "小幅下降 (-10%)",
    },
    "salary_trends": {
        "大模型工程师": "年涨幅 25-40%",
        "NLP工程师": "年涨幅 20-35%",
        "CV工程师": "年涨幅 15-25%",
        "ML工程师": "年涨幅 10-20%",
        "AI产品经理": "年涨幅 10-18%",
        "AI训练师": "年涨幅 5-12%",
    },
    "skill_trends": {
        "rising": ["大模型微调", "Prompt Engineering", "LangChain", "RLHF", "多模态", "向量数据库"],
        "stable": ["Python", "PyTorch", "Transformer", "SQL", "数据挖掘"],
        "declining": ["Caffe", "Theano", "传统规则引擎"],
    },
}


def _resolve_title(keyword: str) -> str:
    lower = keyword.lower().strip()
    if lower in ALIAS_MAP:
        return ALIAS_MAP[lower]
    for alias, title in ALIAS_MAP.items():
        if alias in lower:
            return title
    return "AI工程师"


def _build_skills_from_names(skill_names: List[str], required: bool = True) -> List[Skill]:
    skills: List[Skill] = []
    for name in skill_names:
        skills.append(Skill(
            name=name,
            level=SkillLevel.INTERMEDIATE if required else SkillLevel.BEGINNER,
            target_level=SkillLevel.ADVANCED if required else SkillLevel.INTERMEDIATE,
            category="核心技能",
            priority=2,
        ))
    return skills


class DataDrivenAnalyzer:
    """阶段一：数据驱动的需求分析"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._analysis_result: Optional[MarketData] = None
        self._last_keyword: str = ""

    def analyze(self, job_data: Optional[List[Dict[str, Any]]], keyword: str) -> MarketData:
        if job_data:
            return self._analyze_from_job_data(job_data, keyword)

        title = _resolve_title(keyword)
        builtin = BUILTIN_POSITIONS.get(title)
        if builtin is None:
            builtin = BUILTIN_POSITIONS["AI工程师"]

        top_skills: List[Dict[str, Any]] = []
        for skill_name in builtin["skills"]:
            top_skills.append({
                "name": skill_name,
                "count": 0,
                "avg_salary_boost": 0.0,
            })

        result = MarketData(
            keyword=title,
            total_jobs=builtin["total_jobs"],
            avg_salary=builtin["avg_salary"],
            top_skills=top_skills,
            top_companies=builtin["top_companies"],
            experience_distribution=builtin["experience_distribution"],
            education_distribution=builtin["education_distribution"],
            city_distribution=builtin["city_distribution"],
            source="builtin",
        )
        self._analysis_result = result
        self._last_keyword = keyword
        return result

    def _analyze_from_job_data(self, job_data: List[Dict[str, Any]], keyword: str) -> MarketData:
        total_jobs = len(job_data)
        salaries = [j.get("salary", 0) for j in job_data if j.get("salary")]
        avg_salary = sum(salaries) / len(salaries) if salaries else 0.0

        skill_counter: Dict[str, int] = {}
        skill_salary_map: Dict[str, List[float]] = {}
        for job in job_data:
            salary = job.get("salary", 0)
            for skill_item in job.get("skills", []):
                if isinstance(skill_item, dict):
                    name = skill_item.get("name", "")
                else:
                    name = str(skill_item)
                if not name:
                    continue
                skill_counter[name] = skill_counter.get(name, 0) + 1
                if salary:
                    skill_salary_map.setdefault(name, []).append(salary)

        top_skills: List[Dict[str, Any]] = []
        for skill_name, count in sorted(skill_counter.items(), key=lambda x: -x[1])[:20]:
            skill_salaries = skill_salary_map.get(skill_name, [])
            avg_boost = sum(skill_salaries) / len(skill_salaries) if skill_salaries else 0.0
            top_skills.append({
                "name": skill_name,
                "count": count,
                "avg_salary_boost": round(avg_boost, 2),
            })

        company_counter: Dict[str, int] = {}
        for job in job_data:
            company = job.get("company", "")
            if company:
                company_counter[company] = company_counter.get(company, 0) + 1
        top_companies = [c for c, _ in sorted(company_counter.items(), key=lambda x: -x[1])[:10]]

        result = MarketData(
            keyword=keyword,
            total_jobs=total_jobs,
            avg_salary=round(avg_salary, 2),
            top_skills=top_skills,
            top_companies=top_companies,
            source="job_data",
        )
        self._analysis_result = result
        self._last_keyword = keyword
        return result

    def define_position(
        self,
        title: str,
        industry: str = "互联网",
        required_skills: Optional[List[str]] = None,
        market_data: Optional[MarketData] = None,
    ) -> TargetPosition:

        resolved_title = _resolve_title(title)
        builtin = BUILTIN_POSITIONS.get(resolved_title, BUILTIN_POSITIONS["AI工程师"])

        if required_skills:
            skill_names = required_skills
        elif market_data and market_data.top_skills:
            skill_names = [s["name"] for s in market_data.top_skills[:8]]
        else:
            skill_names = builtin["skills"]

        resolved_skills = _build_skills_from_names(skill_names, required=True)

        preferred_names = ["沟通能力", "团队协作", "项目管理", "敏捷开发", "系统设计"]
        preferred_skills = _build_skills_from_names(preferred_names, required=False)

        if market_data:
            avg_salary = market_data.avg_salary
            job_count = market_data.total_jobs
        else:
            avg_salary = builtin["avg_salary"]
            job_count = builtin["total_jobs"]

        return TargetPosition(
            title=resolved_title,
            industry=industry,
            required_skills=resolved_skills,
            preferred_skills=preferred_skills,
            min_experience_years=1.0,
            avg_salary_range=[avg_salary * 0.6, avg_salary * 1.4],
            education_requirement=builtin.get("education_distribution", {}).get("硕士", 0) > 30 and "硕士及以上" or "本科及以上",
            job_count=job_count,
            growth_outlook=builtin["growth_outlook"],
            entry_barrier=builtin["entry_barrier"],
        )

    def get_market_trends(self) -> Dict[str, Any]:
        return {
            "demand_trends": MARKET_TRENDS["demand_trends"],
            "salary_trends": MARKET_TRENDS["salary_trends"],
            "skill_trends": MARKET_TRENDS["skill_trends"],
        }

    def export_analysis(self, output_path: str) -> None:
        if self._analysis_result is None:
            raise ValueError("请先调用 analyze() 方法进行分析")

        output: Dict[str, Any] = {
            "keyword": self._analysis_result.keyword,
            "total_jobs": self._analysis_result.total_jobs,
            "avg_salary": self._analysis_result.avg_salary,
            "top_skills": self._analysis_result.top_skills,
            "top_companies": self._analysis_result.top_companies,
            "experience_distribution": self._analysis_result.experience_distribution,
            "education_distribution": self._analysis_result.education_distribution,
            "city_distribution": self._analysis_result.city_distribution,
            "source": self._analysis_result.source,
            "collected_at": self._analysis_result.collected_at,
            "market_trends": self.get_market_trends(),
            "exported_at": datetime.now().isoformat(),
        }

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
