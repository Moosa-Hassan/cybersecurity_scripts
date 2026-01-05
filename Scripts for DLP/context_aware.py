import PyPDF2
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

candidate_labels = [
    "Confidential: any sensitive or private information (e.g. PII, financials, trade secrets)",
    "Internal: organization-wide information about company's policies and projects",
    "Public: information that is publicly available or non-sensitive",
]

def classify_text(text):

    result = classifier(text, candidate_labels=candidate_labels)
    classification = result['labels'][0]
    confidence = result['scores'][0]
    return (classification, confidence)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def process_classification(label):
    if "Confidential:" in label:
        return "Confidential"
    elif "Internal:" in label:
        return "Internal"
    elif "Public:" in label:
        return "Public"
    return "Unknown"

pdf_path = "context/Internship Research.pdf"
print("Processing file:", pdf_path)
text_content = extract_text_from_pdf(pdf_path)
classification, confidence = classify_text(text_content)
label = process_classification(classification)
print("Classification Result:", label, " with confidence ", confidence)



