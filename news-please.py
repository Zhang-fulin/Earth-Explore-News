import json
from scraper import get_news_links

def main():
    # 读取 JSON 文件
    with open('websites.json', 'r', encoding='utf-8') as f:
        websites = json.load(f)

    # 测试
    for website in websites:
        if website["enable"]:
            name = website['name']
            url = website['url']
            
            print(f"Scraping news from: {name}")
            news_links = get_news_links(name, url)
            
            if news_links:
                print(f"Found {len(news_links)} news links:")
                for link in list(news_links)[:5]:  # 只打印前5个链接
                    print(link)
            else:
                print(f"No specific scraping rule for {name}.")
            print("\n---\n")

# 入口函数
if __name__ == "__main__":
    main()