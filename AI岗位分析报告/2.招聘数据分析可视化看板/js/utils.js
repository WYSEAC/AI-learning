// 工具函数

// 更新概览指标
function updateOverviewCards(data) {
    const totalJobs = data.length;
    const avgSalary = data.length > 0 
        ? Math.round(data.reduce((sum, j) => sum + j.salary, 0) / data.length) 
        : 0;
    const cities = [...new Set(data.map(j => j.city))];
    
    // 找出最热技能
    const skillCount = {};
    data.forEach(job => {
        job.skills.forEach(skill => {
            skillCount[skill] = (skillCount[skill] || 0) + 1;
        });
    });
    const topSkill = Object.entries(skillCount)
        .sort((a, b) => b[1] - a[1])[0]?.[0] || '-';
    
    document.getElementById('totalJobs').textContent = totalJobs;
    document.getElementById('avgSalary').textContent = avgSalary + 'K';
    document.getElementById('cityCount').textContent = cities.length;
    document.getElementById('topSkill').textContent = topSkill;
}

// 按城市聚合数据
function aggregateByCity(data) {
    const result = {};
    data.forEach(job => {
        if (!result[job.city]) {
            result[job.city] = { count: 0, totalSalary: 0 };
        }
        result[job.city].count++;
        result[job.city].totalSalary += job.salary;
    });
    return Object.entries(result).map(([city, data]) => ({
        name: city,
        count: data.count,
        avgSalary: Math.round(data.totalSalary / data.count)
    })).sort((a, b) => b.count - a.count);
}

// 按经验聚合数据
function aggregateByExperience(data) {
    const expOrder = ['经验不限', '1-3年', '3-5年', '5-10年', '10年以上'];
    const result = {};
    expOrder.forEach(exp => result[exp] = { count: 0, totalSalary: 0 });
    
    data.forEach(job => {
        if (result[job.experience]) {
            result[job.experience].count++;
            result[job.experience].totalSalary += job.salary;
        }
    });
    
    return expOrder.map(exp => ({
        name: exp,
        count: result[exp].count,
        avgSalary: result[exp].count > 0 
            ? Math.round(result[exp].totalSalary / result[exp].count) 
            : 0
    }));
}

// 按学历聚合数据
function aggregateByEducation(data) {
    const eduOrder = ['学历不限', '高中及以下', '大专', '本科', '硕士', '博士'];
    const result = {};
    eduOrder.forEach(edu => result[edu] = 0);
    
    data.forEach(job => {
        if (result[job.education] !== undefined) {
            result[job.education]++;
        }
    });
    
    return eduOrder.map(edu => ({
        name: edu,
        value: result[edu]
    })).filter(item => item.value > 0);
}

// 按公司规模聚合数据
function aggregateByCompanySize(data) {
    const sizeOrder = ['0-20人', '20-99人', '100-499人', '500-999人', '1000-9999人', '10000人以上', '未知'];
    const result = {};
    sizeOrder.forEach(size => result[size] = 0);
    
    data.forEach(job => {
        if (result[job.companySize] !== undefined) {
            result[job.companySize]++;
        }
    });
    
    return sizeOrder.map(size => ({
        name: size,
        value: result[size]
    })).filter(item => item.value > 0);
}

// 按岗位类型聚合数据
function aggregateByJobType(data) {
    const result = {};
    data.forEach(job => {
        result[job.type] = (result[job.type] || 0) + 1;
    });
    return Object.entries(result)
        .map(([type, count]) => ({ name: type, value: count }))
        .sort((a, b) => b.value - a.value);
}

// 按行业聚合数据
function aggregateByIndustry(data) {
    const result = {};
    data.forEach(job => {
        const industry = job.industry || '其他';
        result[industry] = (result[industry] || 0) + 1;
    });
    return Object.entries(result)
        .map(([industry, count]) => ({ name: industry, value: count }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 10);
}

// 薪资分布统计
function getSalaryDistribution(data) {
    const ranges = [
        { min: 0, max: 10, label: '0-10K' },
        { min: 10, max: 20, label: '10-20K' },
        { min: 20, max: 30, label: '20-30K' },
        { min: 30, max: 40, label: '30-40K' },
        { min: 40, max: 50, label: '40-50K' },
        { min: 50, max: 70, label: '50-70K' },
        { min: 70, max: 100, label: '70-100K' },
        { min: 100, max: Infinity, label: '100K+' }
    ];
    
    const result = ranges.map(r => ({ label: r.label, count: 0 }));
    
    data.forEach(job => {
        for (let i = 0; i < ranges.length; i++) {
            if (job.salary >= ranges[i].min && job.salary < ranges[i].max) {
                result[i].count++;
                break;
            }
        }
    });
    
    return result;
}

// 获取筛选后的技能数据
function getFilteredSkillsData(data, skillType) {
    const skillCount = {};
    data.forEach(job => {
        const skills = skillType === 'core' ? job.coreSkills : job.plusSkills;
        skills.forEach(skill => {
            skillCount[skill] = (skillCount[skill] || 0) + 1;
        });
    });
    return Object.entries(skillCount)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value);
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}