import re
from dataclasses import dataclass
from bs4 import BeautifulSoup
from app.collector.normalizer import normalize_email, normalize_phone

EMAIL_RE=re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",re.I)
PHONE_RE=re.compile(r"(?:\+?91[\s.-]?)?[6-9]\d(?:[\s.-]?\d){8}")
PIN_RE=re.compile(r"(?<!\d)([1-9][0-9]{5})(?!\d)")

@dataclass(frozen=True, slots=True)
class ExtractedValue:
    field: str
    value: str
    confidence: float
    source_url: str
    method: str

def _unique(items):
    seen=set(); out=[]
    for item in items:
        key=(item.field,item.value)
        if key not in seen:
            seen.add(key); out.append(item)
    return out

def extract_contacts(html: str, source_url: str) -> list[ExtractedValue]:
    soup=BeautifulSoup(html,"html.parser")
    results=[]
    for a in soup.select('a[href^="mailto:"]'):
        value=normalize_email(a.get("href","").split(":",1)[1].split("?",1)[0])
        if value: results.append(ExtractedValue("email",value,1.0,source_url,"mailto"))
    for a in soup.select('a[href^="tel:"]'):
        value=normalize_phone(a.get("href","").split(":",1)[1])
        if value: results.append(ExtractedValue("phone",value,1.0,source_url,"tel"))
    text=soup.get_text(" ",strip=True)
    for value in EMAIL_RE.findall(text):
        normalized=normalize_email(value)
        if normalized: results.append(ExtractedValue("email",normalized,0.85,source_url,"text_regex"))
    for value in PHONE_RE.findall(text):
        normalized=normalize_phone(value)
        if normalized and len(normalized)==10: results.append(ExtractedValue("phone",normalized,0.80,source_url,"text_regex"))
    for value in PIN_RE.findall(text):
        results.append(ExtractedValue("pin",value,0.75,source_url,"india_pin_regex"))
    for node in soup.select('[itemprop="address"], address, .address, #address'):
        value=" ".join(node.stripped_strings)
        if len(value)>=10: results.append(ExtractedValue("address",value[:1000],0.85,source_url,"address_element"))
    return _unique(results)
