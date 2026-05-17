#!/usr/bin/env python3
"""
ADLP框架 - 命令行工具
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.engine import ADLPEngine
from core.models import ProgressRecord


def cmd_analyze(args):
    """市场分析命令"""
    engine = ADLPEngine(args.config)
    market = engine.analyze_market(keyword=args.keyword)
    target = engine.define_target(args.keyword)
    
    print(f"\n📊 市场分析结果 - '{args.keyword}'")
    print(f"岗位数: {market.total_jobs}")
    print(f"平均薪资: ¥{market.avg_salary/1000:.0f}K")
    print(f"入行门槛: {target.entry_barrier}")
    print(f"发展前景: {target.growth_outlook}")
    print(f"\n核心技能需求: {', '.join(s.name for s in target.required_skills[:8])}")
    
    if args.output:
        result = engine._market_to_dict()
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存到 {args.output}")


def cmd_profile(args):
    """用户画像命令"""
    engine = ADLPEngine(args.config)
    engine.define_target(args.target or args.keyword or "AI工程师")
    profile = engine.build_profile(
        name=args.name or "学习者",
        background=args.background or "有编程基础",
        current_role=args.current_role or "开发者",
        experience_years=args.experience or 1,
        education=args.education or "本科",
        weekly_hours=args.weekly_hours or 20,
        motivation=args.motivation or 7,
        persistence=args.persistence or 6
    )
    gaps = engine.assess_skill_gaps()
    report = engine.phase2.generate_profile_report(profile, engine.target_position, gaps)
    
    print(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 已保存到 {args.output}")


def cmd_plan(args):
    """学习路径命令"""
    engine = ADLPEngine(args.config)
    
    profile_kwargs = {}
    for attr in ['name', 'background', 'current_role', 'experience', 'education', 'motivation', 'persistence', 'weekly_hours']:
        val = getattr(args, attr, None)
        if val:
            profile_kwargs[attr] = val
    
    engine.build_profile(**profile_kwargs) if profile_kwargs else engine.build_profile()
    engine.define_target(args.target or args.keyword or "AI工程师")
    engine.design_path(args.weeks or 12)
    
    markdown = engine.export_path_markdown(args.output)
    print(markdown[:5000])
    if len(markdown) > 5000:
        print(f"\n... (共 {len(markdown)} 字符，全部内容已保存到文件)")


def cmd_full(args):
    """完整流程命令"""
    engine = ADLPEngine(args.config)
    
    profile_kwargs = {}
    for attr in ['name', 'background', 'current_role', 'experience', 'education', 'motivation', 'persistence', 'weekly_hours']:
        val = getattr(args, attr, None)
        if val is not None:
            profile_kwargs[attr] = val
    
    profile_kwargs['target_title'] = args.target or args.keyword or "AI工程师"
    
    result = engine.run_full(keyword=args.keyword or "AI", **profile_kwargs)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 完整报告已保存到 {args.output}")
    
    if args.output:
        path_md = engine.export_path_markdown(str(Path(args.output).with_suffix('.md')))
        print(f"✅ 学习路径已导出")


def cmd_prepare(args):
    """求职准备命令"""
    engine = ADLPEngine(args.config)
    
    profile_kwargs = {}
    for attr in ['name', 'background', 'current_role', 'experience']:
        val = getattr(args, attr, None)
        if val is not None:
            profile_kwargs[attr] = val
    
    engine.build_profile(**profile_kwargs) if profile_kwargs else engine.build_profile()
    engine.define_target(args.target or args.keyword or "AI工程师")
    engine.design_path(args.weeks or 12)
    
    resume = engine.generate_resume()
    interview = engine.generate_interview_prep()
    suggestions = engine.generate_learning_suggestions()
    
    output = f"""# 求职准备材料

{resume}

---

# 面试准备

## 技术基础
{chr(10).join(f'- {q["question"]}' for q in interview.get('tech_basics', interview.get('技术基础', []))) if isinstance(next(iter(interview.values()), {}), list) else '（见完整输出）'}

---

# 持续学习建议

{suggestions.get('summary', '')}
"""
    
    print(output[:3000])
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n✅ 已保存到 {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description='ADLP框架 - AI驱动的学习项目框架',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 分析AI岗位市场
  python -m adlp_skill.cli analyze --keyword AI工程师
  
  # 构建用户画像
  python -m adlp_skill.cli profile --name "小明" --background "2年Java开发"
  
  # 生成学习路径
  python -m adlp_skill.cli plan --keyword AI工程师 --weeks 12
  
  # 完整流程
  python -m adlp_skill.cli full --keyword AI工程师 --name "小明" --output result.json
  
  # 求职准备
  python -m adlp_skill.cli prepare --keyword AI工程师 --name "小明"
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 公共参数
    def add_common_args(p):
        p.add_argument('--keyword', '-k', default='AI工程师', help='目标关键词')
        p.add_argument('--target', '-t', help='目标岗位')
        p.add_argument('--config', help='配置文件路径')
        p.add_argument('--output', '-o', help='输出文件路径')
    
    def add_profile_args(p):
        p.add_argument('--name', help='姓名')
        p.add_argument('--background', help='背景描述')
        p.add_argument('--current-role', help='当前角色')
        p.add_argument('--experience', type=float, help='经验年数')
        p.add_argument('--education', help='学历')
        p.add_argument('--motivation', type=int, help='动机水平(1-10)')
        p.add_argument('--persistence', type=int, help='坚持力(1-10)')
        p.add_argument('--weekly-hours', type=int, help='每周学习时长')
        p.add_argument('--weeks', type=int, help='总周数')
    
    # analyze 命令
    p_analyze = subparsers.add_parser('analyze', help='市场分析')
    add_common_args(p_analyze)
    
    # profile 命令
    p_profile = subparsers.add_parser('profile', help='用户画像')
    add_common_args(p_profile)
    add_profile_args(p_profile)
    
    # plan 命令
    p_plan = subparsers.add_parser('plan', help='学习路径')
    add_common_args(p_plan)
    add_profile_args(p_plan)
    
    # full 命令
    p_full = subparsers.add_parser('full', help='完整流程')
    add_common_args(p_full)
    add_profile_args(p_full)
    
    # prepare 命令
    p_prepare = subparsers.add_parser('prepare', help='求职准备')
    add_common_args(p_prepare)
    add_profile_args(p_prepare)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        'analyze': cmd_analyze,
        'profile': cmd_profile,
        'plan': cmd_plan,
        'full': cmd_full,
        'prepare': cmd_prepare,
    }
    
    commands[args.command](args)


if __name__ == '__main__':
    main()
