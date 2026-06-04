import fitz

from app.utils.logger import get_logger


logger = get_logger(__name__)


class PDFParser:

    def extract_text(self, pdf_path: str) -> str:

        logger.info(f"Reading PDF: {pdf_path}")

        document = fitz.open(pdf_path)

        pages = []

        for page_number in range(len(document)):

            page = document[page_number]

            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)
