import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;

const supabase = createClient(supabaseUrl, supabaseKey);

export async function insert_table(item, tableName) {
    try {
        const { error } = await supabase.from(tableName).insert([item]);
        if (error) {
            console.error('❌插入失败', error);
        } else {
            console.log(`✅插入成功:${item.content}`);
        }
    } catch (error) {
        console.error("Failed to insert data: insert_table");
    }
}    

export async function urlExists(url, tableName) {
  try {
    const { data, error } = await supabase
      .from(tableName)
      .select('url')
      .eq('url', url)
      .limit(1);

    if (error) {
      console.error('查询 URL 出错:', error);
      return false;
    }
    
    return data && data.length > 0;

  } catch (err) {
    console.error('异常:', err);
    return false;
  }
}
