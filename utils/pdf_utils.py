import io

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

ocr_available = False
try:
    import pytesseract
    from pdf2image import convert_from_bytes
    ocr_available = True
except Exception:
    ocr_available = False


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""

    if PdfReader:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception:
            pass

    if text.strip():
        return text.strip()

    if ocr_available:
        try:
            images = convert_from_bytes(pdf_bytes)
            return "\n".join(
                pytesseract.image_to_string(img) for img in images
            ).strip()
        except Exception:
            pass

    return ""
