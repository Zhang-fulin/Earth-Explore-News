import { insert_table, urlExists } from "../supabase_api/supabase_api.js";

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

async function insert_news(news_data) {
    if (!await urlExists(news_data.url, 'cctv-news')) {
        await insert_table(news_data, 'cctv-news');
    } 
}

async function main() {
  const news_data = await readStdinJson();
  await insert_news(news_data);
}

main();