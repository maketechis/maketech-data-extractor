from collections import deque
from urllib.parse import urljoin,urlparse
import httpx
from bs4 import BeautifulSoup
from app.enrichment.contact_extractor import extract_contacts
from app.security.urls import validate_public_http_url
PRIORITY_TERMS=("contact","contact-us","reach-us","about","about-us","location","find-us")
MAX_RESPONSE_BYTES=2000000
def discover_priority_links(html,base_url):
    domain=urlparse(base_url).netloc.lower(); soup=BeautifulSoup(html,"html.parser"); links=[]
    for a in soup.find_all("a",href=True):
        href=urljoin(base_url,a["href"]); p=urlparse(href)
        if p.scheme in ("http","https") and p.netloc.lower()==domain and any(t in (href+" "+a.get_text(" ",strip=True)).lower() for t in PRIORITY_TERMS): links.append(href.split("#",1)[0])
    return list(dict.fromkeys(links))
def crawl_verified_site(url,max_pages=5,timeout=15.0):
    url=validate_public_http_url(url); domain=urlparse(url).netloc.lower(); queue=deque([url]); seen=set(); pages=[]
    with httpx.Client(timeout=timeout,headers={"User-Agent":"MakeTechDataExtractor/0.1"},follow_redirects=False) as client:
        while queue and len(pages)<max_pages:
            current=validate_public_http_url(queue.popleft())
            if current in seen or urlparse(current).netloc.lower()!=domain: continue
            seen.add(current)
            for _ in range(5):
                response=client.get(current)
                if response.is_redirect:
                    current=validate_public_http_url(str(response.next_request.url))
                    if urlparse(current).netloc.lower()!=domain: raise ValueError("Cross-domain redirect blocked")
                    continue
                response.raise_for_status(); break
            else: raise ValueError("Too many redirects")
            if "text/html" not in response.headers.get("content-type","").lower(): continue
            if len(response.content)>MAX_RESPONSE_BYTES: raise ValueError("HTML response too large")
            final=str(response.url); pages.append({"url":final,"values":extract_contacts(response.text,final)})
            if len(pages)==1: queue.extend(discover_priority_links(response.text,final))
    return pages
