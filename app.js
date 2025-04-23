// 引入 Supabase 客户端库
const { createClient } = require('@supabase/supabase-js');

// 设置 Supabase 项目的 URL 和 API 密钥（你可以在 Supabase 控制台中找到这些）
const supabaseUrl = process.env.supabaseUrl;  // 替换为你的 Supabase URL
const supabaseKey = process.env.supabaseKey;  // 替换为你的 API 密钥（服务角色密钥或匿名密钥）


console.log(supabaseUrl,supabaseKey);
// 创建 Supabase 客户端
const supabase = createClient(supabaseUrl, supabaseKey);

async function insertData() {
    // 数据插入对象
    const newsData = {
      title: 'New Feature Released!',
      content: 'We just released a new feature in our app.',
      lat: 36,
      lon: 119,
      city: '潍坊'
    };
  
    // 插入数据到 'news' 表
    const { data, error } = await supabase
      .from('news')  // 指定表名
      .insert([newsData]);  // 插入数据
  
    if (error) {
      console.error('Error inserting data:', error);
    } else {
      console.log('Inserted data:', data);
    }
  }
  
  // 调用插入数据的函数
  insertData();