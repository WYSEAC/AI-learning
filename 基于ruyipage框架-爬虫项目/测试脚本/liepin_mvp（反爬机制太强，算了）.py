# -*- coding: utf-8 -*-
"""猎聘网爬虫 - 多城市版（逐条点击详情抓取）"""

import os
import sys
import re
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import Keys, launch

CITY_PINYIN = {
    "北京": "beijing",
    "上海": "shanghai",
    "广州": "guangzhou",
    "深圳": "shenzhen",
    "杭州": "hangzhou",
    "成都": "chengdu",
    "武汉": "wuhan",
    "西安": "xian",
    "南京": "nanjing",
    "重庆": "chongqing",
    "天津": "tianjin",
    "苏州": "suzhou",
    "长沙": "changsha",
    "青岛": "qingdao",
    "大连": "dalian",
    "无锡": "wuxi",
    "宁波": "ningbo",
    "佛山": "foshan",
    "东莞": "dongguan",
    "郑州": "zhengzhou",
    "昆明": "kunming",
    "哈尔滨": "haerbin",
    "沈阳": "shenyang",
    "济南": "jinan",
    "福州": "fuzhou",
    "南昌": "nanchang",
    "合肥": "hefei",
    "石家庄": "shijiazhuang",
    "太原": "taiyuan",
    "兰州": "lanzhou",
    "贵阳": "guiyang",
    "海口": "haikou",
    "呼和浩特": "huhehaote",
    "银川": "yinchuan",
    "西宁": "xining",
    "乌鲁木齐": "wulumuqi",
    "拉萨": "lasa",
}

LIEPIN_URL = "https://www.liepin.com/"


# ---- 登录 ----
def do_login(page):
    print("\n🔑 点击登录按钮...")
    login_btn = page.ele("xpath://div[1]/div[1]/div[1]/img[1]", timeout=5)
    if not login_btn:
        login_btn = page.ele("css:div._40108uYIXT > img", timeout=3)
    if login_btn:
        login_btn.click()
        page.wait(2)
        print("   ✅ 已点击登录按钮")
    else:
        print("   ⚠️ 未找到登录按钮（可能已登录）")
        return False

    print("📱 切换到App扫码登录...")
    # 如果有VIP弹窗先关闭
    vip_close = page.ele("xpath://i[1]/img[1]", timeout=2)
    if not vip_close:
        vip_close = page.ele("css:i > img", timeout=2)
    if vip_close:
        try:
            vip_close.click()
            page.wait(0.5)
            print("   ✅ 已关闭VIP弹窗")
        except:
            pass

    app_scan = page.ele("xpath://html[1]/body[1]/section[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]", timeout=5)
    if not app_scan:
        app_scan = page.ele("css:div._40108os6BC", timeout=3)
    if app_scan:
        app_scan.click()
        page.wait(1)
        print("   ✅ 已切换到App扫码")
    else:
        print("   ⚠️ 未找到App扫码入口，尝试继续...")

    print("\n" + "=" * 60)
    print("⏰ 请用App扫描二维码登录！等待30秒...")
    print("=" * 60)
    for i in range(30, 0, -10):
        print(f"  剩余 {i} 秒...", flush=True)
        page.wait(10)

    # 再次关闭可能弹出的VIP弹窗
    vip_close2 = page.ele("xpath://i[1]/img[1]", timeout=2)
    if vip_close2:
        try:
            vip_close2.click()
            page.wait(0.5)
            print("   ✅ 关闭登录后VIP弹窗")
        except:
            pass

    print("✅ 登录完成")
    return True


# ---- 搜索关键词 ----
def search_keyword(page, keyword):
    print(f"\n🔍 搜索: {keyword}")
    search_box = page.ele('xpath://input[@placeholder="搜索职位、公司"]', timeout=8)
    if not search_box:
        search_box = page.ele('css:input[placeholder="搜索职位、公司"]', timeout=5)
    if not search_box:
        print("  ❌ 未找到搜索框")
        return None

    search_box.click()
    page.wait(0.3)
    page.actions.combo(Keys.CTRL, "a").perform()
    page.wait(0.05)
    page.actions.press(Keys.DELETE).perform()
    page.wait(0.1)
    page.actions.type(keyword, interval=80).perform()
    page.wait(0.5)

    search_btn = page.ele('xpath://span[normalize-space(text())="搜索"]', timeout=3)
    if not search_btn:
        search_btn = page.ele("css:span.search-btn--Xzc3N", timeout=3)
    if search_btn:
        search_btn.click()
    else:
        page.actions.press(Keys.ENTER).perform()
    page.wait(5)
    print(f"   🔗 当前URL: {page.url}")
    print("✅ 搜索结果已加载")
    return page


