from data_source.cctv import  scrape_cctv_links,  stoarge_cctv_htmls, get_cctv_news


def get_news_links(website_name, url):
    if website_name == "CCTV":
        return scrape_cctv_links(url)
    else:
        return None
    

def get_news_htmls(website_name, urls):
    # if website_name == "CCTV":
    #     return scrape_cctv_htmls(urls)
    # else:
        return None

def process_news_htmls(website_name, htmls):
    # if website_name == "CCTV":
    #     return process_cctv_htmls(htmls)
    # else:
        return None
    
def stoarge_news_contens(website_name, htmls):
    if website_name == "CCTV":
        return stoarge_cctv_htmls(htmls)
    else:
        return None
    
def process_news_website(website_name, url):
    if website_name == "CCTV":
            return get_cctv_news(website_name, url)
    else:
        return None