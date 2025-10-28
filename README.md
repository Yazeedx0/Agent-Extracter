# OCR Agent - Invoice Extraction System

An intelligent invoice extraction system that combines Google Gemini OCR with OpenAI GPT for accurate, structured data extraction from PDF invoices.

##  Features

- **Dual-Model Architecture**: 
  -  **Gemini 2.5 Pro** for advanced OCR and document understanding
  -  **GPT-4/GPT-5** for intelligent data extraction and structuring
  
- **Bilingual Support**: Handles Arabic and English text seamlessly
- **Smart Extraction**: Extracts invoices with semantic understanding
- **RESTful API**: FastAPI-based endpoints for easy integration

##  Architecture

```
PDF Invoice → Gemini OCR → GPT-5 Extraction → Structured JSON
```

1. **Gemini OCR**: Extracts all text, tables, and visual data from PDF
2. **GPT-5 Processing**: Parses and structures the data according to schema
3. **Validation**: Returns clean, validated JSON output

## Extracted Fields

- Invoice ID & Date
- Supplier Information (Name, Address, VAT)
- Customer Information (Name, Address, VAT)
- Line Items (Description, Quantity, Price, Unit, Total)
- Financial Totals (Subtotal, Tax, Total Amount)
- Payment Method & Notes
- Currency

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API Key
- Google Gemini API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Yazeedx0/Agent-Parser.git
cd OCR_Agent
```

2. Create virtual environment:
```bash
python3 -m venv env
source env/bin/activate  # On Linux/Mac
# or
env\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Running the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### 1. Extract Invoice (Full Pipeline)

**Endpoint**: `POST /extract-invoice`

Processes a PDF invoice through the complete Gemini → GPT-5 pipeline.

**Request**:
```bash
curl -X POST "http://localhost:8000/extract-invoice" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@invoice.pdf"
```

**Response**:
```json
{
  "filename": "invoice.pdf",
  "status": "success",
  "invoice_data": {
    "invoice_id": "INV-2024-001",
    "invoice_date": "2024-01-15",
    "supplier": {
      "name": "ZEIDAN TRADING AGENCY",
      "address": "Amman, Jordan",
      "vat_number": "123456789"
    },
    "customer": {
      "name": "Customer Name",
      "address": "Customer Address",
      "vat_number": "987654321"
    },
    "items": [
      {
        "description": "Product Name",
        "quantity": 10,
        "unit_price": 50.0,
        "unit": "pcs",
        "total": 500.0
      }
    ],
    "subtotal": 500.0,
    "tax": 75.0,
    "total_amount": 575.0,
    "currency": "JOD",
    "payment_method": "Cash",
    "invoice_notes": "Thank you for your business"
  }
}
```

### 2. Describe PDF (Gemini OCR Only)

**Endpoint**: `POST /describe-pdf`

Gets raw OCR output from Gemini without GPT processing.

**Request**:
```bash
curl -X POST "http://localhost:8000/describe-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### Model Configuration

- **Gemini Model**: `gemini-2.5-pro` (in `parsing_service.py`)
- **OpenAI Model**: `gpt-4o` (in `extracting_service.py`)
  - Will use GPT-5 when available

## Project Structure

```
OCR_Agent/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment variables template
└── src/
    ├── api/
    │   └── routes.py      # API endpoints
    ├── services/
    │   ├── parsing_service.py     # Gemini OCR service
    │   ├── extracting_service.py  # GPT-5 extraction service
    │   └── pipeline.py            # Complete processing pipeline
    ├── models/
    │   └── schema.py      # Pydantic schemas
    └── helpers/
        └── config.py      # Configuration settings
```

## Development

### Adding New Features

1. **Add new extraction fields**: Update schemas in `src/models/schema.py`
2. **Modify prompts**: Edit prompts in `src/services/extracting_service.py`
3. **Add endpoints**: Create new routes in `src/api/routes.py`

### Testing

Test the API using the interactive docs at `http://localhost:8000/docs`