# ---- 切换城市 ----
def switch_city(page, city_name):
    print(f"\n🌆 切换城市至: {city_name}")

    other_btn = page.ele('xpath://span[normalize-space(text())="其他"]', timeout=3)
    if not other_btn:
        other_btn = page.ele("css:li#filter-option-other-city > span", timeout=3)
    if not other_btn:
        print("  ⚠️ 未找到「其他」城市按钮")
        return False

    other_btn.click()
    page.wait(1)

    city_input = page.ele('xpath://input[@placeholder="搜索城市"]', timeout=5)
    if not city_input:
        city_input = page.ele('css:input[placeholder="搜索城市"]', timeout=3)
    if not city_input:
        print("  ❌ 未找到城市搜索框")
        return False

    city_input.click()
    page.wait(0.3)
    page.actions.combo(Keys.CTRL, "a").perform()
    page.wait(0.05)
    page.actions.type(city_name, interval=60).perform()
    page.wait(1)

    # 方案1: 点击下方自动弹出的城市按钮完成切换
    suggest_city = page.ele("css:li > p", timeout=3)
    if not suggest_city:
        suggest_city = page.ele('xpath://p[normalize-space(text())="中国 ·"]', timeout=3)
    if suggest_city:
        suggest_city.click()
        page.wait(2)
        print(f"✅ 城市已切换至: {city_name}")
        return True

    # 方案2: 再次点击输入框后回车
    city_input.click()
    page.wait(0.3)
    page.actions.press(Keys.ENTER).perform()
    page.wait(3)
    print(f"✅ 城市已切换至: {city_name}")
    return True


# ---- 提取职位卡片基础信息 ----
def extract_basic_info(job_item):
    info = {
        'jobName': '',
        'cityName': '',
        'salaryDesc': '',
        'jobExperience': '',
        'jobDegree': '',
        'brandName': '',
        'brandIndustry': '',
        'brandNature': '',
        'brandScale': '',
        'jobDesc': '',
    }

    # ---- jobName ----
    try:
        el = job_item.ele("css:div[title]", timeout=1)
        if el and el.text:
            info['jobName'] = el.text.strip()
    except: pass

    # ---- cityName ----
    try:
        el = job_item.ele("css:span.ellipsis-1", timeout=1)
        if el and el.text and ('·' in el.text or '区' in el.text or '市' in el.text):
            info['cityName'] = el.text.strip()
    except: pass

    # ---- salaryDesc ----
    try:
        el = job_item.ele("css:span._40108E8PWS", timeout=1)
        if el and el.text:
            info['salaryDesc'] = el.text.strip()
    except: pass

    # ---- jobExperience / jobDegree ----
    try:
        tag_els = job_item.eles("css:span._40108hJbMl")
        for idx, el in enumerate(tag_els):
            if el and el.text:
                t = el.text.strip()
                if idx == 0:
                    info['jobExperience'] = t
                elif idx == 1:
                    info['jobDegree'] = t
    except: pass

    # ---- company tag container ----
    try:
        company_tag = job_item.ele("css:div._40108vBGCE", timeout=1)
        if company_tag:
            # brandName
            try:
                name_el = company_tag.ele("css:span._40108K6Y1c.ellipsis-1", timeout=1)
                if name_el and name_el.text:
                    info['brandName'] = name_el.text.strip()
            except: pass

            # brandIndustry / brandNature / brandScale
            try:
                tag_spans = company_tag.eles("css:span:nth-of-type(1),span:nth-of-type(2),span:nth-of-type(3)")
                texts = []
                for s in tag_spans:
                    if s and s.text:
                        t = s.text.strip()
                        if t != info.get('brandName', ''):
                            texts.append(t)
                if len(texts) >= 3:
                    info['brandIndustry'] = texts[0]
                    info['brandNature'] = texts[1]
                    info['brandScale'] = texts[2]
            except: pass
    except: pass

    return info


