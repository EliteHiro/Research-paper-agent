import os

from fastapi import FastAPI, UploadFile, File

from app.parsers.pdf_parser import PDFParser
from app.services.paper_service import PaperAnalysisService


os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Research Paper Agent"
)

parser = PDFParser()
service = PaperAnalysisService()


@app.get("/")
def root():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):
    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = parser.extract_text(path)

    result = service.analyze(text)

    return result