from io import BytesIO
from openpyxl import Workbook
from app.source_extraction.service import extract_xlsx
def test_xlsx_extracts_school():
    wb=Workbook();ws=wb.active;ws.append(["school_name","udise_code","pin"]);ws.append(["Alpha School","12345678901","841226"]);b=BytesIO();wb.save(b)
    rows=extract_xlsx(b.getvalue(),"https://x/data.xlsx")
    assert rows[0].name=="Alpha School" and rows[0].source_record_id=="12345678901"
