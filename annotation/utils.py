"""Utility functions for the annotations app."""
from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    """Extract text from pdf."""
    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text
