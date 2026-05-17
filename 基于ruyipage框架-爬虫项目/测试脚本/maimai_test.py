# -*- coding: utf-8 -*-
"""脉脉 - XPath 探索模式（仅打开网站）"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import launch

MAIMAI_URL = "https://maimai.cn/"


def main():
    print("=" * 60)
    print("🧪 脉脉 - XPath 探索模式")
    print("=" * 60)
    print()
    print("已预设的关键元素定位（待验证）：")
    print("  登录按钮:        待定位")
    print("  搜索框:          待定位")
    print("  搜索按钮:        待定位")
    print("  职位列表项:      待定位")
    print("  职位名称:        待定位")
    print("  公司名称:        待定位")
    print("  薪资:            待定位")
    print("  详情面板:        待定位")
    print("  下一页按钮:      待定位")
    print()

    page = launch(
        headless=False,
        xpath_picker=True,
        window_size=(1600, 1100),
    )
    page.window.maximize()

    print(f"🌐 打开脉脉: {MAIMAI_URL}")
    page.get(MAIMAI_URL)
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
