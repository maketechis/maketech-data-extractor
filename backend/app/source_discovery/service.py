from dataclasses import asdict,dataclass
from urllib.parse import urlparse
from app.sources.search_settings import SearchSettings
from app.sources.web_search import EngineDiagnostic,search_web_diagnostic
@dataclass(slots=True)
class DiscoveredSource:
    url:str;title:str;engine:str;kind:str;score:int;query:str
def classify(url:str,title:str)->tuple[str,int]:
    u=url.lower();t=title.lower();score=0;kind="page"
    if u.endswith(".pdf"):kind="pdf";score+=35
    if u.endswith((".csv",".xlsx",".xls")):kind="dataset";score+=50
    if any(x in u for x in (".gov.in","gov.in/")):kind="government_"+kind;score+=35
    if any(x in t for x in ("list","directory","institutions","schools","affiliation","report")):score+=20
    if any(x in t for x in ("siwan","district")):score+=10
    return kind,min(score,100)
def discovery_queries(entity_type:str,district:str,state:str,country:str)->list[str]:
    return [f'{entity_type} list {district} {state}',f'{entity_type} directory {district} {state}',f'{entity_type} {district} {state} filetype:pdf',f'{entity_type} {district} {state} filetype:xlsx',f'{entity_type} {district} {state} government list',f'government {entity_type} list {district} {state}',f'private {entity_type} list {district} {state}',f'UDISE {entity_type} {district} {state}',f'CBSE {entity_type} {district} {state} affiliation',f'{entity_type} institutions {district} {state}',f'{entity_type} affiliation list {district} {state}',f'{district} district education {entity_type} report']
def discover_sources(*,entity_type:str,district:str,state:str,country:str,settings:SearchSettings)->dict:
    found={};metrics={x:{"results":0,"sources":0} for x in settings.enabled_engines()};diagnostics={x:EngineDiagnostic(x) for x in settings.enabled_engines()}
    for q in discovery_queries(entity_type,district,state,country):
        for hit in search_web_diagnostic(q,settings,diagnostics):
            metrics.setdefault(hit.engine,{"results":0,"sources":0});metrics[hit.engine]["results"]+=1
            kind,score=classify(hit.url,hit.title)
            host=urlparse(hit.url).netloc.lower()
            key=hit.url.split("#",1)[0]
            item=DiscoveredSource(key,hit.title,hit.engine,kind,score,q)
            if key not in found or score>found[key].score:found[key]=item
    if entity_type=="school" and state.casefold()=="bihar":
        from app.services.bihar_school_sources import BSSB_URL
        kind,score=classify(BSSB_URL,"Bihar Sanskrit Shiksha Board institutions")
        found.setdefault(BSSB_URL,DiscoveredSource(BSSB_URL,"Bihar Sanskrit Shiksha Board institutions","registry",kind,max(score,70),"registered official source"))
        metrics.setdefault("registry",{"results":1,"sources":0})
    rows=sorted(found.values(),key=lambda x:(-x.score,x.url))
    for x in rows:metrics[x.engine]["sources"]+=1
    return {"queries":len(discovery_queries(entity_type,district,state,country)),"metrics":metrics,"engines":{k:asdict(v) for k,v in diagnostics.items()},"sources":[asdict(x) for x in rows]}
