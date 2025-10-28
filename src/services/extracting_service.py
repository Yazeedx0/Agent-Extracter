from openai import AsyncOpenAI
from src.helpers.config import settings
import json
from typing import Dict, Any, List


# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def extract_invoice_data_from_page(page_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured invoice data from a SINGLE page of Gemini OCR output using GPT-5 (GPT-4).
    
    Args:
        page_data: The OCR data for a single page (one element from the "pages" array)
    
    Returns:
        Structured invoice data following the schema
    """
    
    system_prompt = """You are an expert AI data extraction agent specialized in parsing invoices.
  Your task is to take the raw OCR JSON output from Gemini for a SINGLE invoice page
  and produce a clean, validated JSON that follows the given schema exactly.

  ⚠️ Important:
  - Focus heavily on Arabic and English bilingual text.
  - Match fields like invoice_id, supplier name, customer name, dates, totals, and items accurately.
  - Extract numbers even if written in Arabic numerals (e.g., ١٢٣ → 123).
  - Use semantic understanding to infer missing fields (e.g., if "ZEIDAN TRADING AGENCY" appears near "فاتورة", treat it as supplier name).
  - If a field is missing, return it as `null`.
  - Never include explanations, only output valid JSON that strictly follows the schema below.

  Required output schema:
  ```json
  {
    "invoice_id": "",
    "invoice_date": "",
    "supplier": {
      "name": "",
      "address": "",
      "vat_number": ""
    },
    "customer": {
      "name": "",
      "address": "",
      "vat_number": ""
    },
    "items": [
      {
        "description": "",
        "quantity": 0,
        "unit_price": 0,
        "unit": "",
        "total": 0
      }
    ],
    "subtotal": 0,
    "tax": 0,
    "total_amount": 0,
    "currency": "JOD",
    "payment_method": "",
    "invoice_notes": ""
  }
  ```"""
    
    user_prompt = f"""Below is the Gemini OCR JSON output for a SINGLE invoice page.
Please parse it according to the schema above and output ONLY the final JSON.

Gemini OCR result for this page:

```json
{json.dumps(page_data, ensure_ascii=False, indent=2)}
```"""
    
    try:
        # Call GPT-4 (or GPT-5 when available)
        response = await client.chat.completions.create(
            model="gpt-5-mini",  # Use "gpt-5" when available, currently using gpt-4o (latest)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}  # Ensures valid JSON output
        )
        
        # Extract the response
        result_text = response.choices[0].message.content
        
        # Parse JSON to validate
        invoice_data = json.loads(result_text)
        
        return invoice_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse GPT response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting invoice data with GPT: {str(e)}")


async def extract_invoice_data(gemini_ocr_json: str) -> List[Dict[str, Any]]:
    """
    Extract structured invoice data from Gemini OCR output using GPT-5 (GPT-4).
    Processes each page separately to avoid confusion.
    
    Args:
        gemini_ocr_json: The raw OCR JSON output from Gemini containing multiple pages
    
    Returns:
        List of structured invoice data, one per page
    """
    try:
        # Clean the JSON string if it contains markdown code blocks
        json_str = gemini_ocr_json.strip()
        
        # Remove markdown code blocks if present
        if json_str.startswith("```json"):
            json_str = json_str[7:]  # Remove ```json
        elif json_str.startswith("```"):
            json_str = json_str[3:]  # Remove ```
            
        if json_str.endswith("```"):
            json_str = json_str[:-3]  # Remove trailing ```
            
        json_str = json_str.strip()
        
        # Parse the Gemini OCR JSON
        ocr_data = json.loads(json_str)
        
        # Debug: Print the structure we received
        print(f"🔍 Gemini OCR data keys: {list(ocr_data.keys())}")
        print(f"🔍 First 300 chars of parsed data: {str(ocr_data)[:300]}")
        
        # Check if we have pages array
        if "pages" not in ocr_data:
            # Try to handle if Gemini returned the data in a different format
            # Maybe it's already a single page or the structure is different
            print("⚠️  Warning: 'pages' array not found. Attempting alternative parsing...")
            print(f"📋 Available keys: {list(ocr_data.keys())}")
            raise Exception(f"Invalid Gemini OCR format: missing 'pages' array. Keys found: {list(ocr_data.keys())}")
        
        pages = ocr_data["pages"]
        print(f"📑 Found {len(pages)} page(s) to process")
        
        # Process each page separately
        invoices = []
        for i, page_data in enumerate(pages, 1):
            print(f"  ➡️  Processing page {i}/{len(pages)}...")
            invoice = await extract_invoice_data_from_page(page_data)
            invoices.append(invoice)
            print(f"  ✅ Page {i} complete!")
        
        return invoices
        
    except json.JSONDecodeError as e:
        # Print the actual content for debugging
        print(f"❌ Failed to parse JSON. First 500 chars of response:")
        print(gemini_ocr_json[:500])
        raise Exception(f"Failed to parse Gemini OCR JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting invoice data: {str(e)}")


async def process_invoice(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Complete pipeline: OCR with Gemini -> Extract with GPT-5
    
    Args:
        pdf_path: Path to the PDF invoice file
    
    Returns:
        List of structured invoice data (one per page)
    """
    from src.services.parsing_service import describe_pdf
    
    try:
        # Step 1: Get OCR output from Gemini
        print("📄 Processing PDF with Gemini OCR...")
        gemini_output = await describe_pdf(pdf_path)
        
        # Step 2: Extract structured data with GPT-5 (processes each page separately)
        print("🤖 Extracting structured data with GPT...")
        invoices_list = await extract_invoice_data(gemini_output)
        
        print(f"✅ Invoice extraction complete! Extracted {len(invoices_list)} invoice(s)")
        return invoices_list
        
    except Exception as e:
        raise Exception(f"Error in invoice processing pipeline: {str(e)}")
