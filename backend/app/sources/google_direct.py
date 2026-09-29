from dataclasses import dataclass
from urllib.parse import quote_plus,urlparse
import httpx
from bs4 import BeautifulSoup

GOOGLE_SEARCH_URL="https://www.google.com/search"

@dataclass(frozen=True,slots=True)
class GoogleResult:
    title:str
    url:str

def build_google_query(*,entity_type:str,district:str,state:str,country:str,name:str|None=None)->str:
    return " ".join(x for x in [f'"{name}"' if name else entity_type,district,state,country] if x)

def search_google(query:str,*,limit:int=10,timeout:float=15.0)->list[GoogleResult]:
    headers={"User-Agent":"Mozilla/5.0 (compatible; MakeTechDataExtractor/0.1)"}
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:
        response=client.get(GOOGLE_SEARCH_URL,params={"q":query,"num":min(limit,10)})
        response.raise_for_status()
    text=response.text.lower()
    if "unusual traffic" in text or "captcha" in text:
        raise RuntimeError("Google search is temporarily blocked or requires human verification")
    soup=BeautifulSoup(response.text,"html.parser"); results=[]; seen=set()
    for a in soup.select("a[href]"):
        href=a.get("href","")
        if href.startswith("/url?q="): href=href.split("/url?q=",1)[1].split("&",1)[0]
        parsed=urlparse(href)
        if parsed.scheme not in ("http","https") or "google." in parsed.netloc.lower(): continue
        title=a.get_text(" ",strip=True)
        if not title or href in seen: continue
        seen.add(href); results.append(GoogleResult(title,href))
        if len(results)>=limit: break
    return results
