---
name: adlp-framework
version: 1.0.0
description: |
  AI-Driven Learning Project Framework（ADLP框架）
  
  通过AI辅助，将复杂的学习目标拆解为可执行的项目，通过数据驱动决策，实现高效学习转型。
  
  核心功能：
  - 数据驱动的需求分析（招聘数据、技能需求、市场趋势）
  - 个性化学习画像构建（能力评估、目标设定、匹配度分析）
  - 结构化学习路径设计（时间规划、资源矩阵）
  - 项目驱动的实践学习（梯度项目、进度跟踪）
  - 成果导向的求职准备（作品集、面试准备）

triggers:
  - 学习规划
  - 职业转型
  - 技能提升
  - 求职准备
  - 技术学习
  - 转行AI
  - 学习路径
  - 个人发展计划

usage:
  cli: python cli.py [command] [options]
  python: from adlp_skill import ADLPEngine

commands:
  analyze: 分析目标岗位需求和技能缺口
  profile: 构建个人学习画像
  plan: 生成结构化学习路径
  full: 运行完整ADLP流程
  prepare: 生成求职准备材料

outputs:
  - 个人学习画像报告 (JSON/HTML)
  - 结构化学习路径 (Markdown/JSON)
  - 项目计划模板 (Markdown)
  - 求职材料包 (Markdown/HTML)

dependencies:
  - Python 3.8+
  - pyyaml (配置管理)
  - flask (Web界面，可选)
---

# ADLP框架使用说明

## 概述

ADLP (AI-Driven Learning Project Framework) 是一个通过AI辅助，将复杂的学习目标拆解为可执行项目的框架。

## 快速开始

### 方式一：命令行工具

```bash
cd adlp_skill

# 市场分析
python cli.py analyze --keyword AI工程师

# 用户画像
python cli.py profile --name "小明" --background "2年Java开发"

# 生成学习路径（16周）
python cli.py plan --keyword 机器学习工程师 --name "小红" --weeks 16

# 完整5阶段流程
python cli.py full --keyword AI工程师 --name "小明" --experience 2 --weekly-hours 20 --output result.json

# 求职准备
python cli.py prepare --keyword NLP工程师 --name "张工" --background "后端开发"
```

### 方式二：Python API

```python
from adlp_skill import ADLPEngine

engine = ADLPEngine()                                              
result = engine.run_full(keyword="AI工程师", name="小明")           
path_md = engine.export_path_markdown()                           
```

### 方式三：Web界面

```bash
python web.py
# 访问 http://localhost:5001
```

## 项目结构

```
adlp_skill/
├── __init__.py              # 包入口
├── SKILL.md                 # 本文件
├── skill.yaml               # 技能元数据
├── cli.py                   # 命令行工具
├── web.py                   # Web界面
├── core/
│   ├── models.py            # 数据模型
│   ├── engine.py            # 核心引擎
│   ├── phase1_analysis.py   # 阶段一：需求分析
│   ├── phase2_profile.py    # 阶段二：画像构建
│   ├── phase3_design.py     # 阶段三：路径设计
│   ├── phase4_practice.py   # 阶段四：项目实践
│   └── phase5_career.py     # 阶段五：求职准备
└── templates/
    ├── tech_transition.md   # 技术转型模板
    └── skill_upgrade.md     # 技能提升模板
```

## 五大阶段

| 阶段 | 模块 | 输出 |
|------|------|------|
| 1 需求分析 | phase1_analysis | 市场数据、岗位需求 |
| 2 画像构建 | phase2_profile | 能力雷达、技能缺口 |
| 3 路径设计 | phase3_design | 学习路径、周计划 |
| 4 项目实践 | phase4_practice | 梯度项目、进度跟踪 |
| 5 求职准备 | phase5_career | 简历、面试、策略 |
