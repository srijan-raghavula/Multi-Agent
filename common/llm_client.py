import os
import google.generativeai as genai

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    API_KEY = "Enter API KEY"
    genai.configure(api_key=API_KEY)

def query_llm(prompt: str, model_name: str = "models/gemini-2.5-flash", temperature: float = 0.2) -> str:
    """Single Gemini-powered LLM query interface."""
    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error querying Gemini: {e}]"
