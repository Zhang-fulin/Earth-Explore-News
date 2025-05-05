import { delete_data_by_date } from "./supabase_api/supabase_api.js";
import { get_data_by_date } from "./supabase_api/supabase_api.js";
import { insert_table } from "./supabase_api/supabase_api.js";
import { get_utc_now_str } from "./utils_time/utc_time.js";
import { filter_today_news } from "./deepseek_api/deepseek_api.js";

async function readStdinJson() {
  return new Promise((resolve, reject) => {
    process.stdin.setEncoding('utf8');
    let input = '';

    process.stdin.on('data', chunk => {
      input += chunk;
    });

    process.stdin.on('end', () => {
      try {
        const data = JSON.parse(input);
        resolve(data);
      } catch (err) {
        reject(new Error('Invalid JSON input: ' + err.message));
      }
    });

    process.stdin.on('error', err => {
      reject(err);
    });
  });
}

async function delete_today_news() {
  await delete_data_by_date(get_utc_now_str('today'));
}

async function insert_news(news_data) {
  for (const item of news_data.news) {
    const newsData = {
      title: news_data.website_name,
      content: item.content,
      lat: item.lat,
      lon: item.lon,
      city: item.city || '未知',
      time: news_data.news_time
    };

    console.log(newsData.content)
    await insert_table(newsData, 'news');
  }
}

async function insert_today_news(params) {
  const today_news = await get_data_by_date(get_utc_now_str('today'));
  if (today_news.length === 0) {
    console.log("No news found for today.");
    return;
  }

  let news = '|';
  for (const n of today_news) {
    news += n.content + '|';
  }

  const filter_news = await filter_today_news(news);

  const new_of_today_news = filter_news.map(title =>
      today_news.find(n => n.content === title)
    ).filter(Boolean);

  for (const item of new_of_today_news) {
    await insert_table(item, 'today-news')
  }
}


async function main() {
  const news_data = await readStdinJson();
  await insert_news(news_data);
  await delete_today_news();
  await insert_today_news();
}

main();