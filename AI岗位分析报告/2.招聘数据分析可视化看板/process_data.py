import os
import csv
import re
import json
from collections import Counter, defaultdict

# 技能关键词列表
CORE_SKILLS_KEYWORDS = [
    'Python', 'Java', 'LangChain', 'LangGraph', 'RAG', 'LLM', 'Prompt', 
    'Embedding', 'Vector', 'Database', 'API', 'FastAPI', 'Flask', 'Spring',
    'Deep Learning', 'Machine Learning', 'NLP', 'CV', 'Computer Vision',
    'TensorFlow', 'PyTorch', 'Transformers', 'HuggingFace', 'OpenAI',
    'Function Calling', 'Tool Use', 'Agents', 'Multi-Agent', 'Dify', 'Coze'
]

PLUS_SKILLS_KEYWORDS = [
    'Docker', 'Kubernetes', 'K8s', 'AWS', 'Azure', 'GCP', 'Cloud',
    'CI/CD', 'Git', 'GitHub', 'DevOps', 'MLOps', 'Fine-tuning', 'LoRA',
    'QLoRA', 'SFT', 'Model Training', 'Distributed', 'Scalable',
    'Redis', 'PostgreSQL', 'MySQL', 'MongoDB', 'Elasticsearch',
    'React', 'Vue', 'Next.js', 'TypeScript', 'JavaScript', 'HTML', 'CSS'
]

ALL_SKILLS = CORE_SKILLS_KEYWORDS + PLUS_SKILLS_KEYWORDS

def parse_salary(salary_str):
    """解析薪资字符串，返回平均薪资(K)"""
    if not salary_str or salary_str == '面议':
        return None
    
    salary_str = salary_str.replace(' ', '').replace('K', 'k')
    
    range_match = re.search(r'(\d+\.?\d*)-(\d+\.?\d*)(k|万)', salary_str.lower())
    if range_match:
        min_val = float(range_match.group(1))
        max_val = float(range_match.group(2))
        unit = range_match.group(3)
        
        avg = (min_val + max_val) / 2
        
        if unit == '万':
            avg = avg * 10
        
        return round(avg, 1)
    
    fixed_match = re.search(r'(\d+\.?\d*)(k|万)', salary_str.lower())
    if fixed_match:
        val = float(fixed_match.group(1))
        unit = fixed_match.group(2)
        
        if unit == '万':
            val = val * 10
        
        return round(val, 1)
    
    return None

def extract_city(location_str):
    """从工作地点中提取城市"""
    if not location_str:
        return None
    
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '苏州']
    for city in cities:
        if city in location_str:
            return city
    
    return None

def extract_experience(exp_str):
    """标准化经验要求"""
    if not exp_str:
        return '经验不限'
    
    exp_str = exp_str.strip()
    
    if '不限' in exp_str:
        return '经验不限'
    elif '应届' in exp_str or '在校' in exp_str:
        return '经验不限'
    elif '1-3' in exp_str or '1~3' in exp_str:
        return '1-3年'
    elif '3-5' in exp_str or '3~5' in exp_str:
        return '3-5年'
    elif '5-10' in exp_str or '5~10' in exp_str:
        return '5-10年'
    elif '10年以上' in exp_str or '10年+' in exp_str:
        return '10年以上'
    elif '1年' in exp_str:
        return '1-3年'
    elif '3年' in exp_str:
        return '3-5年'
    elif '5年' in exp_str:
        return '5-10年'
    elif '10年' in exp_str:
        return '10年以上'
    
    return '经验不限'

def extract_company_size(size_str):
    """标准化公司规模"""
    if not size_str:
        return '未知'
    
    size_str = size_str.strip()
    
    if '0-20' in size_str or '20人以下' in size_str:
        return '0-20人'
    elif '20-99' in size_str or '20-99' in size_str or '100人以下' in size_str:
        return '20-99人'
    elif '100-499' in size_str or '100-499' in size_str:
        return '100-499人'
    elif '500-999' in size_str or '500-999' in size_str:
        return '500-999人'
    elif '1000-9999' in size_str or '1000-9999' in size_str:
        return '1000-9999人'
    elif '10000' in size_str or '万人' in size_str:
        return '10000人以上'
    
    return '未知'

def extract_education(edu_str):
    """标准化学历要求"""
    if not edu_str:
        return '学历不限'
    
    edu_str = edu_str.strip()
    
    if '博士' in edu_str:
        return '博士'
    elif '硕士' in edu_str:
        return '硕士'
    elif '本科' in edu_str:
        return '本科'
    elif '大专' in edu_str or '专科' in edu_str:
        return '大专'
    elif '高中' in edu_str or '中专' in edu_str:
        return '高中及以下'
    elif '不限' in edu_str:
        return '学历不限'
    
    return '学历不限'

