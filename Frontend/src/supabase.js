import { createClient } from "@supabase/supabase-js";
const url = process.env.REACT_APP_SUPABASE_URL;
const key = process.env.REACT_APP_SUPABASE_KEY;
const supabase = createClient(url, key);

export { supabase };
