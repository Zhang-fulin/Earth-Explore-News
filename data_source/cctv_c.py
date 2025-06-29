from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup
from deepseek_api.deepseek_api import news_coordinates_lon_lat
from utils_time.utc_time import get_utc_now_str
import json
import subprocess
import os
import subprocess


def scrape_cctv_c_links(url):
    today_date = datetime.now().strftime('%Y/%m/%d')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, timeout=60000)
        
        page.wait_for_selector('ul#newslist a[target="_blank"]', timeout=60000)

        links = page.query_selector_all('ul#newslist a[target="_blank"]')

        hrefs = [link.get_attribute('href') for link in links]

        filtered_links = [href for href in hrefs if today_date in href]

        unique_links = list(set(filtered_links))

        browser.close()
        return unique_links
    
def scrape_cctv_c_html(url):
    html = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle')
            page.wait_for_selector('.content_area', timeout=60000) # 等待 JS 加载完成
            html = page.content()  # 获取 HTML 内容
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        browser.close()
    return html

def process_cctv_c_htmls_with_title(html):
    if not html:
        return None
    title_text = None
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one('div#title_area h1')
        title_text = title.get_text(strip=True) if title else ''
    except Exception as e:
            print(f"Error get title {e}")
    return title_text

def process_cctv_c_htmls_with_info(html):
    if not html:
        return None
    info_text = None
    try:
        soup = BeautifulSoup(html, 'html.parser')
        div_info1 = soup.find("div", class_="info1")
        info_text = div_info1.get_text(strip=True) if div_info1 else ''
    except Exception as e:
            print(f"Error get info {e}")
    return info_text

def process_cctv_c_htmls_with_content(html):
    if not html:
        return None
    content_text = None

    try:
        soup = BeautifulSoup(html, 'html.parser')
        content_text = soup.select_one('div#content_area')
    except Exception as e:
            print(f"Error get title {e}")
    return content_text

def clean_content_area(content_area):
    if not content_area:
        return ""
    content_area.attrs = {}
    for tag in content_area.find_all(True):
        
        if tag.name == "p" and tag.find(attrs={"id": lambda x: x and "flash" in x.lower()}):
            tag.decompose()
            continue
        
        if tag.name == "img":
            tag.attrs = {"src": tag.get("src")} if tag.has_attr("src") else {}
        else:
            tag.attrs = {}

    return str(content_area)

def stoarge_cctv_c_htmls(news):

    return None


def get_cctv_c_news(website_name, url):
    news_links = scrape_cctv_c_links(url)
    for link in news_links:
        news_html = scrape_cctv_c_html(link)

        title = process_cctv_c_htmls_with_title(news_html)
        info = process_cctv_c_htmls_with_info(news_html)
        content_origin = process_cctv_c_htmls_with_content(news_html)
        content = clean_content_area(content_origin)
        lon,lat = news_coordinates_lon_lat(content)

        if not all([news_html, title, info, content_origin, content, lon, lat]):
            continue

        news_data = {
            "title": title,
            "info": info,
            "content": content,
            "lon": lon,
            "lat": lat,
            "url": link,
            "source": website_name,
            "time": get_utc_now_str()
        }

        json_data = json.dumps(news_data)

        current_dir = os.path.dirname(__file__)
        script_path = os.path.join(current_dir, 'cctv-news.js')

        result = subprocess.run(['node', script_path], input=json_data,
            text=True,
            capture_output=True,
            encoding='utf-8'
        )

        print(result.stderr, result.stdout)

    return None