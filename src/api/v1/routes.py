import os
import tempfile
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.models.schema import (
    InvoiceData,
    InvoiceExtractionResponse,
    PDFDescriptionResponse,
)
from src.services.parsing_service import describe_pdf
from src.services.pipeline import process_invoice_pipeline

router = APIRouter()


@asynccontextmanager
async def temporary_pdf_file(file: UploadFile) -> AsyncGenerator[str, None]:
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        yield tmp_file_path
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


def validate_pdf_file(file: UploadFile) -> None:
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


@router.post("/describe-pdf", response_model=PDFDescriptionResponse)
async def upload_and_describe_pdf(file: UploadFile = File(...)):
    validate_pdf_file(file)

    try:
        async with temporary_pdf_file(file) as tmp_file_path:
            description = await describe_pdf(tmp_file_path)
            return PDFDescriptionResponse(
                filename=file.filename,
                description=description,
                status="success"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")


@router.post("/extract-invoice", response_model=InvoiceExtractionResponse)
async def extract_invoice(file: UploadFile = File(...)):
    validate_pdf_file(file)

    try:
        async with temporary_pdf_file(file) as tmp_file_path:
            invoices_list = await process_invoice_pipeline(tmp_file_path)
            invoice_data_objects = [InvoiceData(**invoice) for invoice in invoices_list]
            return InvoiceExtractionResponse(
                filename=file.filename,
                invoice_data=invoice_data_objects,
                status="success",
                total_invoices=len(invoice_data_objects)
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting invoice: {e}"
        )
