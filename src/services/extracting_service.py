import json
from typing import Any

from openai import AsyncOpenAI

from src.helpers.config import get_settings


SYSTEM_PROMPT = """You are an expert AI data extraction agent specialized in parsing invoices.
Your task is to take the raw OCR JSON output from Gemini for a SINGLE invoice page
and produce a clean, validated JSON that follows the given schema exactly.

Important:
- Focus heavily on Arabic and English bilingual text.
- Match fields like invoice_id, supplier name, customer name, dates, totals, and items accurately.
- Extract numbers even if written in Arabic numerals (e.g., ١٢٣ → 123).
- Use semantic understanding to infer missing fields.
- If a field is missing, return it as null.
- Never include explanations, only output valid JSON that strictly follows the schema below.

Required output schema:
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
}"""

USER_PROMPT_TEMPLATE = """Below is the Gemini OCR JSON output for a SINGLE invoice page.
Please parse it according to the schema above and output ONLY the final JSON.

Gemini OCR result for this page:

{page_content}"""


def _get_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def _clean_json_string(json_str: str) -> str:
    json_str = json_str.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    elif json_str.startswith("```"):
        json_str = json_str[3:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    return json_str.strip()


async def extract_invoice_data_from_page(page_data: dict[str, Any]) -> dict[str, Any]:
    client = _get_client()
    user_prompt = USER_PROMPT_TEMPLATE.format(
        page_content=json.dumps(page_data, ensure_ascii=False, indent=2)
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse GPT response as JSON: {e}")
    except Exception as e:
        raise Exception(f"Error extracting invoice data with GPT: {e}")


async def extract_invoice_data(gemini_ocr_json: str) -> list[dict[str, Any]]:
    try:
        json_str = _clean_json_string(gemini_ocr_json)
        ocr_data = json.loads(json_str)

        if "pages" not in ocr_data:
            raise Exception(
                f"Invalid Gemini OCR format: missing 'pages' array. Keys found: {list(ocr_data.keys())}"
            )

        pages = ocr_data["pages"]
        invoices = []
        
        for page_data in pages:
            invoice = await extract_invoice_data_from_page(page_data)
            invoices.append(invoice)

        return invoices
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Gemini OCR JSON: {e}")
    except Exception as e:
        raise Exception(f"Error extracting invoice data: {e}")



