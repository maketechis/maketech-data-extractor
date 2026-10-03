from dataclasses import dataclass
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from app.sources.google_direct import search_google
from app.sources.search_settings import SearchMode,SearchSettings
@dataclass(frozen=True,slots=True)
class WebSearchResult: engine:str;title:str;url:str
@dataclass(slots=True)
class EngineDiagnostic:
    engine:str;status:str="not_run";queries:int=0;results:int=0;error:str|None=None
def _generic_search(url,query,engine,limit,timeout=15.0):
    headers={"User-Agent":"Mozilla/5.0 (compatible; MakeTechDataExtractor/0.1)"}
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:r=client.get(url,params={"q":query});r.raise_for_status()
    text=r.text.lower()
    if "captcha" in text or "unusual traffic" in text:raise RuntimeError(f"{engine} search blocked")
    soup=BeautifulSoup(r.text,"html.parser");out=[];seen=set()
    for a in soup.select("a[href]"):
        href=a.get("href","");title=a.get_text(" ",strip=True)
        if engine=="yahoo" and "RU=" in href:
            try:href=href.split("RU=",1)[1].split("/RK=",1)[0]
            except Exception:pass
        p=urlparse(href)
        if p.scheme not in ("http","https") or engine in p.netloc.lower() or not title or href in seen:continue
        seen.add(href);out.append(WebSearchResult(engine,title,href))
        if len(out)>=limit:break
    return out
def search_bing(q,limit=10):return _generic_search("https://www.bing.com/search",q,"bing",limit)
def search_yahoo(q,limit=10):return _generic_search("https://search.yahoo.com/search",q,"yahoo",limit)
def search_engine(engine,query,limit):
    if engine=="google":return [WebSearchResult("google",x.title,x.url) for x in search_google(query,limit=limit)]
    if engine=="bing":return search_bing(query,limit)
    return search_yahoo(query,limit)
def search_web_diagnostic(query,settings,diagnostics):
    combined=[];seen=set()
    for engine in settings.enabled_engines():
        d=diagnostics.setdefault(engine,EngineDiagnostic(engine));d.queries+=1
        try:
            rows=search_engine(engine,query,settings.max_results);d.status="success" if rows else ("empty" if d.status not in ("success","blocked","failed") else d.status);d.results+=len(rows)
        except Exception as exc:
            msg=f"{type(exc).__name__}: {str(exc)[:160]}";d.error=msg
            d.status="blocked" if any(x in msg.lower() for x in ("blocked","captcha","403","429","unusual traffic")) else "failed";rows=[]
        useful=[]
        for row in rows:
            if row.url in seen:continue
            seen.add(row.url);combined.append(row);useful.append(row)
        if settings.mode==SearchMode.FALLBACK and useful:break
    return combined
def search_web(query,settings):
    return search_web_diagnostic(query,settings,{})
