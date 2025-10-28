"""
Invoice Processing Pipeline
Combines Gemini OCR + GPT-5 Extraction
"""

from typing import Dict, Any, List
from src.services.parsing_service import describe_pdf
from src.services.extracting_service import extract_invoice_data


async def process_invoice_pipeline(pdf_path: str) -> List[Dict[str, Any]]:

    try:
        # Step 1: OCR with Gemini
        print("📄 Step 1: Processing PDF with Gemini OCR...")
        gemini_ocr_output = await describe_pdf(pdf_path)
        print(f"✅ Gemini OCR complete. Output length: {len(gemini_ocr_output)} characters")
        
        # Step 2: Extract structured data with GPT-5 (processes each page separately)
        print("🤖 Step 2: Extracting structured data with GPT...")
        invoices_list = await extract_invoice_data(gemini_ocr_output)
        print(f"✅ GPT extraction complete! Extracted {len(invoices_list)} invoice(s)")
        
        return invoices_list
        
    except Exception as e:
        print(f"❌ Error in pipeline: {str(e)}")
        raise Exception(f"Invoice processing pipeline failed: {str(e)}")
