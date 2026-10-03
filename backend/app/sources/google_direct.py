from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
import httpx
from bs4 import BeautifulSoup
GOOGLE_SEARCH_URL="https://www.google.com/search"
@dataclass(frozen=True,slots=True)
class GoogleResult:title:str;url:str;page:int=1;rank:int=0
def build_google_query(*,entity_type:str,district:str,state:str,country:str,name:str|None=None)->str:
    return " ".join(x for x in [f'"{name}"' if name else entity_type,district,state,country] if x)
def _unwrap(href:str)->str:
    if href.startswith("/url?"):
        return parse_qs(urlparse(href).query).get("q",[""])[0]
    return href
def search_google_page(query:str,*,page:int=1,limit:int=10,timeout:float=20)->list[GoogleResult]:
    start=(page-1)*10;headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"en-US,en;q=0.9"}
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:r=client.get(GOOGLE_SEARCH_URL,params={"q":query,"num":10,"start":start,"filter":"0"});r.raise_for_status()
    low=r.text.lower()
    if "unusual traffic" in low or "captcha" in low:raise RuntimeError("Google search blocked/captcha")
    soup=BeautifulSoup(r.text,"html.parser");out=[];seen=set()
    for block in soup.select("div.MjjYud, div.tF2Cxc, div.g"):
        a=block.select_one("a[href]");h=block.select_one("h3")
        if not a or not h:continue
        href=_unwrap(a.get("href",""));p=urlparse(href)
        if p.scheme not in ("http","https") or "google." in p.netloc.lower() or href in seen:continue
        seen.add(href);out.append(GoogleResult(h.get_text(" ",strip=True),href,page,len(out)+1))
        if len(out)>=limit:break
    if not out:
        for a in soup.select("a[href]"):
            href=_unwrap(a.get("href",""));p=urlparse(href);title=a.get_text(" ",strip=True)
            if p.scheme not in ("http","https") or "google." in p.netloc.lower() or not title or href in seen:continue
            seen.add(href);out.append(GoogleResult(title,href,page,len(out)+1))
            if len(out)>=limit:break
    return out
def search_google(query:str,*,limit:int=10,timeout:float=20)->list[GoogleResult]:return search_google_page(query,page=1,limit=limit,timeout=timeout)
def search_google_pages(query:str,*,pages:int=5)->list[GoogleResult]:
    out=[]
    for page in range(1,pages+1):out.extend(search_google_page(query,page=page))
    return out
