from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DiscoveryQuery:
    query: str
    entity_term: str
    district: str
    state: str
    country: str

DEFAULT_SYNONYMS={
    "bookseller":["bookseller","book shop","book store","book dealer"],
    "school":["school","public school","secondary school","senior secondary school"],
}

def build_discovery_queries(*, entity_type: str, district: str, state: str, country: str, synonyms: list[str] | None=None):
    terms=synonyms or DEFAULT_SYNONYMS.get(entity_type,[entity_type])
    seen=set(); output=[]
    for term in terms:
        query=f'{term} in {district} {state} {country}'
        key=query.casefold()
        if key in seen: continue
        seen.add(key)
        output.append(DiscoveryQuery(query=query,entity_term=term,district=district,state=state,country=country))
    return output
