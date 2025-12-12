import pytesseract
from PIL import Image
from nltk.tokenize import sent_tokenize

def extract_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text.strip()

def summarize_text(text, max_sentences=2):
    sentences = sent_tokenize(text)
    return " ".join(sentences[:max_sentences])
