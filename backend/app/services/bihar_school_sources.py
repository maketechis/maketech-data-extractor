import re
from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup
@dataclass(frozen=True,slots=True)
class OfficialSchool:
    name:str;udise_code:str|None;district:str;source_url:str;management:str|None=None;category:str|None=None
BSSB_URL="https://bssb.bihar.gov.in/institutions"
def fetch_bssb(district:str="Siwan",timeout:float=30.0)->list[OfficialSchool]:
    r=httpx.get(BSSB_URL,timeout=timeout,follow_redirects=True,headers={"User-Agent":"MakeTechDataExtractor/0.5"});r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser");out=[];seen=set()
    for tr in soup.select("tr"):
        cells=[x.get_text(" ",strip=True) for x in tr.select("td")]
        if len(cells)<4 or cells[1].casefold()!=district.casefold():continue
        name=cells[2].strip();udise=next((x for x in cells if re.fullmatch(r"\d{11}",x)),None)
        key=(name.casefold(),udise)
        if name and key not in seen:seen.add(key);out.append(OfficialSchool(name,udise,district,BSSB_URL,category=cells[4] if len(cells)>4 else None))
    return out
