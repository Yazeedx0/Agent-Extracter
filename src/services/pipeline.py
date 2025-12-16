from typing import Any

from src.services.extracting_service import extract_invoice_data
from src.services.parsing_service import describe_pdf


async def process_invoice_pipeline(pdf_path: str) -> list[dict[str, Any]]:
    try:
        gemini_ocr_output = await describe_pdf(pdf_path)
        invoices_list = await extract_invoice_data(gemini_ocr_output)
        return invoices_list
    except Exception as e:
        raise Exception(f"Invoice processing pipeline failed: {e}")
