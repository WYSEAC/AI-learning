# -*- coding: utf-8 -*-
"""猎聘网 - XPath 探索模式（仅打开网站）"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import launch

LIEPIN_URL = "https://www.liepin.com/"


def main():
    print("=" * 60)
    print("🧪 猎聘网 - XPath 探索模式")
    print("=" * 60)
    print()
    print("已预设的关键元素定位（待验证）：")
    print("  登录按钮:        span.login-btn")
    print("  搜索框:          input[placeholder='搜索职位、公司']")
    print("  搜索按钮:        i.search-icon")
    print("  职位列表项:      div.job-list-item")
    print("  职位名称:        div.job-title-box span.job-name")
    print("  公司名称:        div.company-name")
    print("  薪资:            span.job-salary")
    print("  详情面板:        div.job-detail-box")
    print("  下一页按钮:      li.ant-pagination-next")
    print()

    page = launch(
        headless=False,
        xpath_picker=True,
        window_size=(1600, 1100),
    )
    page.window.maximize()

    print(f"🌐 打开猎聘网: {LIEPIN_URL}")
    page.get(LIEPIN_URL)
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
