from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
import httpx
from bs4 import BeautifulSoup
from app.sources.google_direct import GoogleResult,search_google
from app.sources.search_settings import SearchMode,SearchSettings

@dataclass(frozen=True,slots=True)
class WebSearchResult:
    engine:str
    title:str
    url:str

def _generic_search(url:str,query:str,engine:str,limit:int,timeout:float=15.0):
    headers={"User-Agent":"Mozilla/5.0 (compatible; MakeTechDataExtractor/0.1)"}
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:
        response=client.get(url,params={"q":query}); response.raise_for_status()
    text=response.text.lower()
    if "captcha" in text or "unusual traffic" in text: raise RuntimeError(f"{engine} search blocked")
    soup=BeautifulSoup(response.text,"html.parser"); out=[]; seen=set()
    for a in soup.select("a[href]"):
        href=a.get("href",""); title=a.get_text(" ",strip=True)
        if engine=="yahoo" and "RU=" in href:
            try: href=href.split("RU=",1)[1].split("/RK=",1)[0]
            except Exception: pass
        p=urlparse(href)
        if p.scheme not in ("http","https") or engine in p.netloc.lower() or not title or href in seen: continue
        seen.add(href); out.append(WebSearchResult(engine,title,href))
        if len(out)>=limit: break
    return out

def search_bing(query:str,limit:int=10):
    return _generic_search("https://www.bing.com/search",query,"bing",limit)

def search_yahoo(query:str,limit:int=10):
    return _generic_search("https://search.yahoo.com/search",query,"yahoo",limit)

def search_web(query:str,settings:SearchSettings):
    combined=[]; seen=set()
    for engine in settings.enabled_engines():
        try:
            if engine=="google": rows=[WebSearchResult("google",x.title,x.url) for x in search_google(query,limit=settings.max_results)]
            elif engine=="bing": rows=search_bing(query,settings.max_results)
            else: rows=search_yahoo(query,settings.max_results)
        except Exception:
            rows=[]
        useful=[]
        for row in rows:
            if row.url in seen: continue
            seen.add(row.url); combined.append(row); useful.append(row)
        if settings.mode==SearchMode.FALLBACK and useful: break
    return combined
