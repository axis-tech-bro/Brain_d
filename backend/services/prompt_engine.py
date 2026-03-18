import requests
import json
import random
import os
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

# Load RAG Data
RAG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "historical_reports.json")
try:
    with open(RAG_FILE_PATH, "r") as f:
        HISTORICAL_REPORTS = json.load(f)
except FileNotFoundError:
    HISTORICAL_REPORTS = []

def is_ollama_running():
    try:
        requests.get("http://localhost:11434/", timeout=1)
        return True
    except:
        return False

def generate_report_text(data: dict) -> str:
    """
    Uses LangChain and local Llama 3 via Ollama to synthesize the market report based
    on the user's style query, augmented with historical RAG examples.
    """
    style_req = data.get('style_instructions', 'None')
    style_note = ""
    if style_req and style_req.lower() != "none":
        style_note = f"\nCRITICAL STYLE INSTRUCTION: {style_req}\n"

    try:
        if not is_ollama_running():
            raise Exception("Ollama server is not reachable on localhost:11434")

        # RAG Step: Pick 3 historical reports to provide stylistic context
        rag_context = ""
        if HISTORICAL_REPORTS:
            samples = random.sample(HISTORICAL_REPORTS, min(3, len(HISTORICAL_REPORTS)))
            for idx, ex in enumerate(samples):
                rag_context += f"--- Example ({ex['quarter']} {ex['year']}) ---\n{ex['text']}\n\n"

        llm = ChatOllama(model="llama3.2:3b", temperature=0.2)
        prompt = PromptTemplate.from_template(
            "You are an expert financial analyst drafting an Equity Market Report.\n"
            "Your output must follow the EXACT length, structure, and tone of the Historical Examples below.\n\n"
            "=== HISTORICAL EXAMPLES ===\n"
            "{rag_context}"
            "=== END HISTORICAL EXAMPLES ===\n\n"
            "INSTRUCTIONS:\n"
            "1. Write EXACTLY two or three paragraphs, mirroring the flow of the examples.\n"
            "2. Paragraph 1 MUST discuss the Macro Drivers and state the MSCI ACWI return.\n"
            "3. Paragraph 2 MUST discuss the S&P 500 return.\n"
            "4. Do NOT use markdown headers, bolding, or bullet points unless the Custom Style explicitly asks for them.\n"
            "5. Seamlessly integrate the following new data into the text:\n\n"
            "Context Data:\n"
            "- Quarter: {quarter} {year}\n"
            "- MSCI ACWI Return: {msci_acwi_return}\n"
            "- S&P 500 Return: {sp500_return}\n"
            "- Macro Drivers: {drivers}\n"
            "{style}\n\n"
            "Final Report Text:"
        )
        chain = prompt | llm
        response = chain.invoke({
            "rag_context": rag_context,
            "quarter": data.get('quarter', 'Unknown'),
            "year": data.get('year', 'Unknown'),
            "msci_acwi_return": data.get('msci_acwi_return', 'N/A'),
            "sp500_return": data.get('sp500_return', 'N/A'),
            "drivers": ", ".join(data.get('macro_drivers', [])),
            "style": style_note
        })
        return response.content
    except Exception as e:
        print("Falling back to mocked response:", e)
        # Mock generation if Ollama fails
        fallback_style = ""
        if style_req and style_req.lower() != "none":
             fallback_style = f"\n\n*(Style applied: {style_req})*"
             
        return f"# Equity Market Report: {data.get('quarter')} {data.get('year')}\n\n" \
               f"During the quarter, the MSCI ACWI returned {data.get('msci_acwi_return')}, " \
               f"while the S&P 500 achieved {data.get('sp500_return')}. The market was driven by: " \
               f"{', '.join(data.get('macro_drivers', []))}." + fallback_style
