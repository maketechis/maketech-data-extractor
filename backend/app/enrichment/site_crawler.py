from collections import deque
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from app.enrichment.contact_extractor import extract_contacts

PRIORITY_TERMS=("contact","contact-us","reach-us","about","about-us","location","find-us")

def discover_priority_links(html: str, base_url: str) -> list[str]:
    base_domain=urlparse(base_url).netloc.lower()
    soup=BeautifulSoup(html,"html.parser"); links=[]
    for a in soup.find_all("a",href=True):
        href=urljoin(base_url,a["href"])
        parsed=urlparse(href)
        if parsed.scheme not in ("http","https") or parsed.netloc.lower()!=base_domain: continue
        haystack=(href+" "+a.get_text(" ",strip=True)).lower()
        if any(term in haystack for term in PRIORITY_TERMS): links.append(href.split("#",1)[0])
    return list(dict.fromkeys(links))

def crawl_verified_site(url: str, max_pages: int=5, timeout: float=15.0):
    domain=urlparse(url).netloc.lower(); queue=deque([url]); seen=set(); pages=[]
    headers={"User-Agent":"MakeTechDataExtractor/0.1 (contact enrichment)"}
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=True) as client:
        while queue and len(pages)<max_pages:
            current=queue.popleft()
            if current in seen or urlparse(current).netloc.lower()!=domain: continue
            seen.add(current)
            response=client.get(current); response.raise_for_status()
            if "text/html" not in response.headers.get("content-type","text/html").lower(): continue
            values=extract_contacts(response.text,str(response.url))
            pages.append({"url":str(response.url),"values":values})
            if len(pages)==1:
                queue.extend(discover_priority_links(response.text,str(response.url)))
    return pages
