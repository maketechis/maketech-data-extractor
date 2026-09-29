import httpx
from bs4 import BeautifulSoup
from app.security.urls import validate_public_http_url

def fetch_page_text(url:str,timeout:float=15.0)->str:
    headers={"User-Agent":"MakeTechDataExtractor/0.1 (verification)"}
    current=validate_public_http_url(url)
    with httpx.Client(timeout=timeout,headers=headers,follow_redirects=False) as client:
        for _ in range(5):
            response=client.get(current)
            if response.is_redirect:
                current=validate_public_http_url(str(response.next_request.url))
                continue
            response.raise_for_status()
            soup=BeautifulSoup(response.text,"html.parser")
            for node in soup(["script","style","noscript"]): node.decompose()
            return soup.get_text(" ",strip=True)
    raise ValueError("Too many redirects")
