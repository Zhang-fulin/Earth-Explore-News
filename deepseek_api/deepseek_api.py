from openai import OpenAI
import os

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