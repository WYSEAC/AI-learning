"""ADLP 核心引擎 - 统一调度五个阶段"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from .models import UserProfile, TargetPosition, SkillGap, LearningPath, ProgressRecord, MarketData
from .phase1_analysis import DataDrivenAnalyzer
from .phase2_profile import ProfileAnalyzer
from .phase3_design import PathDesigner
from .phase4_practice import ProjectPracticeManager
from .phase5_career import CareerPreparer


class ADLPEngine:
    """ADLP框架核心引擎"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.phase1 = DataDrivenAnalyzer(self.config)
        self.phase2 = ProfileAnalyzer(self.config)
        self.phase3 = PathDesigner(self.config)
        self.phase4 = ProjectPracticeManager(self.config)
        self.phase5 = CareerPreparer(self.config)
        
        self.user_profile: Optional[UserProfile] = None
        self.target_position: Optional[TargetPosition] = None
        self.learning_path: Optional[LearningPath] = None
        self.progress_records: List[ProgressRecord] = []
        self.market_data: Optional[MarketData] = None
    
    def _load_config(self, config_path: Optional[str]) -> dict:
        """加载配置"""
        default_config = {
            'output_dir': './adlp_output',
            'data_sources': {
                'job_scraper': '../job_scraper',
                'sample_data': './data/samples'
            },
            'risk_tolerance': 'medium',
            'default_weeks': 12,
            'visualization': {
                'enabled': True,
                'format': 'html'
            }
        }
        
        if config_path:
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config or {})
            except:
                pass
        
        return default_config
    
    # ── 阶段一：数据驱动的需求分析 ──
    
    def analyze_market(self, job_data: Optional[List[Dict]] = None, 
                       keyword: str = "AI") -> MarketData:
        """分析市场数据"""
        self.market_data = self.phase1.analyze(job_data, keyword)
        return self.market_data
    
    def define_target(self, title: str, industry: str = "互联网",
                      required_skills: Optional[List[str]] = None) -> TargetPosition:
        """定义目标岗位"""
        self.target_position = self.phase1.define_position(
            title, industry, required_skills, self.market_data
        )
        return self.target_position
    
    # ── 阶段二：个性化学习画像 ──
    
    def build_profile(self, **kwargs) -> UserProfile:
        """构建用户画像"""
        self.user_profile = self.phase2.build_profile(**kwargs)
        return self.user_profile
    
    def assess_skill_gaps(self) -> List[SkillGap]:
        """评估技能缺口"""
        if not self.user_profile or not self.target_position:
            raise ValueError("请先构建用户画像和定义目标岗位")
        return self.phase2.analyze_gaps(self.user_profile, self.target_position)
    
    def generate_radar(self) -> Dict:
        """生成能力雷达图数据"""
        gaps = self.assess_skill_gaps()
        return self.phase2.build_radar_data(self.user_profile, self.target_position, gaps)
    
    # ── 阶段三：学习路径设计 ──
    
    def design_path(self, total_weeks: Optional[int] = None) -> LearningPath:
        """设计学习路径"""
        if not self.user_profile or not self.target_position:
            raise ValueError("请先完成阶段一和阶段二")
        
        gaps = self.assess_skill_gaps()
        self.learning_path = self.phase3.design(
            self.user_profile, self.target_position, gaps, 
            total_weeks or self.config.get('default_weeks', 12)
        )
        return self.learning_path
    
    def export_path_markdown(self, output_path: Optional[str] = None) -> str:
        """导出学习路径为Markdown"""
        if not self.learning_path:
            self.design_path()
        return self.phase3.export_markdown(self.learning_path, output_path)
    
    def export_path_json(self, output_path: Optional[str] = None) -> str:
        """导出学习路径为JSON"""
        if not self.learning_path:
            self.design_path()
        return self.phase3.export_json(self.learning_path, output_path)
    
    # ── 阶段四：项目驱动实践 ──
    
    def generate_projects(self) -> List[Dict]:
        """生成梯度项目列表"""
        if not self.learning_path:
            self.design_path()
        return self.phase4.generate_project_ladder(self.learning_path)
    
    def create_weekly_plan(self, week: int) -> Dict:
        """创建周度计划"""
        if not self.learning_path:
            self.design_path()
        return self.phase4.create_weekly_plan(self.learning_path, week)
    
    def record_progress(self, record: ProgressRecord):
        """记录学习进度"""
        self.progress_records.append(record)
    
    def generate_progress_report(self) -> str:
        """生成进度报告"""
        return self.phase4.generate_report(
            self.learning_path, self.progress_records
        )
    
    # ── 阶段五：求职准备 ──
    
    def prepare_career(self) -> Dict:
        """准备求职材料"""
        if not self.user_profile or not self.target_position:
            raise ValueError("请先完成前面的阶段")
        return self.phase5.prepare(
            self.user_profile, self.target_position, 
            self.learning_path, self.progress_records
        )
    
    def generate_resume(self, projects: Optional[List[Dict]] = None) -> str:
        """生成简历"""
        return self.phase5.build_resume(self.user_profile, self.target_position, projects)
    
    def generate_interview_prep(self, tech_stack: Optional[List[str]] = None) -> Dict:
        """生成面试准备材料"""
        return self.phase5.prepare_interview(self.target_position, tech_stack)
    
    def generate_learning_suggestions(self) -> Dict:
        """生成学习建议"""
        return self.phase5.suggest_continuous_learning(
            self.user_profile, self.target_position
        )
    
    # ── 综合方法 ──
    
    def run_full(self, job_data: Optional[List[Dict]] = None, 
                 keyword: str = "AI", **profile_kwargs) -> Dict:
        """运行完整ADLP流程"""
        print("=" * 60)
        print("🎯 ADLP框架 - 完整流程")
        print("=" * 60)
        
        # 阶段一
        print("\n📊 [阶段一] 数据驱动的需求分析...")
        self.analyze_market(job_data, keyword)
        self.define_target(profile_kwargs.get('target_title', keyword))
        
        # 阶段二
        print("\n👤 [阶段二] 个性化学习画像构建...")
        self.build_profile(**profile_kwargs)
        gaps = self.assess_skill_gaps()
        print(f"   识别到 {len(gaps)} 个技能缺口")
        for gap in gaps[:5]:
            print(f"   - {gap.skill_name}: {gap.current_level.value} → {gap.target_level.value}")
        
        # 阶段三
        print("\n📐 [阶段三] 学习路径设计...")
        path = self.design_path()
        print(f"   设计了 {len(path.phases)} 个学习阶段，共 {path.total_weeks} 周")
        
        # 阶段四
        print("\n🚀 [阶段四] 项目规划...")
        projects = self.generate_projects()
        print(f"   生成了 {len(projects)} 个梯度项目")
        
        # 阶段五
        print("\n💼 [阶段五] 求职准备...")
        career = self.prepare_career()
        
        # 汇总
        result = {
            'market_data': self._market_to_dict(),
            'user_profile': self._profile_to_dict(),
            'skill_gaps': [self._gap_to_dict(g) for g in gaps],
            'learning_path': self._path_to_dict(path),
            'projects': projects,
            'career_prep': career,
            'generated_at': datetime.now().isoformat()
        }
        
        print("\n" + "=" * 60)
        print("✅ ADLP完整流程执行完毕！")
        print("=" * 60)
        
        return result
    
    def _market_to_dict(self) -> Dict:
        if not self.market_data:
            return {}
        return {
            'keyword': self.market_data.keyword,
            'total_jobs': self.market_data.total_jobs,
            'avg_salary': self.market_data.avg_salary,
            'top_skills': self.market_data.top_skills
        }
    
    def _profile_to_dict(self) -> Dict:
        if not self.user_profile:
            return {}
        return {
            'name': self.user_profile.name,
            'background': self.user_profile.background,
            'current_role': self.user_profile.current_role
        }
    
    def _gap_to_dict(self, gap: SkillGap) -> Dict:
        return {
            'skill': gap.skill_name,
            'current': gap.current_level.value,
            'target': gap.target_level.value,
            'gap': gap.gap_size,
            'hours': gap.estimated_hours
        }
    
    def _path_to_dict(self, path: LearningPath) -> Dict:
        return {
            'total_weeks': path.total_weeks,
            'phases': len(path.phases),
            'risks': path.risks[:5]
        }
