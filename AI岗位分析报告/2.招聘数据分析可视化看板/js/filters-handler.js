let currentFilters = {
    type: 'all',
    city: 'all',
    experience: 'all',
    education: 'all',
    companySize: 'all'
};

function initFilters() {
    const data = getOriginalData();
    
    const typeCount = {};
    data.forEach(job => {
        typeCount[job.type] = (typeCount[job.type] || 0) + 1;
    });
    const topTypes = Object.entries(typeCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 15)
        .map(([type]) => type);
    
    const cities = [...new Set(data.map(j => j.city))].sort();
    const experiences = ['经验不限', '1-3年', '3-5年', '5-10年', '10年以上'];
    const educations = ['学历不限', '大专', '本科', '硕士', '博士'];
    const companySizes = ['0-20人', '20-99人', '100-499人', '500-999人', '1000-9999人', '10000人以上'];
    
    populateSelect('typeFilter', topTypes);
    populateSelect('cityFilter', cities);
    populateSelect('expFilter', experiences);
    populateSelect('eduFilter', educations);
    populateSelect('sizeFilter', companySizes);
    
    document.getElementById('typeFilter').addEventListener('change', applyFilters);
    document.getElementById('cityFilter').addEventListener('change', applyFilters);
    document.getElementById('expFilter').addEventListener('change', applyFilters);
    document.getElementById('eduFilter').addEventListener('change', applyFilters);
    document.getElementById('sizeFilter').addEventListener('change', applyFilters);
}

function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    const firstOption = select.options[0];
    select.innerHTML = '';
    select.appendChild(firstOption);
    
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        select.appendChild(opt);
    });
}

function applyFilters() {
    const data = getOriginalData();
    
    const typeFilter = document.getElementById('typeFilter').value;
    const cityFilter = document.getElementById('cityFilter').value;
    const expFilter = document.getElementById('expFilter').value;
    const eduFilter = document.getElementById('eduFilter').value;
    const sizeFilter = document.getElementById('sizeFilter').value;
    
    currentFilters = {
        type: typeFilter,
        city: cityFilter,
        experience: expFilter,
        education: eduFilter,
        companySize: sizeFilter
    };
    
    currentFilteredData = data.filter(job => {
        if (typeFilter !== 'all' && job.type !== typeFilter) return false;
        if (cityFilter !== 'all' && job.city !== cityFilter) return false;
        if (expFilter !== 'all' && job.experience !== expFilter) return false;
        if (eduFilter !== 'all' && job.education !== eduFilter) return false;
        if (sizeFilter !== 'all' && job.companySize !== sizeFilter) return false;
        return true;
    });
    
    updateAllCharts();
    setCurrentJobType(typeFilter !== 'all' ? typeFilter : null);
}

function resetFilters() {
    document.getElementById('typeFilter').value = 'all';
    document.getElementById('cityFilter').value = 'all';
    document.getElementById('expFilter').value = 'all';
    document.getElementById('eduFilter').value = 'all';
    document.getElementById('sizeFilter').value = 'all';
    
    currentFilters = {
        type: 'all',
        city: 'all',
        experience: 'all',
        education: 'all',
        companySize: 'all'
    };
    
    currentFilteredData = [...getOriginalData()];
    setCurrentJobType(null);
    updateAllCharts();
}
