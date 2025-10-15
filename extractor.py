import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
"""Module for extracting text from PDF and image files."""

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file. If the PDF is scanned (image-based), use OCR to extract text."""   
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
        if full_text.strip() == "":
            pages = convert_from_path(pdf_path, 300)
            for page in pages:
                text = pytesseract.image_to_string(page)
                full_text += text
    return full_text


def extract_text_from_image(image_path):
    """Extract text from an image file using OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def main():
    # Example usage of the functions
    pdf_path = "sample.pdf"  # Replace with your PDF file path
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    print("Extracted text from PDF:")
    print(pdf_text)
    

if __name__ == "__main__":
    main()