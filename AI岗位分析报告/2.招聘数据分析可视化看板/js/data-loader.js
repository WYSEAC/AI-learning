let jobData = [];
let coreSkillsData = [];
let plusSkillsData = [];
let jobTypeDetails = {};
let currentFilteredData = [];

async function loadData() {
    try {
        const jobsResponse = await fetch('data/processed/jobs_cleaned.json');
        jobData = await jobsResponse.json();
        
        const coreSkillsResponse = await fetch('data/processed/core_skills.json');
        coreSkillsData = await coreSkillsResponse.json();
        
        const plusSkillsResponse = await fetch('data/processed/plus_skills.json');
        plusSkillsData = await plusSkillsResponse.json();
        
        const jobTypeDetailsResponse = await fetch('data/processed/job_type_details.json');
        jobTypeDetails = await jobTypeDetailsResponse.json();
        
        currentFilteredData = [...jobData];
        console.log('数据加载成功:', jobData.length, '条岗位数据');
        console.log('岗位详情数据:', jobTypeDetails);
        
    } catch (error) {
        console.error('加载数据失败:', error);
        useMockData();
    }
}

function useMockData() {
    console.log('使用模拟数据');
    
    const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '苏州'];
    const experiences = ['经验不限', '1-3年', '3-5年', '5-10年', '10年以上'];
    const educations = ['学历不限', '大专', '本科', '硕士', '博士'];
    const companySizes = ['0-20人', '20-99人', '100-499人', '500-999人', '1000-9999人', '10000人以上'];
    const jobTypes = ['AI Agent开发工程师', '大模型开发工程师', '算法工程师', '数据工程师'];
    
    jobData = [];
    for (let i = 0; i < 1000; i++) {
        const city = cities[Math.floor(Math.random() * cities.length)];
        const exp = experiences[Math.floor(Math.random() * experiences.length)];
        const edu = educations[Math.floor(Math.random() * educations.length)];
        const size = companySizes[Math.floor(Math.random() * companySizes.length)];
        const type = jobTypes[Math.floor(Math.random() * jobTypes.length)];
        
        let baseSalary = 15;
        if (exp === '1-3年') baseSalary = 20;
        if (exp === '3-5年') baseSalary = 30;
        if (exp === '5-10年') baseSalary = 45;
        if (exp === '10年以上') baseSalary = 60;
        
        if (city === '北京' || city === '上海' || city === '深圳') {
            baseSalary *= 1.2;
        }
        
        const salary = baseSalary + Math.random() * 20;
        
        jobData.push({
            jobName: type + ' ' + (i + 1),
            normalizedJobName: type,
            company: '科技公司 ' + (i + 1),
            salary: Math.round(salary * 10) / 10,
            city: city,
            experience: exp,
            education: edu,
            companySize: size,
            industry: '互联网',
            type: type,
            skills: ['Python', 'LangChain'],
            coreSkills: ['Python', 'LangChain'],
            plusSkills: ['Docker'],
            responsibilities: ['负责产品开发', '参与架构设计', '优化性能调优'],
            techRequirements: ['熟悉Python', '精通LangChain', '有大模型开发经验']
        });
    }
    
    coreSkillsData = ['Python', 'LangChain', 'RAG', 'LLM'].map(skill => ({
        name: skill, value: Math.floor(Math.random() * 500 + 200)
    }));
    
    plusSkillsData = ['Docker', 'Kubernetes', 'Git', 'React'].map(skill => ({
        name: skill, value: Math.floor(Math.random() * 300 + 100)
    }));
    
    jobTypes.forEach(type => {
        jobTypeDetails[type] = {
            count: Math.floor(Math.random() * 300),
            avgSalary: Math.floor(Math.random() * 30 + 20),
            responsibilities: ['负责核心系统架构设计与技术选型', '主导AI产品的工程化落地与性能优化', '与产品团队协作推动需求分析与功能迭代', '负责生产环境部署与运维监控', '编写技术文档与推动团队代码规范'],
            techRequirements: ['精通Python，熟悉FastAPI/Django等主流框架', '深入理解LangChain/RAG技术栈与向量数据库', '有Docker容器化部署与CI/CD流水线经验', '了解大模型微调与分布式训练基本概念', '具备良好的系统设计能力与跨团队沟通能力']
        };
    });
    
    currentFilteredData = [...jobData];
}

function getFilteredData() {
    return currentFilteredData;
}

function getOriginalData() {
    return jobData;
}

function getCoreSkillsData() {
    return coreSkillsData;
}

function getPlusSkillsData() {
    return plusSkillsData;
}

function getJobTypeDetails() {
    return jobTypeDetails;
}
