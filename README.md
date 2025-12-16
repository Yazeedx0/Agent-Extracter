
# OCR Agent - Intelligent Invoice Extraction System

An AI-powered invoice extraction system that combines **Google Gemini OCR** with **OpenAI GPT** to convert PDF invoices into accurate, structured JSON data.

![OCR](https://github.com/user-attachments/assets/671dfaba-b235-4183-a54d-a0e581aa1e95)

---

## 🚀 Features

* **Dual-Model Architecture**

  * **Gemini 2.5 Pro** - Advanced OCR, layout detection, and document understanding
  * **GPT-4 / GPT-5** - Intelligent semantic extraction and data structuring

* **Bilingual Support**
  Seamlessly processes **Arabic and English** invoices.

* **Smart Semantic Extraction**
  Understands invoice context, tables, and relationships—not just raw text.

* **RESTful API**
  FastAPI-powered endpoints for easy integration into existing systems.

---

## 🧠 System Architecture

```
PDF Invoice → Gemini OCR → GPT-5 Extraction → Structured JSON
```

**Pipeline Overview**

1. **Gemini OCR**
   Extracts text, tables, and visual layout from PDF invoices.

2. **GPT Processing**
   Interprets and structures the extracted content based on a predefined schema.

3. **Validation Layer**
   Returns clean, validated, production-ready JSON output.

---

## 📄 Extracted Invoice Fields

* Invoice ID & Date
* Supplier Information (Name, Address, VAT)
* Customer Information (Name, Address, VAT)
* Line Items (Description, Quantity, Unit, Unit Price, Total)
* Financial Totals (Subtotal, Tax, Grand Total)
* Payment Method
* Notes
* Currency

---

## ⚡ Quick Start

### Prerequisites

* Python **3.12+**
* OpenAI API Key
* Google Gemini API Key

---

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Yazeedx0/Agent-Parser.git
cd OCR_Agent
```

2. **Create a virtual environment**

```bash
python3 -m venv env
source env/bin/activate   # Linux / macOS
# or
env\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Add your API keys to .env
```

---

### Running the Server

```bash
python main.py
```

The API will be available at:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 📡 API Endpoints

### 1. Extract Invoice (Full Pipeline)

**Endpoint**
`POST /extract-invoice`

Processes a PDF invoice using the complete **Gemini → GPT** pipeline.

**Request**

```bash
curl -X POST "http://localhost:8000/extract-invoice" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@invoice.pdf"
```

**Response**

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

---

### 2. Describe PDF (OCR Only)

**Endpoint**
`POST /describe-pdf`

Returns raw OCR output from Gemini without GPT post-processing.

**Request**

```bash
curl -X POST "http://localhost:8000/describe-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following values:

```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

### Model Configuration

* **Gemini Model**: `gemini-2.5-pro`
  *(configured in `parsing_service.py`)*

* **OpenAI Model**: `gpt-4o`
  *(configured in `extracting_service.py`)*
  → Automatically switches to **GPT-5** when available.

---

## 🗂 Project Structure

```
OCR_Agent/
├── main.py                  # FastAPI entry point
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── .env.example             # Environment template
└── src/
    ├── api/
    │   └── routes.py        # API routes
    ├── services/
    │   ├── parsing_service.py     # Gemini OCR logic
    │   ├── extracting_service.py  # GPT extraction logic
    │   └── pipeline.py            # End-to-end pipeline
    ├── models/
    │   └── schema.py        # Pydantic schemas
    └── helpers/
        └── config.py        # Configuration management
```

---

## 🛠 Development Guide

### Extending the System

* **Add new fields** → Update `src/models/schema.py`
* **Adjust extraction logic** → Modify prompts in `extracting_service.py`
* **Create new endpoints** → Add routes in `src/api/routes.py`

---

## 🧪 Testing & Documentation

Interactive API documentation is available at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

If you want, I can also:

* Make this README **more marketing-focused**
* Add **badges**, **benchmarks**, or **architecture diagrams**
* Rewrite it for **enterprise / SaaS positioning**
