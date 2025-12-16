import base64

from google import genai

from src.helpers.config import get_settings


OCR_EXTRACTION_PROMPT = """You are an OCR extraction assistant.
Read the following PDF document and extract ALL visible textual data,
including Arabic and English text, numbers, tables, and labels.

Output ONLY valid JSON (no markdown, no explanations, no code blocks).
Start directly with { and end with }.

Required structure:
{
  "pages": [
    {
      "page_number": 1,
      "text_blocks": ["text1", "text2"],
      "tables": [],
      "key_values": [{"key": "value"}]
    }
  ]
}

Do not summarize — extract every visible text element.
Return ONLY the JSON object, nothing else."""


def _get_gemini_client() -> genai.Client:
    settings = get_settings()
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _encode_pdf_to_base64(pdf_path: str) -> str:
    with open(pdf_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


async def describe_pdf(pdf_path: str) -> str:
    try:
        client = _get_gemini_client()
        pdf_b64 = _encode_pdf_to_base64(pdf_path)

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                        {"text": OCR_EXTRACTION_PROMPT}
                    ]
                }
            ],
            config={"response_mime_type": "application/json"}
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error processing PDF: {e}")

