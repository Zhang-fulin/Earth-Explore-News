from playwright.sync_api import sync_playwright
from datetime import datetime

# BBC 爬虫函数
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

def scrape_cctv(url):
    today_date = datetime.now().strftime('%Y/%m/%d')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, timeout=60000)
        
        page.wait_for_selector('a[target="_blank"]', timeout=60000)

        links = page.query_selector_all('a[target="_blank"]')

        hrefs = [link.get_attribute('href') for link in links]

        filtered_links = [href for href in hrefs if today_date in href]

        unique_links = list(set(filtered_links))

        browser.close()
        return unique_links
    
# China Daily 爬虫函数
def scrape_chinadaily(url):
    links = set()
    print(url)
    # 添加China Daily的爬取逻辑
    return links

# Reuters 爬虫函数
def scrape_reuters(url):
    links = set()
    # 添加Reuters的爬取逻辑
    return links

# CNN 爬虫函数
def scrape_cnn(url):
    links = set()
    # 添加CNN的爬取逻辑
    return links

# The New York Times 爬虫函数
def scrape_nytimes(url):
    links = set()
    # 添加The New York Times的爬取逻辑
    return links

# The Guardian 爬虫函数
def scrape_guardian(url):
    links = set()
    # 添加The Guardian的爬取逻辑
    return links

# Le Monde 爬虫函数
def scrape_lemonde(url):
    links = set()
    # 添加Le Monde的爬取逻辑
    return links

# El País 爬虫函数
def scrape_elpais(url):
    links = set()
    # 添加El País的爬取逻辑
    return links

# Al Jazeera 爬虫函数
def scrape_aljazeera(url):
    links = set()
    # 添加Al Jazeera的爬取逻辑
    return links

# The Times of India 爬虫函数
def scrape_timesofindia(url):
    links = set()
    # 添加The Times of India的爬取逻辑
    return links

# The Sydney Morning Herald 爬虫函数
def scrape_smh(url):
    links = set()
    # 添加The Sydney Morning Herald的爬取逻辑
    return links

# South China Morning Post 爬虫函数
def scrape_scmp(url):
    links = set()
    # 添加South China Morning Post的爬取逻辑
    return links

# France 24 爬虫函数
def scrape_france24(url):
    links = set()
    # 添加France 24的爬取逻辑
    return links

# Der Spiegel 爬虫函数
def scrape_spiegel(url):
    links = set()
    # 添加Der Spiegel的爬取逻辑
    return links

# The Australian 爬虫函数
def scrape_theaustralian(url):
    links = set()
    # 添加The Australian的爬取逻辑
    return links

# The Africa Report 爬虫函数
def scrape_africareport(url):
    links = set()
    # 添加The Africa Report的爬取逻辑
    return links

# The Japan Times 爬虫函数
def scrape_japantimes(url):
    links = set()
    # 添加The Japan Times的爬取逻辑
    return links

# Telesur 爬虫函数
def scrape_telesur(url):
    links = set()
    # 添加Telesur的爬取逻辑
    return links

# Clarin 爬虫函数
def scrape_clarin(url):
    links = set()
    # 添加Clarin的爬取逻辑
    return links

# O Globo 爬虫函数
def scrape_oglobo(url):
    links = set()
    # 添加O Globo的爬取逻辑
    return links

# Folha de S. Paulo 爬虫函数
def scrape_folha(url):
    links = set()
    # 添加Folha de S. Paulo的爬取逻辑
    return links

# Times of Malta 爬虫函数
def scrape_timesofmalta(url):
    links = set()
    # 添加Times of Malta的爬取逻辑
    return links

# Middle East Eye 爬虫函数
def scrape_middleeasteye(url):
    links = set()
    # 添加Middle East Eye的爬取逻辑
    return links

# The Hindu 爬虫函数
def scrape_thehindu(url):
    links = set()
    # 添加The Hindu的爬取逻辑
    return links

# Asahi Shimbun 爬虫函数
def scrape_asahi(url):
    links = set()
    # 添加Asahi Shimbun的爬取逻辑
    return links

# 主函数用于根据网站名来选择爬虫函数
def get_news_links(website_name, url):
    if website_name == "BBC":
        links = scrape_bbc(url)
        return links
    elif website_name == "CCTV":
        return scrape_cctv(url)
    elif website_name == "China Daily":
        return scrape_chinadaily(url)
    elif website_name == "Reuters":
        return scrape_reuters(url)
    elif website_name == "CNN":
        return scrape_cnn(url)
    elif website_name == "The New York Times":
        return scrape_nytimes(url)
    elif website_name == "The Guardian":
        return scrape_guardian(url)
    elif website_name == "Le Monde":
        return scrape_lemonde(url)
    elif website_name == "El País":
        return scrape_elpais(url)
    elif website_name == "Al Jazeera":
        return scrape_aljazeera(url)
    elif website_name == "The Times of India":
        return scrape_timesofindia(url)
    elif website_name == "The Sydney Morning Herald":
        return scrape_smh(url)
    elif website_name == "South China Morning Post":
        return scrape_scmp(url)
    elif website_name == "France 24":
        return scrape_france24(url)
    elif website_name == "Der Spiegel":
        return scrape_spiegel(url)
    elif website_name == "The Australian":
        return scrape_theaustralian(url)
    elif website_name == "The Africa Report":
        return scrape_africareport(url)
    elif website_name == "The Japan Times":
        return scrape_japantimes(url)
    elif website_name == "Telesur":
        return scrape_telesur(url)
    elif website_name == "Clarin":
        return scrape_clarin(url)
    elif website_name == "O Globo":
        return scrape_oglobo(url)
    elif website_name == "Folha de S. Paulo":
        return scrape_folha(url)
    elif website_name == "Times of Malta":
        return scrape_timesofmalta(url)
    elif website_name == "Middle East Eye":
        return scrape_middleeasteye(url)
    elif website_name == "The Hindu":
        return scrape_thehindu(url)
    elif website_name == "Asahi Shimbun":
        return scrape_asahi(url)
    else:
        return None
    

def fetch_htmls(urls):
    html_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for url in urls:
            try:
                page.goto(url, timeout=60000)
                html = page.content()
                html_list.append(html)
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                html_list.append(None)
        browser.close() 
    return html_list



