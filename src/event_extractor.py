import spacy

nlp = spacy.load("en_core_web_sm")

def extract_event_info(text):
    doc = nlp(text)

    # Extract DATE entities
    dates = [ent for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]

    # Extract LOCATION entities
    locations = [ent for ent in doc.ents if ent.label_ in ("LOC", "GPE", "FAC")]
    
	# Extract date and location texts for output
    date_text = dates[0] if dates else None
    location_text = locations[0] if locations else None

    # Remove date and location spans from original text to isolate event name
    spans_to_remove = dates + locations
    spans_to_remove = sorted(spans_to_remove, key=lambda ent: ent.start_char, reverse=True)

    event_name_text = text
    for span in spans_to_remove:
        start, end = span.start_char, span.end_char
        event_name_text = event_name_text[:start] + event_name_text[end:]

    # Clean leftover event name text
    # event_name_text = event_name_text.strip()
    # Optionally, remove prepositions or connecting words like "on", "in", "at"
    event_name_text = event_name_text.replace(" on ", " ").replace(" in ", " ").replace(" at ", " ")

    # Further clean extra spaces
    event_name_text = " ".join(event_name_text.split())

    return {
		"event_name": event_name_text if event_name_text else None,
		"date": date_text.text if date_text else None,
		"location": location_text.text if location_text else None,
	}
