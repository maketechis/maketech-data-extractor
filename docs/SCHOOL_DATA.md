# Structured school data

School-specific attributes are stored separately from the generic Entity record.

Generic Entity:
name, geography, address, PIN, coordinates, contacts, websites, sources, verification.

SchoolProfile:
UDISE code, block, village/town, management, category, board, plus future source-specific structured attributes.

UDISE code is unique when present and is the strongest school identity key. Schools without a UDISE code can still enter the generic matching/review workflow.

Normalized import contract:
udise_code,school_name,state,district,block,village_town,address,pin,management,category,board

The importer expects geography to already exist, preventing accidental creation of misspelled states/districts from school source files.
