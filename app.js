const fs = require('fs/promises');
const path = require('path');
const websites = require('./websites.json');

const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.supabaseUrl; 
const supabaseKey = process.env.supabaseKey; 

const supabase = createClient(supabaseUrl, supabaseKey);

function getTodayDateString() {
  const today = new Date();

  // 获取北京时间（UTC + 8 小时）
  const offset = 8 * 60;  // 北京时间与UTC的时差是8小时
  
  // 获取 UTC 时间并加上北京时间的偏移
  const utc = today.getTime() + today.getTimezoneOffset() * 60000;  
  const beijingTime = new Date(utc + offset * 60000);

  // 获取 "YYYY-MM-DD" 格式的日期
  const year = beijingTime.getFullYear();
  const month = String(beijingTime.getMonth() + 1).padStart(2, '0');
  const day = String(beijingTime.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}

// 查找与网站名对应的最新文件
async function findLatestFile(sourceName) {
  const todayDate = getTodayDateString();
  console.log(todayDate)
  const files = await fs.readdir('.');  // 获取当前目录的文件列表
  const matchedFiles = files.filter(f =>
    f.startsWith(`${sourceName}_${todayDate}`) && f.endsWith('.json')  // 查找今天的文件
  );

  if (matchedFiles.length === 0) {
    console.log(`⚠️ 没有找到 ${sourceName} 今日的文件`);
    return null;
  }

  // 按日期时间排序，最新的文件排前
  const sorted = matchedFiles
    .map(file => {
      const match = file.match(/^.+_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json$/);
      if (!match) return null;
      const timestamp = match[1].replace(/_/g, ' ').replace(/-/g, ':').replace(' ', 'T');
      return { file, date: new Date(timestamp.replace(/:/g, (c, i) => i === 13 || i === 16 ? ':' : '-')) };
    })
    .filter(Boolean)
    .sort((a, b) => b.date - a.date);  // 最新的排前面

  return sorted[0]?.file || null;  // 返回最新的文件名
}

// 从文件名提取时间（例如：CCTV_2025-04-30_20-07-53.json 中提取出时间部分）
function extractTimeFromFilename(filename) {
  const match = filename.match(/_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json/);
  return match ? match[1].replace(/_/g, ' ').replace(/-/g, ':') : null;  // 转换成 'YYYY-MM-DD HH:mm:ss' 格式
}

async function insertData() {

  for (const site of websites) {
    if (site.enable) {
      const latestFile = await findLatestFile(site.name);

      if (latestFile) {
        // 读取文件内容
        const raw = await fs.readFile(latestFile, 'utf-8');
        const json = JSON.parse(raw);
    
        // 从文件名中提取时间信息（或使用当前时间）
        const time = extractTimeFromFilename(latestFile) || new Date().toISOString();
        
        for (const item of json) {
          // 构造数据
          const newsData = {
            title: site.name,
            content: item.content,
            lat: item.lat,
            lon: item.lon,
            city: item.city || '未知',
            time: time 
          };
           // 插入数据到 Supabase
          const { data, error } = await supabase.from('news').insert([newsData]);
      
          if (error) {
            console.error(`❌ 插入失败: ${site.name}`, error);
          } else {
            console.log(`✅ 插入成功: ${site.name}`, data);
          }
        }
      }
    }
  }
}
  
//   // 调用插入数据的函数
insertData();