def extract_skills(desc):
    """从职位描述中提取技能"""
    if not desc:
        return {'core': [], 'plus': []}
    
    desc_lower = desc.lower()
    core_skills = []
    plus_skills = []
    
    for skill in CORE_SKILLS_KEYWORDS:
        if skill.lower() in desc_lower:
            core_skills.append(skill)
    
    for skill in PLUS_SKILLS_KEYWORDS:
        if skill.lower() in desc_lower:
            plus_skills.append(skill)
    
    return {
        'core': list(set(core_skills)),
        'plus': list(set(plus_skills))
    }

def extract_job_details(desc):
    """从职位描述中提取主要职责和技术要求"""
    responsibilities = []
    tech_requirements = []
    
    if not desc:
        return {'responsibilities': [], 'tech_requirements': []}
    
    # 提取职责相关内容
    responsibility_keywords = ['职责', '负责', '主要', '工作', '参与', '开发', '设计', '构建', '优化', '负责', '承担', '负责', '负责']
    # 提取技术相关内容
    tech_keywords = ['要求', '熟悉', '精通', '掌握', '具备', '技能', '能力', '经验', '了解', '框架', '语言', '熟悉', '掌握', '精通']
    
    # 分割句子
    sentences = re.split(r'[。！？；]', desc)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # 检查是否是职责相关
        if any(keyword in sentence for keyword in responsibility_keywords):
            # 清理句子，提取要点
            cleaned = re.sub(r'^职位描述|^职责|^任职要求|^要求|^1[、.]|^2[、.]|^3[、.]|^4[、.]|^5[、.]|^6[、.]|^7[、.]|^8[、.]|^9[、.]', '', sentence)
            cleaned = cleaned.strip()
            if len(cleaned) > 5 and len(cleaned) < 100:
                # 进一步提取要点
                for keyword in ['负责', '参与', '开发', '设计', '构建', '优化', '承担']:
                    if keyword in cleaned:
                        cleaned = re.sub(r'^.*?' + keyword, keyword, cleaned)
                        break
                responsibilities.append(cleaned)
        
        # 检查是否是技术要求相关
        if any(keyword in sentence for keyword in tech_keywords):
            cleaned = re.sub(r'^职位描述|^职责|^任职要求|^要求|^1[、.]|^2[、.]|^3[、.]|^4[、.]|^5[、.]|^6[、.]|^7[、.]|^8[、.]|^9[、.]', '', sentence)
            cleaned = cleaned.strip()
            if len(cleaned) > 5 and len(cleaned) < 100:
                # 进一步提取要点
                for keyword in ['熟悉', '精通', '掌握', '具备', '了解', '要求']:
                    if keyword in cleaned:
                        cleaned = re.sub(r'^.*?' + keyword, keyword, cleaned)
                        break
                tech_requirements.append(cleaned)
    
    # 去重
    responsibilities = list(set(responsibilities))
    tech_requirements = list(set(tech_requirements))
    
    return {
        'responsibilities': responsibilities,
        'tech_requirements': tech_requirements
    }

def normalize_job_name(job_name):
    """归一化岗位名称，智能合并相似岗位"""
    if not job_name:
        return '未知'
    
    job_name = job_name.strip()
    job_name_lower = job_name.lower()
    
    # 智能归类 - 合并相似岗位
    if 'agent' in job_name_lower or '智能体' in job_name:
        return 'AI Agent开发工程师'
    
    if '大模型' in job_name or 'llm' in job_name_lower:
        return '大模型开发工程师'
    
    if '算法' in job_name:
        if 'nlp' in job_name_lower or '自然语言' in job_name:
            return 'NLP算法工程师'
        elif 'cv' in job_name_lower or '视觉' in job_name:
            return '计算机视觉算法工程师'
        else:
            return '算法工程师'
    
    if '数据' in job_name and '标注' not in job_name:
        return '数据工程师'
    
    if '产品' in job_name and '经理' in job_name:
        return '产品经理'
    
    if '测试' in job_name or '评测' in job_name:
        return '测试/评测工程师'
    
    if 'ai应用' in job_name_lower or 'ai开发' in job_name_lower:
        return 'AI应用开发工程师'
    
    if '全栈' in job_name:
        return '全栈工程师'
    
    if '后端' in job_name:
        return '后端开发工程师'
    
    if '前端' in job_name:
        return '前端开发工程师'
    
    if '架构' in job_name:
        return '架构师'
    
    if '运维' in job_name or 'devops' in job_name_lower:
        return '运维/DevOps工程师'
    
    # 如果没有匹配到，清理一下并返回
    job_name = re.sub(r'\([^)]*\)', '', job_name)
    job_name = re.sub(r'（[^）]*）', '', job_name)
    job_name = re.sub(r'J\d+', '', job_name, flags=re.IGNORECASE)
    job_name = re.sub(r'\d+-\d+', '', job_name)
    job_name = re.sub(r'\d+年', '', job_name)
    job_name = re.sub(r'[0-9]+', '', job_name)
    job_name = re.sub(r'[\s\-_\.,·/]+', '', job_name)
    
    return job_name

