import spacy

nlp = spacy.load("en_core_web_sm")

def extract_event_info(text):
    doc = nlp(text)

    # Extract DATE entities
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    # Extract LOCATION entities
    locations = [ent.text for ent in doc.ents if ent.label_ in ("LOC", "GPE", "FAC")]

    # Heuristic for event name via noun chunks without leading ignored adjectives
    adjectives_to_ignore = {"fun", "great", "awesome", "cool"}

    event_candidates = []
    for chunk in doc.noun_chunks:
        if chunk[0].pos_ == "ADJ" and chunk[0].text.lower() in adjectives_to_ignore:
            event_name = chunk[1:].text
        else:
            event_name = chunk.text
        event_candidates.append(event_name)

    event_name = max(event_candidates, key=len) if event_candidates else ""

    return {
        "event_name": event_name.strip(),
        "date": dates[0] if dates else None,
        "location": locations[0] if locations else None,
    }
