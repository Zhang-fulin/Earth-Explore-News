from openai import OpenAI
import os
import json
import re

deepseek_api_key = os.getenv('deepseek_api_key', 'default_value')

client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

def filter_website_news(news):
    response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant who can search the web for information."},
                        {"role": "user", "content": f"'{news}' 汇总并总结出5个最重要的新闻 并按照json数组{{content:xxx, lon:xxx, lat:xxx}}格式输出, lon lat 是你推断的经纬度, 如果推断一样的经纬度，请加不超过2的偏移"},
                    ],
                    stream=False
                )

    return response.choices[0].message.content

def news_coordinates_lon_lat(news):
    response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个推断新闻发生地的助手"},
                        {"role": "user", "content": f'"{news}" 请推断出上面div标签中的新闻发生地, 并只输出这个{{ "lon":xxx, "lat":xxx }}, lon lat 是你推断的经纬度'},
                    ],
                    stream=False
                )

    return extract_lon_lat(response.choices[0].message.content)

def extract_lon_lat(response_text):
    try:
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if not match:
            raise ValueError("未找到 JSON 格式的大括号")
        json_str = match.group(0)
        lon_lat= json.loads(json_str)
        return lon_lat['lon'], lon_lat['lat']

    except Exception as e:
        print(f"⚠️ 解析失败: {e}")
        return None, None