# ---- 点击职位打开详情页抓取 ----
def extract_detail_from_new_tab(page, job_item):
    try:
        # 先移鼠标到最左侧
        try:
            page.actions.move_to(10, 300).perform()
            page.wait(0.2)
        except:
            pass

        # 点击职位名称打开新标签页
        name_el = job_item.ele("css:div[title]", timeout=2)
        if not name_el:
            return ''

        page.run_js("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", name_el)
        page.wait(0.3)

        # 点击在新标签页打开
        detail_tab = name_el.click.for_new_tab()
        if not detail_tab:
            name_el.click()
            page.wait(5)
            return ''

        detail_tab.wait.doc_loaded(timeout=10)
        detail_tab.wait(2)

        # 提取详情
        desc = ''
        try:
            detail_el = detail_tab.ele("css:section.job-intro-container", timeout=5)
            if not detail_el:
                detail_el = detail_tab.ele("xpath://content[1]/section[2]", timeout=3)
            if detail_el and detail_el.text:
                desc = re.sub(r'\s+', ' ', detail_el.text.strip())
        except:
            pass

        detail_tab.close()
        page.wait(0.5)
        return desc
    except:
        return ''


# ---- 抓取一页 ----
def grab_one_page(page, all_jobs, max_count):
    print(f"  🔍 查找职位列表...")

    page.run_js("window.scrollTo(0, 0);")
    page.wait(0.5)
    page.run_js("window.scrollTo(0, 500);")
    page.wait(0.5)
    page.run_js("window.scrollTo(0, 0);")
    page.wait(1)

    # 将鼠标移到最左侧，避免经过下拉列表
    try:
        page.actions.move_to(10, 300).perform()
        page.wait(0.3)
    except:
        pass

    job_items = page.eles("css:div.job-card-pc-container")
    if not job_items:
        job_items = page.eles("css:div._40108Nrnc3.job-card-pc-container")
    if not job_items:
        job_items = page.eles("css:div[class*='job-card']")

    print(f"  📋 找到 {len(job_items)} 条职位")

    if not job_items:
        print(f"  ⚠️ 无职位")
        print("     → 页面等待 60 秒供人工检查...")
        page.wait(60)
        return 0

    grabbed = 0
    skip_count = 0

    for idx in range(len(job_items)):
        if len(all_jobs) >= max_count:
            break
        try:
            item = job_items[idx]
            page.run_js("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", item)
            page.wait(0.3)

            job = extract_basic_info(item)
            name = job['jobName'] or f'(无名{idx+1})'

            job['jobDesc'] = extract_detail_from_new_tab(page, item)

            all_jobs.append(job)
            grabbed += 1

            dl = len(job.get('jobDesc', ''))
            st = f"📝{dl}字" if dl else "⚠无详情"
            print(f"  [{len(all_jobs)}/{max_count}] {name[:22]}... {st} | "
                  f"{job.get('brandName','')[:8]} | {job.get('salaryDesc','')[:10]}")

        except Exception:
            skip_count += 1

    print(f"  📊 本页: {grabbed} 条, 跳过 {skip_count}")
    return grabbed


# ---- 翻页 ----
def go_next_page(page):
    page.run_js("window.scrollTo(0, document.body.scrollHeight);")
    page.wait(1)

    # 优先用 CSS，不受页码数量变化影响
    next_btn = page.ele("css:li[title='Next Page'] > button[type='button']", timeout=3)
    if not next_btn:
        next_btn = page.ele("css:li.ant-pagination-next", timeout=2)
    if not next_btn:
        next_btn = page.ele("css:li[title='Next Page'] > button", timeout=2)
    if not next_btn:
        next_btn = page.ele("css:li[class*='next'] button", timeout=2)
    if not next_btn:
        next_btn = page.ele("css:li[class*='next']", timeout=2)
    if not next_btn:
        next_btn = page.ele("css:button[class*='next']", timeout=2)
    if not next_btn:
        next_btn = page.ele("css:a[class*='next']", timeout=2)

    if next_btn:
        try:
            page.run_js("arguments[0].scrollIntoView({behavior:'instant',block:'center'});", next_btn)
            page.wait(0.5)
            next_btn.click()
            page.wait(4)
            return True
        except:
            print("  ⚠️ 点击下一页失败")
    else:
        print("  ⚠️ 未找到「下一页」按钮")
        print(f"   🔗 当前URL: {page.url}")
    return False


# ---- 导出CSV ----
def export_csv(jobs, keyword, city):
    if not jobs:
        print("  ❌ 无数据，未生成CSV")
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"liepin_{city}_{keyword}_{ts}.csv"
    print(f"\n📊 导出: {fname}")
    records = []
    for j in jobs:
        records.append({
            '岗位名称': j.get('jobName', ''),
            '公司名称': j.get('brandName', ''),
            '薪资范围': j.get('salaryDesc', ''),
            '工作城市': j.get('cityName', ''),
            '经验要求': j.get('jobExperience', ''),
            '学历要求': j.get('jobDegree', ''),
            '公司行业': j.get('brandIndustry', ''),
            '公司性质': j.get('brandNature', ''),
            '公司规模': j.get('brandScale', ''),
            '职位描述': j.get('jobDesc', ''),
        })
    pd.DataFrame(records).to_csv(fname, index=False, encoding='utf-8-sig')
    print(f"✅ 导出 {len(records)} 条")
    return fname


