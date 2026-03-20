from pypdf import PdfReader

def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_chunks = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)

    return "\n".join(text_chunks)
