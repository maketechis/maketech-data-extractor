from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
import time
import httpx
from bs4 import BeautifulSoup
GOOGLE_SEARCH_URL="https://www.google.com/search"
@dataclass(frozen=True,slots=True)
class GoogleResult:title:str;url:str;page:int=1;rank:int=0
class GoogleSerpError(RuntimeError):pass
class GoogleRateLimited(GoogleSerpError):pass
def build_google_query(*,entity_type:str,district:str,state:str,country:str,name:str|None=None)->str:return " ".join(x for x in [f'"{name}"' if name else entity_type,district,state,country] if x)
def _unwrap(href):
    if href.startswith("/url?"):
        q=parse_qs(urlparse(href).query);return (q.get("q") or q.get("url") or [""])[0]
    return href
def _parse(html,page,limit=10):
    soup=BeautifulSoup(html,"html.parser");out=[];seen=set()
    for h in soup.select("h3"):
        a=h.find_parent("a",href=True)
        if not a:continue
        href=_unwrap(a.get("href",""));p=urlparse(href)
        if p.scheme not in ("http","https") or "google." in p.netloc.lower() or href in seen:continue
        seen.add(href);out.append(GoogleResult(h.get_text(" ",strip=True),href,page,len(out)+1))
        if len(out)>=limit:break
    return out
class GoogleSession:
    def __init__(self,timeout=25):
        self.client=httpx.Client(timeout=timeout,follow_redirects=True,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","Accept-Language":"en-IN,en;q=0.9"})
    def close(self):self.client.close()
    def page(self,query,page):
        r=self.client.get(GOOGLE_SEARCH_URL,params={"q":query,"start":(page-1)*10,"num":10,"hl":"en","gl":"in","pws":"0","filter":"0"})
        if r.status_code==429:raise GoogleRateLimited("HTTP 429 Too Many Requests")
        r.raise_for_status();low=r.text.lower()
        if "unusual traffic" in low or "captcha" in low:raise GoogleRateLimited("Google unusual-traffic/captcha response")
        rows=_parse(r.text,page)
        if not rows:raise GoogleSerpError("no parseable organic results")
        return rows
def search_google_page(query,*,page=1,limit=10,timeout=25):
    s=GoogleSession(timeout)
    try:return s.page(query,page)[:limit]
    finally:s.close()
def search_google(query,*,limit=10,timeout=25):return search_google_page(query,page=1,limit=limit,timeout=timeout)
def search_google_pages(query,*,pages=5,delay_seconds=20,sleep=time.sleep):
    out=[];diagnostics=[];session=GoogleSession()
    try:
        for page in range(1,pages+1):
            try:
                rows=session.page(query,page);out.extend(rows);diagnostics.append({"page":page,"status":"success","results":len(rows),"error":None})
            except GoogleRateLimited as exc:
                diagnostics.append({"page":page,"status":"rate_limited","results":0,"error":str(exc)})
                for skipped in range(page+1,pages+1):diagnostics.append({"page":skipped,"status":"deferred","results":0,"error":"Deferred after Google rate limit; retry later."})
                break
            except Exception as exc:
                diagnostics.append({"page":page,"status":"failed","results":0,"error":f"{type(exc).__name__}: {str(exc)[:200]}"})
            if page<pages:sleep(delay_seconds)
    finally:session.close()
    return out,diagnostics
