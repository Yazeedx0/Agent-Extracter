from google import genai
import base64
import os
from src.helpers.config import get_settings


settings = get_settings()
# Initialize Gemini client (using API key for Gemini Developer API)
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


async def describe_pdf(pdf_path: str, prompt: str = "Describe the content of this document in detail. Include any text, tables, charts, or images you see.") -> str:
    """
    Describe a PDF file using Gemini 2.5 Pro directly
    
    Args:
        pdf_path: Path to the PDF file
        prompt: Custom prompt for the description
    
    Returns:
        Description of the PDF content
    """
    try:
        # Read PDF file and convert to base64
        with open(pdf_path, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Generate content using Gemini with PDF
        prompt = """
You are an OCR extraction assistant. 
Read the following PDF document and extract ALL visible textual data, 
including Arabic and English text, numbers, tables, and labels. 

CRITICAL: Output ONLY valid JSON (no markdown, no explanations, no code blocks).
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
Return ONLY the JSON object, nothing else.
"""
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                        {"text": prompt}
                    ]
                }
            ],
            config={
                "response_mime_type": "application/json"  # Force JSON output
            }
        )
        
        # Debug: Print first 500 chars of response
        print(f"🔍 Gemini response (first 500 chars): {response.text[:500]}")
        
        return response.text
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


