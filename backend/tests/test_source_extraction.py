from app.source_extraction.service import extract_csv,extract_html
def test_csv_extracts_school_fields():
    rows=extract_csv("school_name,udise_code,pin,email\nAlpha School,12345678901,841226,a@example.org\n","https://x/data.csv")
    assert rows[0].name=="Alpha School" and rows[0].source_record_id=="12345678901" and rows[0].pin=="841226"
def test_html_extracts_school_table():
    rows=extract_html("<table><tr><td>Alpha Public School</td><td>12345678901</td><td>841226</td></tr></table>","https://x/list")
    assert rows and rows[0].name=="Alpha Public School" and rows[0].pin=="841226"
