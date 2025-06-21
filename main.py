from data_source.cctv import get_cctv_news
import time
import json
    
def process_news_website(website_name, url):
    if website_name == "CCTV":
            return get_cctv_news(website_name, url)
    else:
        return None

def main():
    with open('websites.json', 'r', encoding='utf-8') as f:
        websites = json.load(f)

    for website in websites:
        if website["enable"]:
            website_name = website['name']
            website_url = website['url']
            
            process_news_website(website_name, website_url)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1 * 60 * 60)
