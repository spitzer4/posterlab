import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_event_info(text):
    doc = nlp(text)

    # Hold detected values
    date_span = None
    location_span = None

    # Collect spans for removal
    spans_to_remove = []

    for ent in doc.ents:
        if ent.label_ == "DATE" and date_span is None:
            date_span = ent
            spans_to_remove.append(ent)
        elif ent.label_ in {"GPE", "LOC"} and location_span is None:
            location_span = ent
            spans_to_remove.append(ent)

    # Sort spans in reverse so we can safely slice the string
    spans_to_remove = sorted(spans_to_remove, key=lambda ent: ent.start_char, reverse=True)

    # Start with the original text for event name removal
    event_name_text = text
    for span in spans_to_remove:
        event_name_text = event_name_text[:span.start_char] + event_name_text[span.end_char:]

    # If we found a date/location, convert to strings
    date_text = date_span.text if date_span else None
    location_text = location_span.text if location_span else None

    # If no location found, keep original event_name_text (with location inside)
    if not location_text and not spans_to_remove:
        event_name_text = text
    else:
        # Clean up extra spaces and remove stray prepositions
        event_name_text = re.sub(r"\b(on|in|at)\b", "", event_name_text, flags=re.IGNORECASE)

    # Final tidy up
    event_name_text = " ".join(event_name_text.split())  # normalize spaces

    return {
        "event_name": event_name_text,
        "date": date_text or "",
        "location": location_text or ""
    }
