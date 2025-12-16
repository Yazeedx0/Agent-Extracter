from pydantic import BaseModel, Field


class PDFDescriptionResponse(BaseModel):
    filename: str
    description: str
    status: str = "success"


class ImageDescriptionResponse(BaseModel):
    filename: str
    description: str
    status: str = "success"


class Supplier(BaseModel):
    name: str | None = None
    address: str | None = None
    vat_number: str | None = None


class Customer(BaseModel):
    name: str | None = None
    address: str | None = None
    vat_number: str | None = None


class InvoiceItem(BaseModel):
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    unit: str | None = None
    total: float | None = None


class InvoiceData(BaseModel):
    invoice_id: str | None = None
    invoice_date: str | None = None
    supplier: Supplier | None = None
    customer: Customer | None = None
    items: list[InvoiceItem] = Field(default_factory=list)
    subtotal: float | None = None
    tax: float | None = None
    total_amount: float | None = None
    currency: str | None = "JOD"
    payment_method: str | None = None
    invoice_notes: str | None = None


class InvoiceExtractionResponse(BaseModel):
    filename: str
    invoice_data: list[InvoiceData]
    status: str = "success"
    total_invoices: int
