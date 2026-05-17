# -*- coding: utf-8 -*-
"""智联招聘 - XPath 探索模式（仅打开网站）"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import launch

ZHAOPIN_URL = "https://www.zhaopin.com/"


def main():
    print("=" * 60)
    print("🧪 智联招聘 - XPath 探索模式")
    print("=" * 60)
    print()
    print("已预设的关键元素定位：")
    print("  登录按钮:        a.home-header__c-no-login")
    print("  微信扫码:        div.zppp-panel-normal-bar__img")
    print("  搜索框:          input[placeholder='搜索职位、公司']")
    print("  搜索按钮:        div.search-box.fl > button")
    print("  切换城市:        div.content-s__item")
    print("  城市输入框:      input[placeholder='输入地区名称']")
    print("  职位列表项:      div.joblist-box__item.clearfix")
    print("  职位名称:        a.jobinfo__name")
    print("  职位详情面板:    div.info-detail__content-text")
    print("  下一页按钮:      a.soupager__btn (文本: 下一页)")
    print()

    page = launch(
        headless=False,
        xpath_picker=True,
        window_size=(1600, 1100),
    )
    page.window.maximize()

    print(f"🌐 打开智联招聘: {ZHAOPIN_URL}")
    page.get(ZHAOPIN_URL)
    page.wait.doc_loaded(timeout=15)
    print("✅ 页面已加载，xpath 选择器已就绪")

    print("\n🔚 浏览器保持打开，按 Ctrl+C 退出...")
    try:
        while True:
            page.wait(10)
    except KeyboardInterrupt:
        print("\n👋 关闭浏览器")
        page.quit()


if __name__ == "__main__":
    main()
