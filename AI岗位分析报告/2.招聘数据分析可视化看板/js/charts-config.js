let charts = {};
let currentJobType = null;

function initAllCharts() {
    charts.salaryChart = echarts.init(document.getElementById('salaryChart'));
    charts.expChart = echarts.init(document.getElementById('expChart'));
    charts.eduChart = echarts.init(document.getElementById('eduChart'));
    charts.sizeChart = echarts.init(document.getElementById('sizeChart'));
    charts.industryChart = echarts.init(document.getElementById('industryChart'));
    charts.coreSkillChart = echarts.init(document.getElementById('coreSkillChart'));
    charts.plusSkillChart = echarts.init(document.getElementById('plusSkillChart'));
    charts.typeChart = echarts.init(document.getElementById('typeChart'));
    charts.jobSalaryChart = echarts.init(document.getElementById('jobSalaryChart'));
    charts.eduSalaryChart = echarts.init(document.getElementById('eduSalaryChart'));
    charts.salarySkillChart = echarts.init(document.getElementById('salarySkillChart'));
    
    window.addEventListener('resize', () => {
        Object.values(charts).forEach(chart => chart.resize());
    });
}

function updateAllCharts() {
    const data = getFilteredData();
    updateOverviewCards(data);
    
    updateSalaryChart(data);
    updateExpChart(data);
    updateEduChart(data);
    updateSizeChart(data);
    updateIndustryChart(data);
    updateCoreSkillChart(data);
    updatePlusSkillChart(data);
    updateTypeChart(data);
    updateJobSalaryChart(data);
    updateEduSalaryChart(data);
    updateSalarySkillChart(data);
}

function updateSalaryChart(data) {
    const salaryDist = getSalaryDistribution(data);
    const option = {
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: salaryDist.map(d => d.label), axisLabel: { rotate: 45 } },
        yAxis: { type: 'value' },
        series: [{
            name: '岗位数',
            type: 'bar',
            data: salaryDist.map(d => d.count),
            itemStyle: { color: '#667eea' },
            barWidth: '60%'
        }]
    };
    charts.salaryChart.setOption(option);
}

function updateExpChart(data) {
    const expData = aggregateByExperience(data);
    const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['岗位数', '平均薪资'] },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: expData.map(d => d.name) },
        yAxis: [{ type: 'value', name: '岗位数' }, { type: 'value', name: '平均薪资(K)' }],
        series: [
            {
                name: '岗位数',
                type: 'bar',
                data: expData.map(d => d.count),
                itemStyle: { color: '#667eea' }
            },
            {
                name: '平均薪资',
                type: 'line',
                yAxisIndex: 1,
                data: expData.map(d => d.avgSalary),
                itemStyle: { color: '#ee6666' },
                smooth: true
            }
        ]
    };
    charts.expChart.setOption(option);
}

function updateEduChart(data) {
    const eduData = aggregateByEducation(data);
    const option = {
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [{
            name: '学历要求',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
            label: { show: true, formatter: '{b}: {c} ({d}%)' },
            emphasis: { label: { fontSize: '16', fontWeight: 'bold' } },
            data: eduData
        }]
    };
    charts.eduChart.setOption(option);
}

function updateSizeChart(data) {
    const sizeData = aggregateByCompanySize(data);
    const option = {
        tooltip: { trigger: 'item' },
        series: [{
            name: '公司规模',
            type: 'pie',
            radius: '70%',
            data: sizeData,
            emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
        }]
    };
    charts.sizeChart.setOption(option);
}

function updateIndustryChart(data) {
    const industryData = aggregateByIndustry(data);
    const option = {
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: { type: 'category', data: industryData.map(d => d.name).reverse() },
        series: [{
            name: '岗位数',
            type: 'bar',
            data: industryData.map(d => d.value).reverse(),
            itemStyle: { color: '#91cc75' }
        }]
    };
    charts.industryChart.setOption(option);
}

function updateCoreSkillChart(data) {
    const skillData = getFilteredSkillsData(data, 'core').slice(0, 30);
    const option = {
        tooltip: {},
        series: [{
            type: 'wordCloud',
            shape: 'circle',
            gridSize: 2,
            sizeRange: [12, 50],
            rotationRange: [-45, 45],
            textStyle: {
                fontFamily: 'sans-serif',
                fontWeight: 'bold',
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 100 + 100),
                        Math.round(Math.random() * 80 + 80),
                        Math.round(Math.random() * 150 + 100)
                    ].join(',') + ')';
                }
            },
            emphasis: { textStyle: { shadowBlur: 10, shadowColor: '#333' } },
            data: skillData
        }]
    };
    charts.coreSkillChart.setOption(option);
}

function updatePlusSkillChart(data) {
    const skillData = getFilteredSkillsData(data, 'plus').slice(0, 30);
    const option = {
        tooltip: {},
        series: [{
            type: 'wordCloud',
            shape: 'circle',
            gridSize: 2,
            sizeRange: [12, 50],
            rotationRange: [-45, 45],
            textStyle: {
                fontFamily: 'sans-serif',
                fontWeight: 'bold',
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 80 + 100),
                        Math.round(Math.random() * 150 + 100),
                        Math.round(Math.random() * 80 + 80)
                    ].join(',') + ')';
                }
            },
            emphasis: { textStyle: { shadowBlur: 10, shadowColor: '#333' } },
            data: skillData
        }]
    };
    charts.plusSkillChart.setOption(option);
}

function updateTypeChart(data) {
    const typeData = aggregateByJobType(data).slice(0, 10);
    const option = {
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [{
            name: '岗位类型',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
            data: typeData
        }]
    };
    charts.typeChart.setOption(option);
}

