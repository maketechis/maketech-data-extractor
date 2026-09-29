import re
from urllib.parse import urlparse

def normalize_text(value: str | None) -> str | None:
    if not value: return None
    return " ".join(value.strip().split())

def normalize_name(value: str) -> str:
    value=normalize_text(value) or ""
    return re.sub(r"[^a-z0-9]+"," ",value.lower()).strip()

def normalize_phone(value: str | None) -> str | None:
    if not value: return None
    digits=re.sub(r"\D","",value)
    if len(digits)==12 and digits.startswith("91"): digits=digits[2:]
    return digits or None

def normalize_email(value: str | None) -> str | None:
    return (normalize_text(value) or "").lower() or None

def normalize_website(value: str | None) -> str | None:
    if not value: return None
    value=value.strip()
    if not value.startswith(("http://","https://")): value="https://"+value
    parsed=urlparse(value)
    return parsed.geturl() if parsed.netloc else None
