from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.services.parsing_service import describe_pdf
from src.services.pipeline import process_invoice_pipeline
from src.models.schema import PDFDescriptionResponse, InvoiceExtractionResponse, InvoiceData
import tempfile
import os

router = APIRouter()

@router.post("/describe-pdf", response_model=PDFDescriptionResponse)
async def upload_and_describe_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and get its description using Gemini 2.5 Pro
    
    Args:
        file: PDF file to process
    
    Returns:
        PDFDescriptionResponse containing the description
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process the PDF with Gemini
        description = await describe_pdf(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return PDFDescriptionResponse(
            filename=file.filename,
            description=description,
            status="success"
        )
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )


@router.post("/extract-invoice", response_model=InvoiceExtractionResponse)
async def extract_invoice(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process the invoice through the complete pipeline
        # Returns a list of invoices (one per page)
        invoices_list = await process_invoice_pipeline(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        # Convert list of invoices to InvoiceData objects
        invoice_data_objects = [InvoiceData(**invoice) for invoice in invoices_list]
        
        return InvoiceExtractionResponse(
            filename=file.filename,
            invoice_data=invoice_data_objects,  # Now a list of invoices
            status="success",
            total_invoices=len(invoice_data_objects)
        )
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting invoice: {str(e)}"
        )
