"""
PDF text extraction service
Uses PyMuPDF (fitz) to extract text from PDF files
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF file content
    
    Args:
        pdf_content: PDF file as bytes
        
    Returns:
        Extracted text as string
    """
    # Open PDF from bytes
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    
    text_parts = []
    
    # Extract text from each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        if text.strip():
            text_parts.append(text)
    
    pdf_document.close()
    
    # Join all text with spaces
    full_text = " ".join(text_parts)
    
    # Clean up whitespace
    full_text = " ".join(full_text.split())
    
    return full_text
