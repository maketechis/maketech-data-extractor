from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
import httpx
from bs4 import BeautifulSoup
GOOGLE_ENDPOINTS=("https://www.google.com/search","https://www.google.co.in/search")
@dataclass(frozen=True,slots=True)
class GoogleResult:title:str;url:str;page:int=1;rank:int=0
class GoogleSerpError(RuntimeError):pass
def build_google_query(*,entity_type:str,district:str,state:str,country:str,name:str|None=None)->str:
    return " ".join(x for x in [f'"{name}"' if name else entity_type,district,state,country] if x)
def _unwrap(href:str)->str:
    if href.startswith("/url?"):
        q=parse_qs(urlparse(href).query)
        return (q.get("q") or q.get("url") or [""])[0]
    return href
def _parse(html:str,page:int,limit:int=10)->list[GoogleResult]:
    soup=BeautifulSoup(html,"html.parser");out=[];seen=set()
    for h in soup.select("h3"):
        a=h.find_parent("a",href=True)
        if not a:continue
        href=_unwrap(a.get("href",""));p=urlparse(href)
        if p.scheme not in ("http","https") or "google." in p.netloc.lower() or href in seen:continue
        seen.add(href);out.append(GoogleResult(h.get_text(" ",strip=True),href,page,len(out)+1))
        if len(out)>=limit:return out
    for a in soup.select("a[href]"):
        href=_unwrap(a.get("href",""));p=urlparse(href);title=a.get_text(" ",strip=True)
        if p.scheme not in ("http","https") or "google." in p.netloc.lower() or not title or href in seen:continue
        seen.add(href);out.append(GoogleResult(title,href,page,len(out)+1))
        if len(out)>=limit:break
    return out
def search_google_page(query:str,*,page:int=1,limit:int=10,timeout:float=20)->list[GoogleResult]:
    start=(page-1)*10
    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml","Accept-Language":"en-IN,en;q=0.9"}
    attempts=[{"q":query,"start":start,"num":10,"hl":"en","gl":"in","pws":"0","filter":"0","udm":"14"},{"q":query,"start":start,"num":10,"hl":"en","gl":"in","pws":"0","filter":"0","gbv":"1"}]
    last_reason="no parseable organic results"
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:
        for endpoint in GOOGLE_ENDPOINTS:
            for params in attempts:
                r=client.get(endpoint,params=params);r.raise_for_status();low=r.text.lower()
                if any(x in low for x in ("unusual traffic","our systems have detected unusual","captcha")):
                    last_reason="Google blocked automated request";continue
                if "consent.google" in str(r.url) or ("before you continue to google" in low):
                    last_reason="Google consent page returned";continue
                rows=_parse(r.text,page,limit)
                if rows:return rows
    raise GoogleSerpError(last_reason)
def search_google(query:str,*,limit:int=10,timeout:float=20)->list[GoogleResult]:return search_google_page(query,page=1,limit=limit,timeout=timeout)
def search_google_pages(query:str,*,pages:int=5)->tuple[list[GoogleResult],list[dict]]:
    out=[];diagnostics=[]
    for page in range(1,pages+1):
        try:
            rows=search_google_page(query,page=page);out.extend(rows);diagnostics.append({"page":page,"status":"success","results":len(rows),"error":None})
        except Exception as exc:
            diagnostics.append({"page":page,"status":"failed","results":0,"error":f"{type(exc).__name__}: {str(exc)[:300]}"})
    return out,diagnostics
