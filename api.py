# api.py
import spacy

from textblob import TextBlob

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def ner(text):
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return {"entities": entities}

def sentiment(text):
    blob=TextBlob(text)
    sentiment=blob.sentiment

    return {
        "polarity": sentiment.polarity,  # -1 (negative) to +1 (positive)
        "subjectivity": sentiment.subjectivity  # 0 (objective) to 1 (subjective)
    }

def extract_keywords(text):
    doc = nlp(text)

    # Extract nouns and proper nouns only, remove stop words and punctuation
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and token.is_alpha]

    # Deduplicate and sort
    keywords = list(set(keywords))

    return keywords