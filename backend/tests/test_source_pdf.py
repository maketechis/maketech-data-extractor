from app.source_extraction.service import extract_pdf
def test_pdf_text_extracts_school_and_codes(monkeypatch):
    class Page:
        def extract_text(self):return "10123456789 Alpha Public School 841226"
    class Reader:
        def __init__(self,*a,**k):self.pages=[Page()]
    monkeypatch.setattr("app.source_extraction.service.PdfReader",Reader)
    rows=extract_pdf(b"fake","https://x/schools.pdf")
    assert rows and "Alpha Public School" in rows[0].name
    assert rows[0].source_record_id=="10123456789" and rows[0].pin=="841226"

def test_pdf_district_filter(monkeypatch):
    class Page:
        def extract_text(self):return "SIWAN\n10123456789 Alpha Public School 841226\nPATNA\n10111111111 Beta Public School 800001"
    class Reader:
        def __init__(self,*a,**k):self.pages=[Page()]
    monkeypatch.setattr("app.source_extraction.service.PdfReader",Reader)
    rows=extract_pdf(b"fake","https://x/schools.pdf",district="Siwan")
    assert any("Alpha" in x.name for x in rows)
