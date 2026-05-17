# -*- coding: utf-8 -*-
"""Boss 直聘爬虫 - 网络监听版（参考43_zhipin_xpath_picker.py）"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import Keys, launch


TARGET_URL = "https://www.zhipin.com/?city=100010000&ka=city-sites-100010000"
SEARCH_COORD = {"x": 856, "y": 100}
JOBLIST_API = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"

# 热门城市配置
CITY_CONFIG = {
    "北京": "xpath://li[normalize-space(text())=\"北京\"]",
    "上海": "xpath://li[normalize-space(text())=\"上海\"]",
    "广州": "xpath://li[normalize-space(text())=\"广州\"]",
    "深圳": "xpath://li[normalize-space(text())=\"深圳\"]",
    "杭州": "xpath://li[normalize-space(text())=\"杭州\"]",
    "天津": "xpath://li[normalize-space(text())=\"天津\"]",
    "西安": "xpath://li[normalize-space(text())=\"西安\"]",
    "苏州": "xpath://li[normalize-space(text())=\"苏州\"]",
    "武汉": "xpath://li[normalize-space(text())=\"武汉\"]",
    "厦门": "xpath://li[normalize-space(text())=\"厦门\"]",
    "长沙": "xpath://li[normalize-space(text())=\"长沙\"]",
    "成都": "xpath://li[normalize-space(text())=\"成都\"]",
    "郑州": "xpath://li[normalize-space(text())=\"郑州\"]",
    "重庆": "xpath://li[normalize-space(text())=\"重庆\"]",
}


def decode_network_text(data):
    """从网络数据收集器解码文本"""
    if not data or not data.has_data:
        return None
    raw = data.bytes
    if raw is None:
        return None
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="replace")
    if isinstance(raw, str):
        return raw
    return str(raw)


def xy_click_type_enter(page, keyword):
    """按坐标点击搜索框并输入"""
    print(f"按坐标点击搜索框: ({SEARCH_COORD['x']}, {SEARCH_COORD['y']})")
    page.actions.move_to(SEARCH_COORD).click().perform()
    page.wait(0.3)

    page.actions.combo(Keys.CTRL, "a").perform()
    page.wait(0.05)
    page.actions.press(Keys.DELETE).perform()
    page.wait(0.1)

    page.actions.type(keyword, interval=80).press(Keys.ENTER).perform()
    print("已输入并回车，等待页面 3 秒...")
    page.wait(3)


def parse_joblist_json(json_str):
    """解析 joblist.json 数据"""
    try:
        import ast
        
        # 打印响应内容用于调试
        print(f"   🔍 原始响应内容预览:")
        preview_len = min(500, len(json_str))
        print(f"   {json_str[:preview_len]}")
        
        # 先尝试用 ast.literal_eval 解析（处理可能的 Python 字典格式）
        wrapper = None
        try:
            wrapper = ast.literal_eval(json_str)
            print(f"   ✅ 用 ast.literal_eval 解析成功")
        except:
            # 如果失败，尝试用 json.loads
            try:
                wrapper = json.loads(json_str)
                print(f"   ✅ 用 json.loads 解析成功")
            except:
                pass
        
        # 检查是否有外层包装
        actual_json = json_str
        if isinstance(wrapper, dict) and wrapper.get('type') == 'string' and 'value' in wrapper:
            actual_json = wrapper['value']
            print(f"   ✅ 成功解包外层结构")
        
        # 解析实际的 JSON
        data = None
        if actual_json != json_str:
            # 已经解包了，直接解析
            try:
                data = json.loads(actual_json)
            except:
                # 如果失败，尝试用 ast.literal_eval
                try:
                    data = ast.literal_eval(actual_json)
                except:
                    pass
        else:
            # 没有包装，尝试解析
            if isinstance(wrapper, dict) and 'code' in wrapper:
                data = wrapper
            else:
                try:
                    data = json.loads(json_str)
                except:
                    try:
                        data = ast.literal_eval(json_str)
                    except:
                        pass
        
        if not data:
            print(f"   ❌ 无法解析响应数据")
            return []
        
        if data.get('code') != 0:
            print(f"   ❌ API返回错误: {data.get('message')}")
            return []
        
        zp_data = data.get('zpData', {})
        job_list = zp_data.get('jobList', [])
        
        print(f"   ✅ 成功解析 {len(job_list)} 条职位数据")
        
        parsed_jobs = []
        for job in job_list:
            job_data = {
                'jobName': job.get('jobName', ''),
                'brandName': job.get('brandName', ''),
                'salaryDesc': job.get('salaryDesc', ''),
                'cityName': job.get('cityName', ''),
                'jobDegree': job.get('jobDegree', ''),
                'jobExperience': job.get('jobExperience', ''),
                'brandScaleName': job.get('brandScaleName', ''),
                'brandIndustry': job.get('brandIndustry', ''),
                'welfareList': '|'.join(job.get('welfareList', [])) if job.get('welfareList') else '',
                'jobDesc': '',  # 后面从详情获取
                'encryptJobId': job.get('encryptJobId', ''),
            }
            parsed_jobs.append(job_data)
        
        return parsed_jobs
        
    except Exception as e:
        print(f"   ❌ JSON解析失败: {e}")
        import traceback
        traceback.print_exc()
        return []


def clean_job_desc(text):
    """清理职位描述中的CSS干扰内容"""
    import re
    if not text:
        return ''
    # 移除CSS样式内容（类似 .xxx{...} 的内容）
    text = re.sub(r'\.[a-zA-Z0-9_-]+{[^}]*}', '', text)
    # 移除单独的CSS类名定义
    text = re.sub(r'\.[a-zA-Z0-9_-]+', '', text)
    # 移除特定的干扰词
    text = re.sub(r'kanzhun', '', text)
    text = re.sub(r'BOSS直聘|Boss直聘|boss直聘|直聘', '', text, flags=re.IGNORECASE)
    text = re.sub(r'来自BOSS直聘|来自Boss直聘|来自boss直聘|来自直聘', '', text, flags=re.IGNORECASE)
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_job_detail_from_element(page):
    """从 p.desc 直接提取职位详细信息"""
    detail_data = {
        'jobDesc': '',
    }
    
    try:
        # 直接从 p.desc 提取职位详细信息（用户指定）
        desc_elem = page.ele("css:p.desc")
        if desc_elem:
            raw_text = desc_elem.text.strip() if desc_elem.text else ''
            # 清理CSS干扰内容
            detail_data['jobDesc'] = clean_job_desc(raw_text)
            if detail_data['jobDesc']:
                print(f"         职位详细信息: {detail_data['jobDesc'][:80]}...")
            else:
                print(f"         ⚠️ 提取到内容但清理后为空")
        else:
            print(f"         ⚠️ 未找到 p.desc 元素")
        
    except Exception as e:
        print(f"      ⚠️ 详情提取失败: {e}")
        import traceback
        traceback.print_exc()
    
    return detail_data


def export_to_csv(all_jobs, keyword, city, filename=None):
    """导出到CSV文件"""
    if not all_jobs:
        print("❌ 没有数据可导出")
        return None
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"zhipin_{city}_{keyword}_{timestamp}.csv"
    
    print(f"\n📊 正在导出数据到 CSV: {filename}")
    
    records = []
    for job in all_jobs:
        records.append({
            '岗位名称': job.get('jobName', ''),
            '公司名称': job.get('brandName', ''),
            '薪资范围': job.get('salaryDesc', ''),
            '工作地点': job.get('cityName', ''),
            '学历要求': job.get('jobDegree', ''),
            '经验要求': job.get('jobExperience', ''),
            '公司规模': job.get('brandScaleName', ''),
            '公司行业': job.get('brandIndustry', ''),
            '福利待遇': job.get('welfareList', ''),
            '职位信息': job.get('jobDesc', ''),
        })
    
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ CSV导出成功！共 {len(records)} 条记录")
    return filename


def switch_city(page, city_name):
    """切换城市"""
    print(f"  🌆 切换城市至: {city_name}")
    city_selector_elem = page.ele("xpath://span[normalize-space(text())=\"全国\"]")
    if not city_selector_elem:
        city_selector_elem = page.ele("xpath://span[contains(@class,'city')]")
    if not city_selector_elem:
        print("  ⚠️ 未找到城市选择器")
        return False
    
    city_selector_elem.click()
    page.wait(1)
    
    if city_name == "全国":
        quan_guo_elem = page.ele("xpath://li[contains(text(),'全国')]")
        if quan_guo_elem:
            quan_guo_elem.click()
            page.wait(1)
            return True
        page.actions.press("ESCAPE").perform()
        page.wait(0.3)
        return True
    
    city_xpath = CITY_CONFIG.get(city_name)
    if not city_xpath:
        print(f"  ⚠️ 未找到城市 '{city_name}' 的配置")
        return False
    
    city_elem = page.ele(city_xpath)
    if city_elem:
        city_elem.click()
        page.wait(2)
        return True
    
    print(f"  ⚠️ 未找到城市元素")
    return False


def crawl_one_city(page, collector, keyword, city_name, max_count):
    """爬取单个城市的完整数据，返回 (jobs列表, csv文件名)"""
    print("\n" + "=" * 80)
    print(f"🏙️ 开始爬取: {city_name}")
    print("=" * 80)
    
    if not switch_city(page, city_name):
        return [], None
    
    page.listen.stop()
    page.wait(0.3)
    page.listen.start(JOBLIST_API, method="POST")
    xy_click_type_enter(page, keyword)
    
    print("\n🔍 等待 joblist.json 响应...")
    joblist_body = None
    while 1:
        packet = page.listen.wait(timeout=30)
        if not packet:
            print("   ⚠️ 超时")
            break
        request_id = packet.request.get("request", "") if packet.request else ""
        if not request_id:
            continue
        body = decode_network_text(collector.get(request_id, data_type="response"))
        if not body:
            continue
        print(f"已捕获响应: {packet.status} {packet.url[:60]}...")
        if '您的环境存在异常' in body:
            continue
        joblist_body = body
        break
    
    if not joblist_body:
        return [], None
    
    parsed_jobs = parse_joblist_json(joblist_body)
    if not parsed_jobs:
        return [], None
    
    print(f"📊 初始 {len(parsed_jobs)} 条")
    
    all_jobs = []
    idx = 0
    
    while len(all_jobs) < max_count:
        if idx >= len(parsed_jobs):
            print(f"  📜 加载更多 (当前 {len(parsed_jobs)} 条)...")
            page.listen.stop()
            page.wait(0.3)
            
            loaded_ok = False
            for retry in range(8):
                try:
                    page.listen.start(JOBLIST_API, method="POST")
                    page.wait(0.3)
                    page.run_js("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait(2.5)
                    
                    packet = page.listen.wait(timeout=4)
                    if packet:
                        req_id = packet.request.get("request", "") if packet.request else ""
                        if req_id:
                            body = decode_network_text(collector.get(req_id, data_type="response"))
                            if body:
                                new_jobs = parse_joblist_json(body)
                                if new_jobs:
                                    old_ids = set(j.get('encryptJobId','') for j in parsed_jobs)
                                    added = 0
                                    for j in new_jobs:
                                        if j.get('encryptJobId','') not in old_ids:
                                            parsed_jobs.append(j)
                                            old_ids.add(j.get('encryptJobId',''))
                                            added += 1
                                    if added > 0:
                                        print(f"     ✅ 新增 {added} 条, 总计 {len(parsed_jobs)} 条")
                                        loaded_ok = True
                                        break
                except:
                    pass
            
            if not loaded_ok:
                print("  ⚠️ 无法获取更多数据")
                break
            continue
        
        job_items = page.eles("css:li.job-card-box")
        
        if idx >= len(job_items):
            for _ in range(5):
                try:
                    page.run_js("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait(1.5)
                    job_items = page.eles("css:li.job-card-box")
                    if idx < len(job_items):
                        break
                except:
                    break
        
        if idx >= len(job_items):
            idx += 1
            continue
        
        job_data = parsed_jobs[idx]
        name = job_data.get('jobName', '?')[:22]
        print(f"  [{len(all_jobs)+1}/{max_count}] {name}...")
        
        try:
            elem = job_items[idx]
            page.run_js("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", elem)
            page.wait(0.3)
            elem.click()
            page.wait(2)
        except:
            idx += 1
            continue
        
        try:
            d = extract_job_detail_from_element(page)
            job_data['jobDesc'] = d['jobDesc']
        except:
            job_data['jobDesc'] = ''
        
        all_jobs.append(job_data)
        idx += 1
    
    print(f"  ✅ {city_name} 完成: {len(all_jobs)} 条")
    
    csv_file = None
    if all_jobs:
        csv_file = export_to_csv(all_jobs, keyword, city_name)
    
    return all_jobs, csv_file


def main():
    print("=" * 80)
    print("🚀 Boss 直聘爬虫 - 多城市版")
    print("=" * 80)
    
    keyword = input("\n📝 岗位关键字: ").strip() or "AI"
    
    cities = list(CITY_CONFIG.keys())
    print(f"\n🏙️ 热门城市 (共{len(cities)}个):")
    for i, city in enumerate(cities, 1):
        print(f"   {i:>2}. {city}")
    
    print("\n💡 输入方式:")
    print("   - 单个城市: 北京 或 5")
    print("   - 多个城市: 1,3,5 或 北京,上海,广州")
    print("   - 全部城市: all")
    print("   - 不输入默认: 全国")
    
    city_input = input("\n📍 城市选择: ").strip()
    
    selected_cities = []
    if not city_input:
        selected_cities = ["全国"]
    elif city_input.lower() == "all":
        selected_cities = list(cities)
    else:
        parts = [p.strip() for p in city_input.replace("，", ",").split(",")]
        for p in parts:
            if p.isdigit():
                idx = int(p) - 1
                if 0 <= idx < len(cities):
                    selected_cities.append(cities[idx])
            elif p in CITY_CONFIG:
                selected_cities.append(p)
            else:
                print(f"⚠️ 无法识别: '{p}'，已跳过")
    
    if not selected_cities:
        selected_cities = ["全国"]
    
    count_input = input(f"\n📊 每个城市抓取数量 (默认100): ").strip()
    max_count = int(count_input) if count_input.isdigit() else 100
    
    print(f"\n✅ 将抓取 {len(selected_cities)} 个城市, 每个最多 {max_count} 条")
    print(f"   城市列表: {', '.join(selected_cities)}")
    
    page = launch(headless=False, xpath_picker=False, window_size=(1600, 1100))
    page.window.maximize()
    
    try:
        print("\n🌐 打开Boss直聘...")
        page.get(TARGET_URL)
        page.wait.doc_loaded(timeout=15)
        print("✅ 页面已加载")
        
        print("\n" + "=" * 80)
        print("⏰ 请扫码登录！等待60秒...")
        print("=" * 80)
        for i in range(60, 0, -10):
            print(f"  剩余 {i} 秒...", flush=True)
            page.wait(10)
        print("✅ 登录完成")
        
        collector = page.network.add_data_collector(
            ["responseCompleted"],
            data_types=["response"],
        )
        page.listen.start(JOBLIST_API, method="POST")
        
        all_csv_files = []
        for ci, city in enumerate(selected_cities, 1):
            print(f"\n{'='*80}")
            print(f"  📍 [{ci}/{len(selected_cities)}] 城市: {city}")
            print(f"{'='*80}")
            
            jobs, csv_file = crawl_one_city(page, collector, keyword, city, max_count)
            if csv_file:
                all_csv_files.append(csv_file)
            
            if ci < len(selected_cities):
                print(f"\n  ⏸️  休息 3 秒...")
                page.wait(3)
        
        print("\n" + "=" * 80)
        print("✅ 全部完成！")
        print(f"   共爬取 {len(selected_cities)} 个城市")
        print(f"   生成文件: {len(all_csv_files)} 个")
        for f in all_csv_files:
            print(f"   📄 {f}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            page.listen.stop()
        except:
            pass
        try:
            collector.remove()
        except:
            pass
        print("\n🔚 10秒后关闭浏览器...")
        page.wait(10)
        page.quit()


if __name__ == "__main__":
    main()
