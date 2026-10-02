import csv,io,re
from dataclasses import asdict,dataclass
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup
@dataclass(slots=True)
class ExtractedEntity:
    name:str;source_url:str;address:str|None=None;pin:str|None=None;phone:str|None=None;email:str|None=None;website:str|None=None;source_record_id:str|None=None
def _pick(row:dict,*names):
    low={str(k).strip().casefold():str(v).strip() for k,v in row.items() if k is not None}
    return next((low[n.casefold()] for n in names if low.get(n.casefold())),None)
def extract_csv(text:str,url:str)->list[ExtractedEntity]:
    out=[]
    for row in csv.DictReader(io.StringIO(text)):
        name=_pick(row,"school_name","school name","name","institution","institution name")
        if not name:continue
        out.append(ExtractedEntity(name,url,_pick(row,"address"),_pick(row,"pin","pincode","postal code"),_pick(row,"phone","mobile","telephone"),_pick(row,"email","e-mail"),_pick(row,"website","url"),_pick(row,"udise_code","udise code","code","id")))
    return out
def extract_html(text:str,url:str)->list[ExtractedEntity]:
    soup=BeautifulSoup(text,"html.parser");out=[];seen=set()
    for tr in soup.select("tr"):
        cells=[x.get_text(" ",strip=True) for x in tr.select("td")]
        if len(cells)<2:continue
        candidates=[x for x in cells if len(x)>=3 and not x.isdigit()]
        name=next((x for x in candidates if any(k in x.casefold() for k in ("school","vidyal","academy","college","institution","madrasa"))),None)
        if not name:continue
        key=name.casefold()
        if key in seen:continue
        seen.add(key);pin=next((x for x in cells if re.fullmatch(r"\d{6}",x)),None);code=next((x for x in cells if re.fullmatch(r"\d{8,12}",x)),None)
        out.append(ExtractedEntity(name,url,pin=pin,source_record_id=code))
    return out
def extract_source(url:str,timeout:float=30)->dict:
    r=httpx.get(url,timeout=timeout,follow_redirects=True,headers={"User-Agent":"MakeTechDataExtractor/0.6"});r.raise_for_status()
    ct=r.headers.get("content-type","").lower();path=str(r.url).lower()
    if "csv" in ct or path.endswith(".csv"):rows=extract_csv(r.text,url);kind="csv"
    elif "html" in ct or "<html" in r.text[:1000].lower():rows=extract_html(r.text,url);kind="html"
    else:return {"url":url,"kind":"unsupported","records":[],"count":0}
    return {"url":url,"kind":kind,"records":[asdict(x) for x in rows],"count":len(rows)}
