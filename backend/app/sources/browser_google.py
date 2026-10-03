from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
import time
from playwright.sync_api import sync_playwright
@dataclass(frozen=True,slots=True)
class BrowserResult:title:str;url:str;page:int;rank:int
def _clean(href):
    if href.startswith("/url?"):
        q=parse_qs(urlparse(href).query);return (q.get("q") or q.get("url") or [""])[0]
    return href
def acquire_google(query:str,*,pages:int=5,delay_seconds:int=20,headless:bool=False):
    results=[];diagnostics=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="chrome",headless=headless)
        context=browser.new_context(locale="en-IN");page=context.new_page()
        for n in range(1,pages+1):
            try:
                page.goto("https://www.google.com/search",wait_until="domcontentloaded",timeout=45000)
                page.locator('textarea[name="q"],input[name="q"]').first.fill(query)
                page.keyboard.press("Enter");page.wait_for_load_state("domcontentloaded")
                if n>1:
                    page.goto("https://www.google.com/search?q="+__import__("urllib.parse",fromlist=["quote_plus"]).quote_plus(query)+"&start="+str((n-1)*10),wait_until="domcontentloaded",timeout=45000)
                low=page.content().lower()
                if "unusual traffic" in low or "captcha" in low:
                    diagnostics.append({"page":n,"status":"human_check","results":0,"error":"Google requires human verification in the visible browser."});break
                rows=[];seen=set()
                for h in page.locator("h3").all():
                    a=h.locator("xpath=ancestor::a[1]")
                    if a.count()==0:continue
                    href=_clean(a.get_attribute("href") or "");parsed=urlparse(href)
                    if parsed.scheme not in ("http","https") or "google." in parsed.netloc.lower() or href in seen:continue
                    seen.add(href);rows.append(BrowserResult(h.inner_text().strip(),href,n,len(rows)+1))
                results.extend(rows);diagnostics.append({"page":n,"status":"success","results":len(rows),"error":None})
                if n<pages:time.sleep(delay_seconds)
            except Exception as exc:diagnostics.append({"page":n,"status":"failed","results":0,"error":f"{type(exc).__name__}: {str(exc)[:300]}"})
        context.close();browser.close()
    return results,diagnostics
