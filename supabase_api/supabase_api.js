import { createClient } from '@supabase/supabase-js';
import { get_utc_now } from '../utils_time/utc_time';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;

const supabase = createClient(supabaseUrl, supabaseKey);

export async function insert_table(item, tableName) {
    try {
        const { error } = await supabase.from(tableName).insert([item]);
        if (error) {
            console.error(`❌插入失败:${item.title}`, get_utc_now().toDateString());
        } else {
            console.log(`✅插入成功:${item.title}`);
        }
    } catch (error) {
        console.error("Failed to insert data: insert_table");
    }
}