def process_csv(file_path):
    """处理单个CSV文件"""
    jobs = []
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if 'zhaopin_' in file_path:
                    job_name = row.get('岗位名称', '')
                    company = row.get('公司名称', '')
                    salary_str = row.get('薪资范围', '')
                    location = row.get('工作城市', '')
                    experience = row.get('经验要求', '')
                    education = row.get('学历要求', '')
                    company_size = row.get('公司规模', '')
                    industry = row.get('公司行业', '')
                    desc = row.get('职位描述', '')
                else:
                    job_name = row.get('岗位名称', '')
                    company = row.get('公司名称', '')
                    salary_str = row.get('薪资范围', '')
                    location = row.get('工作地点', '')
                    experience = row.get('经验要求', '')
                    education = row.get('学历要求', '')
                    company_size = row.get('公司规模', '')
                    industry = row.get('公司行业', '')
                    desc = row.get('职位信息', '')
                
                salary = parse_salary(salary_str)
                city = extract_city(location)
                exp = extract_experience(experience)
                edu = extract_education(education)
                size = extract_company_size(company_size)
                skills = extract_skills(desc)
                job_details = extract_job_details(desc)
                
                normalized_job_name = normalize_job_name(job_name)
                
                if salary and city:
                    job = {
                        'jobName': job_name,
                        'normalizedJobName': normalized_job_name,
                        'company': company,
                        'salary': salary,
                        'city': city,
                        'experience': exp,
                        'education': edu,
                        'companySize': size,
                        'industry': industry,
                        'type': normalized_job_name,
                        'skills': skills['core'] + skills['plus'],
                        'coreSkills': skills['core'],
                        'plusSkills': skills['plus'],
                        'responsibilities': job_details['responsibilities'],
                        'techRequirements': job_details['tech_requirements']
                    }
                    jobs.append(job)
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return jobs

def aggregate_job_details(all_jobs):
    """按岗位类型聚合职责和技术要求"""
    job_type_details = defaultdict(lambda: {
        'responsibilities': [],
        'techRequirements': [],
        'count': 0,
        'avgSalary': 0
    })
    
    for job in all_jobs:
        job_type = job['type']
        job_type_details[job_type]['count'] += 1
        job_type_details[job_type]['avgSalary'] += job['salary']
        job_type_details[job_type]['responsibilities'].extend(job['responsibilities'])
        job_type_details[job_type]['techRequirements'].extend(job['techRequirements'])
    
    result = {}
    for job_type, details in job_type_details.items():
        details['avgSalary'] = round(details['avgSalary'] / details['count'], 1)
        resp_counter = Counter(details['responsibilities'])
        tech_counter = Counter(details['techRequirements'])
        details['responsibilities'] = [item for item, count in resp_counter.most_common(5)]
        details['techRequirements'] = [item for item, count in tech_counter.most_common(5)]
        result[job_type] = details
    
    return result

def main():
    """主函数"""
    data_dir = os.path.join(os.path.dirname(__file__), '招聘原始数据')
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'processed')
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_jobs = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_dir, filename)
            print(f"Processing {filename}...")
            jobs = process_csv(file_path)
            all_jobs.extend(jobs)
            print(f"  Found {len(jobs)} valid jobs")
    
    print(f"\nTotal jobs: {len(all_jobs)}")
    
    core_skill_counts = Counter()
    plus_skill_counts = Counter()
    
    for job in all_jobs:
        for skill in job['coreSkills']:
            core_skill_counts[skill] += 1
        for skill in job['plusSkills']:
            plus_skill_counts[skill] += 1
    
    core_skills_data = [{'name': k, 'value': v} for k, v in core_skill_counts.most_common()]
    plus_skills_data = [{'name': k, 'value': v} for k, v in plus_skill_counts.most_common()]
    
    # 聚合岗位类型详细信息
    job_type_details = aggregate_job_details(all_jobs)
    
    with open(os.path.join(output_dir, 'jobs_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, 'core_skills.json'), 'w', encoding='utf-8') as f:
        json.dump(core_skills_data, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, 'plus_skills.json'), 'w', encoding='utf-8') as f:
        json.dump(plus_skills_data, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, 'job_type_details.json'), 'w', encoding='utf-8') as f:
        json.dump(job_type_details, f, ensure_ascii=False, indent=2)
    
    print(f"\nData saved to {output_dir}")
    print(f"Job types: {len(job_type_details)}")

if __name__ == '__main__':
    main()
