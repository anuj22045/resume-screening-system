import io
import pdfplumber
import docx


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from an uploaded DOCX file."""
    file_bytes = uploaded_file.read()
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def extract_text(uploaded_file) -> str:
    """
    Auto-detect file type and extract text.
    Supports PDF and DOCX uploads.
    """
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        return ""