import httpx
from bs4 import BeautifulSoup

def fetch_page_text(url: str, timeout: float=15.0) -> str:
    headers={"User-Agent":"MakeTechDataExtractor/0.1 (verification)"}
    response=httpx.get(url,headers=headers,timeout=timeout,follow_redirects=True)
    response.raise_for_status()
    soup=BeautifulSoup(response.text,"html.parser")
    for node in soup(["script","style","noscript"]): node.decompose()
    return soup.get_text(" ",strip=True)
