from app.enrichment.contact_extractor import extract_contacts
from app.enrichment.site_crawler import discover_priority_links

HTML='''<html><body>
<a href="mailto:Info@ExampleSchool.IN">Email</a>
<a href="tel:+91 98765 43210">Call</a>
<address>ABC School, Main Road, Siwan, Bihar 841226</address>
<a href="/contact-us">Contact us</a>
<a href="https://other.example/contact">External</a>
</body></html>'''

def test_extracts_normalized_contacts_with_evidence():
    values=extract_contacts(HTML,"https://school.example/contact")
    data={(x.field,x.value,x.source_url,x.method) for x in values}
    assert ("email","info@exampleschool.in","https://school.example/contact","mailto") in data
    assert ("phone","9876543210","https://school.example/contact","tel") in data
    assert any(x.field=="pin" and x.value=="841226" for x in values)
    assert any(x.field=="address" and "ABC School" in x.value for x in values)

def test_priority_links_stay_on_domain():
    links=discover_priority_links(HTML,"https://school.example/")
    assert "https://school.example/contact-us" in links
    assert all("other.example" not in x for x in links)
