import OpenAI from "openai";

const deepseek_api_key = process.env.deepseek_api_key;

const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: deepseek_api_key
});

export async function filter_today_news(news) {
    try{
        const completion = await openai.chat.completions.create({
            messages: [
              { role: "system", content: "你是一个筛选新闻的好帮手" },
              {
                role: "user",
                content: `'${news}' 请忽略重复的新闻并提取出你觉得最重要的5个新闻,按照|***|***|***|... 的样式输出，请保证新闻内容不变`
              }
            ],
            model: "deepseek-chat",
          });
    
          return completion.choices[0].message.content.split('|').map(t => t.trim()).filter(t => t.length > 0);
    } catch (error) {
        console.error("Error in filter_today_news", error);
        throw error; // 如果发生错误，抛出异常
  }
}
  