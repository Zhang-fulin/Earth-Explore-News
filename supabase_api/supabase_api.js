import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;

const supabase = createClient(supabaseUrl, supabaseKey);

export async function delete_table(tableName) {
    try {
      const { error } = await supabase.from(tableName).delete();

      if (error) {
        console.error(`Failed to delete data from "${tableName}"`);
        throw new Error('Failed to delete data from table')
      }
  
      console.log(`All data from table "${tableName}" has been successfully deleted.`);
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


    //   const { data, error } = await supabase
//     .from('news')
//     .select('*')
//     .gte('time', currentDateISOString);

//   if (error) {
//     console.error('Error fetching news:', error);
//     return [];
//   }

//   console.log(data);
//   return data || [];
// }