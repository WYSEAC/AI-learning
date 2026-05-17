"""
ADLP框架 - Web可视化界面
使用 Flask 提供交互式学习规划界面
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

try:
    from flask import Flask, render_template_string, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

if HAS_FLASK:
    from core.engine import ADLPEngine
    app = Flask(__name__)
    engine = ADLPEngine()

    INDEX_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ADLP - AI驱动的学习项目框架</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
.gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.card { @apply bg-white rounded-xl shadow-lg p-6; }
.phase-card { @apply border-l-4 p-4 rounded-r-lg mb-3; }
.phase-1 { @apply border-blue-500 bg-blue-50; }
.phase-2 { @apply border-purple-500 bg-purple-50; }
.phase-3 { @apply border-green-500 bg-green-50; }
.phase-4 { @apply border-amber-500 bg-amber-50; }
.phase-5 { @apply border-red-500 bg-red-50; }
</style>
</head>
<body class="bg-gray-50 min-h-screen">
<div class="gradient-bg text-white p-6 shadow-lg">
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold">🎯 ADLP框架</h1>
    <p class="opacity-90 mt-2">AI-Driven Learning Project Framework - 数据驱动的个性化学习规划</p>
  </div>
</div>

<div class="max-w-6xl mx-auto p-6">
  <div class="card mb-6">
    <h2 class="text-xl font-semibold mb-4">📋 快速开始</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div><label class="block text-sm mb-1">目标岗位</label>
        <select id="keyword" class="w-full border rounded px-3 py-2">
          <option>AI工程师</option><option>机器学习工程师</option><option>深度学习工程师</option>
          <option>NLP工程师</option><option>计算机视觉工程师</option><option>AI产品经理</option>
          <option>AI训练师</option><option>推荐算法工程师</option>
        </select></div>
      <div><label class="block text-sm mb-1">姓名</label>
        <input id="name" class="w-full border rounded px-3 py-2" placeholder="学习者"></div>
      <div><label class="block text-sm mb-1">背景</label>
        <input id="background" class="w-full border rounded px-3 py-2" placeholder="有2年Java开发经验"></div>
      <div><label class="block text-sm mb-1">每周学习时长</label>
        <input id="weekly_hours" type="number" class="w-full border rounded px-3 py-2" value="20"></div>
    </div>
    <button onclick="runFull()" class="mt-4 bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700">🚀 运行完整ADLP流程</button>
    <button onclick="runAnalyze()" class="mt-4 ml-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">📊 仅分析</button>
  </div>

  <div id="loading" class="hidden text-center py-12">
    <div class="animate-spin w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
    <p>正在执行ADLP流程...</p>
  </div>

  <div id="results" class="hidden">
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
      <div class="phase-card phase-1"><div class="font-bold">📊 阶段一</div><div class="text-sm">需求分析</div><div id="phase1-status">✅</div></div>
      <div class="phase-card phase-2"><div class="font-bold">👤 阶段二</div><div class="text-sm">画像构建</div><div id="phase2-status">✅</div></div>
      <div class="phase-card phase-3"><div class="font-bold">📐 阶段三</div><div class="text-sm">路径设计</div><div id="phase3-status">✅</div></div>
      <div class="phase-card phase-4"><div class="font-bold">🚀 阶段四</div><div class="text-sm">项目实践</div><div id="phase4-status">✅</div></div>
      <div class="phase-card phase-5"><div class="font-bold">💼 阶段五</div><div class="text-sm">求职准备</div><div id="phase5-status">✅</div></div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div class="card"><h3 class="font-semibold mb-3">🎯 能力雷达图</h3><canvas id="radarChart" height="250"></canvas></div>
      <div class="card"><h3 class="font-semibold mb-3">📊 技能缺口分析</h3><div id="gapAnalysis"></div></div>
    </div>

    <div class="card mb-6"><h3 class="font-semibold mb-3">📐 学习路径</h3><div id="learningPath"></div></div>
    <div class="card mb-6"><h3 class="font-semibold mb-3">💼 求职准备</h3><div id="careerPrep"></div></div>
  </div>
</div>

<script>
let radarChart = null;

async function callAPI(endpoint, data) {
  const resp = await fetch(endpoint, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  return resp.json();
}

async function runFull() {
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');
  const data = {keyword:document.getElementById('keyword').value,name:document.getElementById('name').value||'学习者',background:document.getElementById('background').value||'有编程基础',weekly_hours:parseInt(document.getElementById('weekly_hours').value)||20};
  const result = await callAPI('/api/full', data);
  renderResults(result);
}

async function runAnalyze() {
  const data = {keyword:document.getElementById('keyword').value};
  const result = await callAPI('/api/analyze', data);
  document.getElementById('phase1-status').textContent = '✅';
  document.getElementById('results').classList.remove('hidden');
}

function renderResults(r) {
  document.getElementById('loading').classList.add('hidden');
  document.getElementById('results').classList.remove('hidden');
  
  if (r.skill_gaps) {
    let html = '<div class="space-y-2">';
    r.skill_gaps.slice(0,8).forEach(g => {
      const w = Math.min(100, (g.hours||40)/200*100);
      html += `<div><div class="flex justify-between text-sm"><span>${g.skill}</span><span class="text-gray-500">${g.hours}h | ${g.current}→${g.target}</span></div><div class="bg-gray-200 rounded h-2 mt-1"><div class="bg-blue-500 rounded h-2" style="width:${w}%"></div></div></div>`;
    });
    html += '</div>';
    document.getElementById('gapAnalysis').innerHTML = html;
  }
  
  if (r.learning_path?.phases) {
    let html = '<div class="space-y-3">';
    r.learning_path.phases.forEach((p,i) => {
      html += `<div class="phase-card phase-${i%5+1}"><div class="font-bold">${p.name} (${p.duration_weeks}周)</div><div class="text-sm">技能: ${(p.skills_to_learn||[]).slice(0,5).join(', ')}</div></div>`;
    });
    html += '</div>';
    document.getElementById('learningPath').innerHTML = html;
  }
  
  if (r.career_prep?.resume) {
    document.getElementById('careerPrep').innerHTML = `<div class="prose max-w-none text-sm"><pre class="whitespace-pre-wrap bg-gray-50 p-4 rounded">${r.career_prep.resume.slice(0,1000)}${r.career_prep.resume.length>1000?'...':''}</pre></div>`;
  }
  
  if (r.market_data) {
    if (radarChart) radarChart.destroy();
    const ctx = document.getElementById('radarChart').getContext('2d');
    const gapNames = (r.skill_gaps||[]).slice(0,6).map(g=>g.skill);
    const gapHours = (r.skill_gaps||[]).slice(0,6).map(g=>g.hours||0);
    radarChart = new Chart(ctx, {type:'radar',data:{labels:gapNames,datasets:[{label:'所需学习时长(小时)',data:gapHours,backgroundColor:'rgba(139,92,246,0.3)',borderColor:'rgb(139,92,246)'}]},options:{responsive:true,scales:{r:{beginAtZero:true,max:Math.max(200,...gapHours)}}}});
  }
}
</script>
</body></html>'''

    @app.route('/')
    def index():
        return render_template_string(INDEX_HTML)

    @app.route('/api/analyze', methods=['POST'])
    def api_analyze():
        data = request.json
        market = engine.analyze_market(keyword=data.get('keyword','AI工程师'))
        target = engine.define_target(data.get('keyword','AI工程师'))
        return jsonify({
            'market_data': {'keyword':market.keyword,'total_jobs':market.total_jobs,'avg_salary':market.avg_salary},
            'target': {'title':target.title,'entry_barrier':target.entry_barrier,'growth_outlook':target.growth_outlook}
        })

    @app.route('/api/full', methods=['POST'])
    def api_full():
        data = request.json
        result = engine.run_full(
            keyword=data.get('keyword','AI工程师'),
            name=data.get('name','学习者'),
            background=data.get('background','有编程基础'),
            experience=data.get('experience',1),
            weekly_hours=data.get('weekly_hours',20),
            motivation=data.get('motivation',7),
            persistence=data.get('persistence',6)
        )
        return jsonify(result)

    @app.route('/api/health')
    def health():
        return jsonify({'status':'ok','version':'1.0.0'})

def main():
    if HAS_FLASK:
        print("🌐 ADLP Web界面启动: http://localhost:5001")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ 需要安装Flask: pip install flask")
        print("💡 使用命令行工具: python cli.py --help")

if __name__ == '__main__':
    main()
