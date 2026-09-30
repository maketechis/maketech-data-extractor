export const API=process.env.API_URL||process.env.NEXT_PUBLIC_API_URL||"http://127.0.0.1:8000";
export async function api(path:string,init?:RequestInit){const r=await fetch(API+path,{...init,cache:"no-store"});if(!r.ok)throw new Error("API "+r.status);return r.json()}
