import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;

const supabase = createClient(supabaseUrl, supabaseKey);

export async function delete_data_by_date(date, tableName="today-news") {
    try {
      const { error } = await supabase.from(tableName).delete().gte('time', date)

      if (error) {
        console.error(`Failed to delete data from "${tableName}"`);
        throw new Error('Failed to delete data from table')
      }
  
      console.log(`✅删除成功 All data newer "${date}" than  has been deleted`);
      return true;
    } catch (error) {
        console.error(`Failed to delete data from "${tableName}"`);
      return false;
    }
}

export async function get_data_by_date(date, tableName='news') {
    try {

      const { data, error } = await supabase.from(tableName).select('*').gte('time', date);

      if (error) {
        console.error("Failed to get data: get_data_by_data");
        throw new Error("Failed to get data: get_data_by_data")
      }
      return data;
    } catch (error) {
        console.error("Failed to get data: get_data_by_data");
      return [];
    }
}

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

    // ✅ 如果查到了数据，返回 true；否则 false
    return data && data.length > 0;

  } catch (err) {
    console.error('异常:', err);
    return false;
  }
}
