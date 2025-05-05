import json
from scraper import get_news_links
from scraper import fetch_htmls
from newsplease import NewsPlease
import re
import subprocess
from utils_time.utc_time import get_utc_now_str
from deepseek_api.deepseek_api import filter_website_news
import time

def main():
    with open('websites.json', 'r', encoding='utf-8') as f:
        websites = json.load(f)

    for website in websites:
        if website["enable"]:
            website_name = website['name']
            website_url = website['url']
            
            print(f"Scraping news from: {website_name}")
            news_links = get_news_links(website_name, website_url)
            news_htmls = fetch_htmls(news_links)

            news_titles = ''
            
            if news_htmls:
                for html in list(news_htmls):
                    try:
                        article = NewsPlease.from_html(html)
                        if article and article.title:
                            news_titles += article.title + '|'
                    except Exception as e:
                        print(f"Error parsing article: {e}")

            else:
                print(f"No specific scraping rule for {website_name}.")

            response_content = filter_website_news(news_titles);

            cleaned_response = response_content.replace("\n", "")

            match = re.search(r'\[.*\]', cleaned_response, re.DOTALL)

            if match:
                json_string = match.group(0)
                try:
                    news = json.loads(json_string)

                    news_data = {
                        "website_name": website_name,
                        "news": news,
                        "news_time": get_utc_now_str()
                    }

                    json_data = json.dumps(news_data)

                    result = subprocess.run(['node', 'clean-news.js'], input=json_data,
                        text=True,
                        capture_output=True,
                        encoding='utf-8'
                    )

                    print(result.stderr, result.stdout)
                except json.JSONDecodeError:
                    print("提取的内容不是有效的 JSON 格式")
            else:
                print("未找到有效的 JSON 内容")

if __name__ == "__main__":
    while True:
        # main()
        time.sleep(2 * 60 * 60)
