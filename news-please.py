import json
from scraper import get_news_links
from scraper import fetch_htmls
from newsplease import NewsPlease
from openai import OpenAI
import re
import datetime
import os
import time
import subprocess

deepseek_api_key = os.getenv('deepseek_api_key', 'default_value')

client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

def main():
    with open('websites.json', 'r', encoding='utf-8') as f:
        websites = json.load(f)

    for website in websites:
        if website["enable"]:
            name = website['name']
            url = website['url']
            
            print(f"Scraping news from: {name}")
            news_links = get_news_links(name, url)
            news_htmls = fetch_htmls(news_links)

            news_titles = ''
            
            if news_htmls:
                for html in list(news_htmls):
                    article = NewsPlease.from_html(html)
                    if article.title:
                        news_titles += article.title + '|'

            else:
                print(f"No specific scraping rule for {name}.")

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who can search the web for information."},
                    {"role": "user", "content": f"'{news_titles}' 汇总并总结出5个最重要的新闻 并按照json数组{{content:xxx, lon:xxx, lat:xxx}}格式输出, lon lat 是你推断的经纬度, 如果推断一样的经纬度，请加不超过5的偏移"},
                ],
                stream=False
            )

            response_content = response.choices[0].message.content

            cleaned_response = response_content.replace("\n", "")

            match = re.search(r'\[.*\]', cleaned_response, re.DOTALL)

            if match:
                json_string = match.group(0)
                try:
                    data = json.loads(json_string)

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    
                    file_name = f"{name + '_' + current_time}.json"
                    
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"数据已保存到文件 {file_name}")

                except json.JSONDecodeError:
                    print("提取的内容不是有效的 JSON 格式")
            else:
                print("未找到有效的 JSON 内容")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1 * 60)
        subprocess.run(["node", "app.js"])
        time.sleep(2 * 60 * 60)
