import re
from urllib.parse import urlparse
SCHOOL_TERMS=("school","vidyal","academy","madrasa","विद्यालय","स्कूल")
BAD_NAMES=("institutions","institution","schools","school list","directory")
def validate_record(row:dict,*,district:str,state:str)->tuple[bool,str]:
    name=" ".join(str(row.get("name") or "").split());low=name.casefold()
    if len(name)<4:return False,"name_too_short"
    if low in BAD_NAMES:return False,"generic_heading"
    if not any(x in low for x in SCHOOL_TERMS):return False,"not_school_like"
    if any(x in low for x in ("examination board","education board","school examination board","council","directorate","department of education")):return False,"organization_not_school"
    website=row.get("website")
    if website:
        host=urlparse(website).netloc.casefold()
        if any(x in host for x in ("google.com","google.co.","bing.com","yahoo.com")):row["website"]=None
    address=(row.get("address") or "").casefold()
    if address and state.casefold() not in address and district.casefold() not in address:
        return False,"geography_mismatch"
    return True,"accepted"
def filter_records(records:list[dict],*,district:str,state:str)->tuple[list[dict],dict]:
    accepted=[];rejected={}
    for row in records:
        ok,reason=validate_record(row,district=district,state=state)
        if ok:accepted.append(row)
        else:rejected[reason]=rejected.get(reason,0)+1
    return accepted,{"accepted":len(accepted),"rejected":sum(rejected.values()),"reasons":rejected}
