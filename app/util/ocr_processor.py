import pytesseract
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_fields(text):
    import re
    merchant = text.split('\n')[0]
    date_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    amount_match = re.search(r'Total\s*\$?(\d+(\.\d{2})?)', text, re.IGNORECASE)

    return {
        "merchant_name": merchant,
        "purchased_at": date_match.group() if date_match else "Unknown",
        "total_amount": float(amount_match.group(1)) if amount_match else 0.0
    }
