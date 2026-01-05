from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = ["Restricted", "Confidential", "Internal", "Public"]

text = "This document describes a trade secret algorithm used internally."

result = classifier(text, candidate_labels=labels)
print(result)