# ---- 单城市爬取 ----
def crawl_one_city(page, keyword, city_name, max_count):
    print("\n" + "=" * 80)
    print(f"🏙️ 开始爬取: {city_name}")
    print("=" * 80)

    city_pinyin = CITY_PINYIN.get(city_name)
    if not city_pinyin:
        print(f"  ❌ 未找到城市「{city_name}」的拼音映射")
        return [], None

    city_url = f"https://www.liepin.com/zhaopin/?city={city_pinyin}&key={keyword}"
    print(f"  🌐 访问: {city_url}")
    page.get(city_url)
    page.wait.doc_loaded(timeout=10)
    page.wait(3)
    print("  ✅ 城市页面已加载")

    if not switch_city(page, city_name):
        print(f"  ❌ {city_name} 城市切换失败")
        return [], None

    if not search_keyword(page, keyword):
        print(f"  ❌ {city_name} 搜索失败")
        return [], None

    all_jobs = []
    same_count = 0
    prev_total = 0

    while len(all_jobs) < max_count:
        grab_one_page(page, all_jobs, max_count)

        if len(all_jobs) == prev_total:
            same_count += 1
            if same_count >= 3:
                print("  ⚠️ 连续3页无新数据，结束")
                break
        else:
            same_count = 0
        prev_total = len(all_jobs)

        if len(all_jobs) >= max_count:
            break

        print(f"\n  📄 翻第 {same_count + 2} 页... ({len(all_jobs)}/{max_count})")
        if not go_next_page(page):
            print("  ⚠️ 无下一页，结束")
            break

    print(f"\n  ✅ {city_name} 完成: {len(all_jobs)} 条")
    csv_file = None
    if all_jobs:
        csv_file = export_csv(all_jobs, keyword, city_name)
    return all_jobs, csv_file


# ---- 主函数 ----
def main():
    print("=" * 80)
    print("🚀 猎聘网爬虫 - 多城市版")
    print("=" * 80)

    keyword = input("\n📝 岗位关键字: ").strip() or "AI"

    cities = list(CITY_PINYIN.keys())
    print(f"\n🏙️ 热门城市 (共{len(cities)}个):")
    for i, city in enumerate(cities, 1):
        print(f"   {i:>2}. {city}")

    print("\n💡 输入方式:")
    print("   - 单个城市: 北京 或 5")
    print("   - 多个城市: 1,3,5 或 北京,上海,广州")
    print("   - 全部城市: all")

    city_input = input("\n📍 城市选择: ").strip()

    selected_cities = []
    if not city_input:
        selected_cities = ["北京"]
    elif city_input.lower() == "all":
        selected_cities = list(cities)
    else:
        parts = [p.strip() for p in city_input.replace("，", ",").split(",")]
        for p in parts:
            if p.isdigit():
                idx = int(p) - 1
                if 0 <= idx < len(cities):
                    selected_cities.append(cities[idx])
            elif p in CITY_PINYIN:
                selected_cities.append(p)
            else:
                print(f"⚠️ 无法识别: '{p}'，已跳过")

    if not selected_cities:
        selected_cities = ["北京"]

    count_input = input(f"\n📊 每个城市抓取数量 (默认20): ").strip()
    max_count = int(count_input) if count_input.isdigit() else 20

    print(f"\n✅ 将抓取 {len(selected_cities)} 个城市, 每个最多 {max_count} 条")
    print(f"   城市列表: {', '.join(selected_cities)}")

    page = launch(headless=False, xpath_picker=False, window_size=(1600, 1100))
    page.window.maximize()

    try:
        print(f"\n🌐 打开猎聘网...")
        page.get(LIEPIN_URL)
        page.wait.doc_loaded(timeout=15)
        print("✅ 页面已加载")

        do_login(page)

        all_csv_files = []
        for ci, city in enumerate(selected_cities, 1):
            print(f"\n{'='*80}")
            print(f"  📍 [{ci}/{len(selected_cities)}] 城市: {city}")
            print(f"{'='*80}")

            jobs, csv_file = crawl_one_city(page, keyword, city, max_count)
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

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 10秒后关闭浏览器...")
        page.wait(10)
        page.quit()


if __name__ == "__main__":
    main()
