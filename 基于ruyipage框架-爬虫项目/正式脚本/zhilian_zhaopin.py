# -*- coding: utf-8 -*-
"""智联招聘爬虫 - 多城市版"""

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


def do_login(page):
    print("\n🔑 点击登录按钮...")
    login_btn = page.ele("css:a.home-header__c-no-login", timeout=5)
    if not login_btn:
        login_btn = page.ele("xpath://header[1]/div[1]/div[2]/a[2]", timeout=3)
    if login_btn:
        login_btn.click()
        page.wait(2)
        print("   ✅ 已点击登录按钮")
    else:
        print("   ⚠️ 未找到登录按钮（可能已登录）")
        return False

    print("📱 点击微信扫码登录...")
    wechat_btn = page.ele("css:div.zppp-panel-normal-bar__img", timeout=5)
    if not wechat_btn:
        wechat_btn = page.ele("xpath:/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]", timeout=5)
    if wechat_btn:
        wechat_btn.click()
        page.wait(1)
        print("   ✅ 已点击微信扫码")
    else:
        print("   ⚠️ 未找到微信扫码入口")

    print("\n" + "=" * 60)
    print("⏰ 请用微信扫描二维码登录！等待30秒...")
    print("=" * 60)
    for i in range(30, 0, -10):
        print(f"  剩余 {i} 秒...", flush=True)
        page.wait(10)
    print("✅ 登录完成")
    return True


def search_keyword(page, keyword):
    print(f"\n🔍 搜索: {keyword}")
    search_box = page.ele('xpath://input[@placeholder="请输入关键词,例如:JAVA,销售代表,行政助理等"]', timeout=8)
    if not search_box:
        search_box = page.ele('css:input[placeholder="请输入关键词,例如:JAVA,销售代表,行政助理等"]', timeout=5)
    if not search_box:
        print("  ❌ 未找到搜索框")
        return None, None
    search_box.click()
    page.wait(0.3)
    page.actions.combo(Keys.CTRL, "a").perform()
    page.wait(0.05)
    page.actions.press(Keys.DELETE).perform()
    page.wait(0.1)
    page.actions.type(keyword, interval=80).perform()
    page.wait(0.5)
    search_btn = page.ele("css:a.zp-search__btn.zp-search__btn--blue", timeout=3)
    if search_btn:
        print("   🔘 点击搜索，等待新标签页打开...")
        new_tab = search_btn.click.for_new_tab()
        if not new_tab:
            search_btn.click()
            page.wait(8)
            return page, page.url
    else:
        page.actions.press(Keys.ENTER).perform()
        page.wait(8)
        return page, page.url

    if new_tab:
        new_tab.wait.doc_loaded(timeout=10)
        new_tab.wait(3)
        print(f"   🔗 搜索结果URL: {new_tab.url}")
        print("✅ 搜索结果已加载")
        return new_tab, new_tab.url

    return page, page.url


def extract_basic_info(job_item):
    info = {
        'jobName': '',
        'brandName': '',
        'salaryDesc': '',
        'cityName': '',
        'jobExperience': '',
        'jobDegree': '',
        'brandNature': '',
        'brandScale': '',
        'brandIndustry': '',
        'companyTag': '',
        'jobDesc': '',
    }

    # ---- jobName: a.jobinfo__name ----
    try:
        el = job_item.ele("css:a.jobinfo__name", timeout=1)
        if el and el.text:
            info['jobName'] = el.text.strip()
    except: pass

    # ---- salaryDesc: p.jobinfo__salary ----
    try:
        el = job_item.ele("css:p.jobinfo__salary", timeout=1)
        if el and el.text:
            info['salaryDesc'] = el.text.strip()
    except: pass

    # ---- brandName: a[title] ----
    try:
        el = job_item.ele("css:a[title]", timeout=1)
        if el and el.text:
            info['brandName'] = el.text.strip()
    except: pass

    # ---- cityName / jobExperience / jobDegree: div.jobinfo__other-info-item ----
    try:
        info_items = job_item.eles("css:div.jobinfo__other-info-item")
        for el in info_items:
            if not (el and el.text): continue
            t = el.text.strip()
            if any(kw in t for kw in ['经验', '年', '不限', '应届']):
                if not info['jobExperience']:
                    info['jobExperience'] = t
            elif any(kw in t for kw in ['学历', '大专', '本科', '硕士', '博士', '中专', '高中']):
                if not info['jobDegree']:
                    info['jobDegree'] = t
            else:
                if not info['cityName']:
                    info['cityName'] = t
    except: pass

    # ---- brandNature / brandScale / brandIndustry: div.companyinfo__tag ----
    try:
        tag_container = job_item.ele("css:div.companyinfo__tag", timeout=1)
        if tag_container:
            tag_els = tag_container.eles("xpath:*")
            for idx, el in enumerate(tag_els):
                if el and el.text:
                    t = el.text.strip()
                    if idx == 0: info['brandNature'] = t
                    elif idx == 1: info['brandScale'] = t
                    elif idx == 2: info['brandIndustry'] = t
    except: pass

    # ---- companyTag: div.companyinfo__employ-tag ----
    try:
        el = job_item.ele("css:div.companyinfo__employ-tag", timeout=1)
        if el and el.text:
            info['companyTag'] = el.text.strip()
    except: pass

    return info


