from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_bbc(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, timeout=60000)

              # 等待网络空闲，确保页面加载完成
        # page.wait_for_load_state('networkidle')

        # 抓取所有新闻链接：通常是以 https://www.bbc.com/news 开头
        anchors = page.query_selector_all('a[href^="/news"]')

        links = set()
        for a in anchors:
            href = a.get_attribute('href')
            if href:
                if href.startswith("/news/articles"):
                    links.add("https://www.bbc.com" + href)
                elif href.startswith("https://www.bbc.com/news"):
                    links.add(href)

        browser.close()
        return list(links)