import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.supabaseUrl;
const supabaseKey = process.env.supabaseKey;

const supabase = createClient(supabaseUrl, supabaseKey);

export async function insert_table(item, tableName) {
    try {
        const { error } = await supabase.from(tableName).insert([item]);
        if (error) {
            console.error(`❌插入失败:${item.title}`, Date().toString());
        } else {
            console.log(`✅插入成功:${item.title}`);
        }
    } catch (error) {
        console.error("Failed to insert data: insert_table");
    }
}