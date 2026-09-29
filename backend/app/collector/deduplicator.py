from app.collector.normalizer import normalize_name, normalize_phone

def entity_key(name: str, pin: str | None=None, phone: str | None=None) -> tuple:
    return (normalize_name(name), (pin or "").strip(), normalize_phone(phone) or "")

def deduplicate(records):
    seen=set(); output=[]
    for record in records:
        key=entity_key(record.name,record.pin,record.phone)
        if key in seen: continue
        seen.add(key); output.append(record)
    return output
