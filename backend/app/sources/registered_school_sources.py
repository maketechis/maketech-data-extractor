from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RegisteredSource:
    name:str;url:str;states:tuple[str,...];kind:str;priority:int;note:str
SOURCES=(
    RegisteredSource("Ministry of Education Bihar PAB school tables","https://dsel.education.gov.in/sites/default/files/2022-06/pab_bihar_22_23.pdf",("Bihar",),"pdf",95,"Official Ministry school-level tables; historical 2022-23 source"),
    RegisteredSource("AIM Operational Atal Tinkering Labs","https://aim.gov.in/pdf/4_7_2022_OperationalATLsInIndia.pdf",("Bihar",),"pdf",75,"Official NITI Aayog school list; supplemental historical source"),
    RegisteredSource("Bihar Sanskrit Shiksha Board institutions","https://bssb.bihar.gov.in/institutions",("Bihar",),"html",85,"Official Bihar board institution registry"),
)
def for_state(state:str):
    return [x for x in SOURCES if state.casefold() in {s.casefold() for s in x.states}]
