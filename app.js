import fs from 'fs/promises';
import path from 'path';

const websites = JSON.parse(await fs.readFile('./websites.json', 'utf-8'));

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;
const deepseek_api_key = process.env.deepseek_api_key;

const supabase = createClient(supabaseUrl, supabaseKey);

function getTodayDateString() {
  const today = new Date();
  const offset = 8 * 60;
  const utc = today.getTime() + today.getTimezoneOffset() * 60000;
  const beijingTime = new Date(utc + offset * 60000);
  const year = beijingTime.getFullYear();
  const month = String(beijingTime.getMonth() + 1).padStart(2, '0');
  const day = String(beijingTime.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

async function findLatestFile(sourceName) {
  const todayDate = getTodayDateString();
  const files = await fs.readdir('.');
  const matchedFiles = files.filter(f =>
    f.startsWith(`${sourceName}_${todayDate}`) && f.endsWith('.json')
  );

  if (matchedFiles.length === 0) {
    console.log(`⚠️ 没有找到 ${sourceName} 今日的文件`);
    return null;
  }

  const sorted = matchedFiles
    .map(file => {
      const match = file.match(/^.+_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json$/);
      if (!match) return null;
      const timestamp = match[1].replace(/_/g, ' ').replace(/-/g, ':').replace(' ', 'T');
      return { file, date: new Date(timestamp.replace(/:/g, (c, i) => i === 13 || i === 16 ? ':' : '-')) };
    })
    .filter(Boolean)
    .sort((a, b) => b.date - a.date);

  return sorted[0]?.file || null;
}

function extractTimeFromFilename(filename) {
  const match = filename.match(/_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json/);
  return match ? match[1].replace(/_/g, ' ').replace(/-/g, ':') : null;
}

async function insertData() {
  for (const site of websites) {
    if (site.enable) {
      const latestFile = await findLatestFile(site.name);
      if (latestFile) {
        const raw = await fs.readFile(latestFile, 'utf-8');
        const json = JSON.parse(raw);
        const time = extractTimeFromFilename(latestFile) || new Date().toISOString();

        for (const item of json) {
          const newsData = {
            title: site.name,
            content: item.content,
            lat: item.lat,
            lon: item.lon,
            city: item.city || '未知',
            time: time
          };

          const { data, error } = await supabase.from('news').insert([newsData]);

          if (error) {
            console.error(`❌ 插入失败: ${site.name}`, error);
          } else {
            console.log(`✅ 插入成功: ${site.name}`, item.content);
          }
        }
      }
    }
  }
}

insertData()

import { startOfDay } from 'date-fns';
async function fetchNews() {
  const currentDateISOString = startOfDay(new Date()).toISOString();

  const { data, error } = await supabase
    .from('news')
    .select('*')
    .gte('time', currentDateISOString);

  if (error) {
    console.error('Error fetching news:', error);
    return [];
  }

  console.log(data);
  return data || [];
}

import OpenAI from "openai";

const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: deepseek_api_key
});

async function main() {
  const newsItems = await fetchNews();

  if (newsItems.length === 0) {
    console.log("No news found for today.");
    return;
  }

  let news = '|';
  for (const n of newsItems) {
    news += n.content + '|';
  }

  const completion = await openai.chat.completions.create({
    messages: [
      { role: "system", content: "你是一个筛选新闻的好帮手" },
      {
        role: "user",
        content: `'${news}' 请忽略重复的新闻并提取出你觉得最重要的10个新闻,按照|***|***|***|... 的样式输出，请保证新闻内容不变`
      }
    ],
    model: "deepseek-chat",

  });

      // 2. 提取标题数组
    const aiTitles = completion.choices[0].message.content
    .split('|')
    .map(t => t.trim())
    .filter(t => t.length > 0);

    const selectedNewsItems = aiTitles.map(title =>
      newsItems.find(n => n.content === title)
    ).filter(Boolean); // 去掉未匹配上的 null

    const currentDateISOString = startOfDay(new Date()).toISOString();
    await supabase
      .from('news-filter')
      .delete()
      .gte('time', currentDateISOString);

    for (const item of selectedNewsItems) {
      const { error } = await supabase.from('news-filter').insert([item]);
      if (error) {
        console.error('❌ 插入失败', error);
      } else {
        console.log(`✅ 插入成功: ${item.content}`);
      }
    }
}

main();
