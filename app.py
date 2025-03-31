import streamlit as st
import spacy
import PyPDF2
import docx
from textblob import TextBlob
import os

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read resume
def read_resume(file):
    ext = os.path.splitext(file.name)[1]
    if ext == ".pdf":
        return extract_text_from_pdf(file)
    elif ext == ".docx":
        return extract_text_from_docx(file)
    return ""

# Function to analyze resume
def analyze_resume(text):
    doc = nlp(text)

    # Readability Score (Simple Estimation)
    num_sentences = len(list(doc.sents))
    num_words = len(doc)
    readability_score = round((num_words / num_sentences) if num_sentences else 0, 2)

    # Extract Keywords
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    # Sentiment Analysis
    sentiment = TextBlob(text).sentiment.polarity

    return {
        "word_count": num_words,
        "sentence_count": num_sentences,
        "readability_score": readability_score,
        "top_keywords": keywords[:10],
        "sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    }

# Streamlit UI
st.title("📄 Resume Analyzer")
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.subheader("Extracted Text")
    resume_text = read_resume(uploaded_file)
    st.text_area("Resume Content", resume_text, height=200)

    if st.button("Analyze Resume"):
        result = analyze_resume(resume_text)
        st.subheader("🔍 Analysis Results")
        st.write(f"📌 **Word Count:** {result['word_count']}")
        st.write(f"📌 **Sentence Count:** {result['sentence_count']}")
        st.write(f"📌 **Readability Score:** {result['readability_score']}")
        st.write(f"📌 **Top Keywords:** {', '.join(result['top_keywords'])}")
        st.write(f"📌 **Sentiment Analysis:** {result['sentiment']}")
