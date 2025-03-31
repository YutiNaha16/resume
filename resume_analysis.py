import spacy
import PyPDF2
import docx
from textblob import TextBlob
import os

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

# Read Resume and Extract Text
def read_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    return ""

# Analyze Resume
def analyze_resume(file_path):
    text = read_resume(file_path)
    if not text:
        return {"error": "Could not extract text from the file."}

    doc = nlp(text)

    # Readability Score Calculation
    num_sentences = len(list(doc.sents))
    num_words = len(doc)
    readability_score = round((num_words / num_sentences) if num_sentences else 0, 2)

    # Extract Keywords (Unique Proper Nouns & Nouns)
    keywords = list(set(token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]))

    # Sentiment Analysis
    sentiment_polarity = TextBlob(text).sentiment.polarity
    sentiment = "Positive" if sentiment_polarity > 0 else "Negative" if sentiment_polarity < 0 else "Neutral"

    return {
        "word_count": num_words,
        "sentence_count": num_sentences,
        "readability_score": readability_score,
        "top_keywords": keywords[:10],
        "sentiment": sentiment
    }
