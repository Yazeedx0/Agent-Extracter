from pydantic import BaseModel, Field
from typing import Optional, List


class PDFDescriptionResponse(BaseModel):
    filename: str = Field(..., description="Name of the uploaded PDF file")
    description: str = Field(..., description="Description of the PDF content")
    status: str = Field(default="success", description="Processing status")


class ImageDescriptionResponse(BaseModel):
    filename: str = Field(..., description="Name of the uploaded image file")
    description: str = Field(..., description="Description of the image content")
    status: str = Field(default="success", description="Processing status")


# Invoice Extraction Schemas
class Supplier(BaseModel):
    name: Optional[str] = Field(None, description="Supplier/vendor name")
    address: Optional[str] = Field(None, description="Supplier address")
    vat_number: Optional[str] = Field(None, description="Supplier VAT number")


class Customer(BaseModel):
    name: Optional[str] = Field(None, description="Customer name")
    address: Optional[str] = Field(None, description="Customer address")
    vat_number: Optional[str] = Field(None, description="Customer VAT number")


class InvoiceItem(BaseModel):
    description: Optional[str] = Field(None, description="Item description")
    quantity: Optional[float] = Field(None, description="Quantity")
    unit_price: Optional[float] = Field(None, description="Unit price")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    total: Optional[float] = Field(None, description="Total price for this item")


class InvoiceData(BaseModel):
    invoice_id: Optional[str] = Field(None, description="Invoice ID/Number")
    invoice_date: Optional[str] = Field(None, description="Invoice date")
    supplier: Optional[Supplier] = Field(None, description="Supplier information")
    customer: Optional[Customer] = Field(None, description="Customer information")
    items: Optional[List[InvoiceItem]] = Field(default_factory=list, description="List of invoice items")
    subtotal: Optional[float] = Field(None, description="Subtotal amount")
    tax: Optional[float] = Field(None, description="Tax amount")
    total_amount: Optional[float] = Field(None, description="Total amount")
    currency: Optional[str] = Field("JOD", description="Currency code")
    payment_method: Optional[str] = Field(None, description="Payment method")
    invoice_notes: Optional[str] = Field(None, description="Additional notes")


class InvoiceExtractionResponse(BaseModel):
    filename: str = Field(..., description="Name of the uploaded PDF file")
    invoice_data: List[InvoiceData] = Field(..., description="List of extracted invoices (one per page)")
    status: str = Field(default="success", description="Processing status")
    total_invoices: int = Field(..., description="Total number of invoices extracted")