def hover_extract_detail(page, name_element):
    try:
        # 先移到最左侧，避免鼠标路径经过下拉列表
        page.actions.move_to(10, 300).perform()
        page.wait(0.2)
        page.actions.move_to(name_element).perform()
        page.wait(1.5)
        detail_el = page.ele("css:div.info-detail__content", timeout=3)
        if detail_el and detail_el.text:
            return re.sub(r'\s+', ' ', detail_el.text.strip())
    except: pass
    return ''


def grab_one_page(page, all_jobs, max_count):
    print(f"  🔍 查找职位列表...")

    page.run_js("window.scrollTo(0, 0);")
    page.wait(0.5)
    page.run_js("window.scrollTo(0, 500);")
    page.wait(0.5)
    page.run_js("window.scrollTo(0, 0);")
    page.wait(1)

    job_items = page.eles("css:div.joblist-box__item.clearfix")
    if not job_items:
        job_items = page.eles("css:div.joblist-box__item")
    if not job_items:
        job_items = page.eles("css:div[class*='joblist-box__item']")

    print(f"  📋 找到 {len(job_items)} 条职位")

    if not job_items:
        print(f"  ⚠️ 无职位")
        print("     → 页面等待 60 秒供人工检查...")
        page.wait(60)
        return 0

    # 将鼠标移到最左侧，避免后续移动时经过下拉列表干扰详情提取
    page.actions.move_to(10, 300).perform()
    page.wait(0.3)

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

            name_el = item.ele("css:a.jobinfo__name", timeout=2)
            if name_el:
                job['jobDesc'] = hover_extract_detail(page, name_el)

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


def go_next_page(page):
    page.run_js("window.scrollTo(0, document.body.scrollHeight);")
    page.wait(1)

    next_btn = page.ele('xpath://a[normalize-space(text())="下一页"]', timeout=3)
    if not next_btn:
        next_btn = page.ele("css:a.btn.soupager__btn", timeout=3)

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
    return False


def export_csv(jobs, keyword, city):
    if not jobs:
        print("  ❌ 无数据，未生成CSV")
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"zhaopin_{city}_{keyword}_{ts}.csv"
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
            '公司性质': j.get('brandNature', ''),
            '公司规模': j.get('brandScale', ''),
            '公司行业': j.get('brandIndustry', ''),
            '公司标签': j.get('companyTag', ''),
            '职位描述': j.get('jobDesc', ''),
        })
    pd.DataFrame(records).to_csv(fname, index=False, encoding='utf-8-sig')
    print(f"✅ 导出 {len(records)} 条")
    return fname


def crawl_one_city(page, keyword, city_name, max_count):
    print("\n" + "=" * 80)
    print(f"🏙️ 开始爬取: {city_name}")
    print("=" * 80)

    city_pinyin = CITY_PINYIN.get(city_name)
    if not city_pinyin:
        print(f"  ❌ 未找到城市「{city_name}」的拼音映射")
        return [], None

    city_url = f"https://www.zhaopin.com/{city_pinyin}/"
    print(f"  🌐 访问: {city_url}")
    page.get(city_url)
    page.wait.doc_loaded(timeout=10)
    page.wait(2)
    print("  ✅ 城市页面已加载")

    result = search_keyword(page, keyword)
    if not result or not result[0]:
        print(f"  ❌ {city_name} 搜索失败")
        return [], None
    search_page = result[0]

    print("\n  👆 开始逐条抓取...")

    all_jobs = []
    same_count = 0
    prev_total = 0

    while len(all_jobs) < max_count:
        grab_one_page(search_page, all_jobs, max_count)

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

        if not go_next_page(search_page):
            print("  ⚠️ 无下一页，结束")
            break

    print(f"\n  ✅ {city_name} 完成: {len(all_jobs)} 条")
    csv_file = None
    if all_jobs:
        csv_file = export_csv(all_jobs, keyword, city_name)

    # 关闭搜索结果标签页
    if search_page is not page:
        try:
            search_page.close()
        except:
            pass

    return all_jobs, csv_file


def main():
    print("=" * 80)
    print("🚀 智联招聘爬虫 - 多城市版")
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
        print(f"\n🌐 打开智联招聘首页...")
        page.get("https://www.zhaopin.com/")
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