function updateJobSalaryChart(data) {
    const jobTypeData = {};
    data.forEach(job => {
        if (!jobTypeData[job.type]) {
            jobTypeData[job.type] = { count: 0, totalSalary: 0 };
        }
        jobTypeData[job.type].count++;
        jobTypeData[job.type].totalSalary += job.salary;
    });
    
    const chartData = Object.entries(jobTypeData)
        .map(([type, info]) => ({
            name: type,
            count: info.count,
            avgSalary: Math.round(info.totalSalary / info.count)
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 12);
    
    const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['岗位数', '平均薪资(K)'] },
        grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
        xAxis: { type: 'category', data: chartData.map(d => d.name), axisLabel: { rotate: 45 } },
        yAxis: [{ type: 'value', name: '岗位数' }, { type: 'value', name: '平均薪资(K)' }],
        series: [
            {
                name: '岗位数',
                type: 'bar',
                data: chartData.map(d => d.count),
                itemStyle: { color: '#667eea' }
            },
            {
                name: '平均薪资(K)',
                type: 'line',
                yAxisIndex: 1,
                data: chartData.map(d => d.avgSalary),
                itemStyle: { color: '#ee6666' },
                smooth: true
            }
        ]
    };
    charts.jobSalaryChart.setOption(option);
}

function updateEduSalaryChart(data) {
    const eduOrder = ['学历不限', '高中及以下', '大专', '本科', '硕士', '博士'];
    const eduData = {};
    eduOrder.forEach(edu => eduData[edu] = { count: 0, totalSalary: 0 });
    
    data.forEach(job => {
        if (eduData[job.education]) {
            eduData[job.education].count++;
            eduData[job.education].totalSalary += job.salary;
        }
    });
    
    const chartData = eduOrder
        .map(edu => ({
            name: edu,
            count: eduData[edu].count,
            avgSalary: eduData[edu].count > 0 ? Math.round(eduData[edu].totalSalary / eduData[edu].count) : 0
        }))
        .filter(d => d.count > 0);
    
    const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['岗位数', '平均薪资(K)'] },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: chartData.map(d => d.name) },
        yAxis: [{ type: 'value', name: '岗位数' }, { type: 'value', name: '平均薪资(K)' }],
        series: [
            {
                name: '岗位数',
                type: 'bar',
                data: chartData.map(d => d.count),
                itemStyle: { color: '#91cc75' }
            },
            {
                name: '平均薪资(K)',
                type: 'line',
                yAxisIndex: 1,
                data: chartData.map(d => d.avgSalary),
                itemStyle: { color: '#ee6666' },
                smooth: true
            }
        ]
    };
    charts.eduSalaryChart.setOption(option);
}

function updateSalarySkillChart(data) {
    const skillSalary = {};
    data.forEach(job => {
        job.coreSkills.forEach(skill => {
            if (!skillSalary[skill]) {
                skillSalary[skill] = { count: 0, totalSalary: 0 };
            }
            skillSalary[skill].count++;
            skillSalary[skill].totalSalary += job.salary;
        });
    });
    
    const topSkills = Object.entries(skillSalary)
        .map(([skill, info]) => ({
            name: skill,
            count: info.count,
            avgSalary: Math.round(info.totalSalary / info.count)
        }))
        .sort((a, b) => b.avgSalary - a.avgSalary)
        .slice(0, 15);
    
    const option = {
        tooltip: { trigger: 'axis' },
        legend: { data: ['出现次数', '平均薪资(K)'] },
        grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
        xAxis: { type: 'category', data: topSkills.map(d => d.name), axisLabel: { rotate: 45 } },
        yAxis: [{ type: 'value', name: '出现次数' }, { type: 'value', name: '平均薪资(K)' }],
        series: [
            {
                name: '出现次数',
                type: 'bar',
                data: topSkills.map(d => d.count),
                itemStyle: { color: '#fac858' }
            },
            {
                name: '平均薪资(K)',
                type: 'line',
                yAxisIndex: 1,
                data: topSkills.map(d => d.avgSalary),
                itemStyle: { color: '#ee6666' },
                smooth: true
            }
        ]
    };
    charts.salarySkillChart.setOption(option);
}

function setCurrentJobType(jobType) {
    currentJobType = jobType;
    updateJobTypeDetails();
}

function updateJobTypeDetails() {
    const jobTypeDetails = getJobTypeDetails();
    const detailsContainer = document.getElementById('jobTypeDetails');
    
    if (!currentJobType || !jobTypeDetails[currentJobType]) {
        detailsContainer.innerHTML = '<p style="text-align:center;color:#666;">请从上方岗位类型筛选器选择一个岗位查看详情</p>';
        return;
    }
    
    const details = jobTypeDetails[currentJobType];
    detailsContainer.innerHTML = `
        <div class="details-header">
            <h3>${currentJobType}</h3>
            <div class="details-stats">
                <span>岗位数: ${details.count}</span>
                <span>平均薪资: ${details.avgSalary}K</span>
            </div>
        </div>
        <div class="details-content">
            <div class="details-section">
                <h4>📋 主要职责</h4>
                <ul>
                    ${details.responsibilities.length > 0 ? 
                        details.responsibilities.map(r => `<li>${r}</li>`).join('') : 
                        '<li>暂无数据</li>'}
                </ul>
            </div>
            <div class="details-section">
                <h4>💻 技术要求</h4>
                <ul>
                    ${details.techRequirements.length > 0 ? 
                        details.techRequirements.map(t => `<li>${t}</li>`).join('') : 
                        '<li>暂无数据</li>'}
                </ul>
            </div>
        </div>
    `;
}
