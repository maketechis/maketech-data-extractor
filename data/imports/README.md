# Collector imports

CSV is the first source adapter and is intended for public/open datasets or manually obtained exports.

Expected fields:

name,state,district,address,pin,phone,email,website,source_name,source_url,source_record_id

System 1 will add additional adapters behind the same interface. Every imported record must retain provenance.
