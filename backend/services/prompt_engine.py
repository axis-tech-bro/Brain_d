import requests
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

def is_ollama_running():
    try:
        requests.get("http://localhost:11434/", timeout=1)
        return True
    except:
        return False

def generate_report_text(data: dict) -> str:
    """
    Uses LangChain and local Llama 3 via Ollama to synthesize the market report based
    on the user's style query.
    """
    style_req = data.get('style_instructions', 'None')
    style_note = ""
    if style_req and style_req.lower() != "none":
        style_note = f"\nCRITICAL STYLE INSTRUCTION: {style_req}\n"

    try:
        if not is_ollama_running():
            raise Exception("Ollama server is not reachable on localhost:11434")

        llm = ChatOllama(model="llama3", temperature=0.7)
        prompt = PromptTemplate.from_template(
            "You are an expert financial analyst drafting a final Equity Market Report for the organization.\n"
            "You MUST perfectly mimic the exact structure, headers, and bullet points of the Historical Example below, but replace the data with the new Context Data.\n\n"
            "--- HISTORICAL EXAMPLE ---\n"
            "Context: Q1 2024 | MSCI ACWI: 8.1% | S&P 500: 10.2% | Drivers: resilient economic growth, robust AI-driven tech earnings\n\n"
            "Report:\n"
            "# Equity Market Report: Q1 2024\n\n"
            "## Executive Summary\n"
            "During the first quarter of 2024, global equities delivered strong performance, underscored by resilient economic growth and robust AI-driven tech earnings. In this environment, the MSCI ACWI returned 8.1%, while the S&P 500 led developed markets, achieving a 10.2% return.\n\n"
            "## Market Drivers\n"
            "The primary catalysts for the quarter's bullish momentum included:\n"
            "* **Macroeconomic Resilience**: Resilient economic growth surprised to the upside.\n"
            "* **Sector Dominance**: Robust AI-driven tech earnings propelled major indices.\n"
            "--- END HISTORICAL EXAMPLE ---\n\n"
            "Now it is your turn. Write the new report.\n"
            "Context Data:\n"
            "- Quarter: {quarter} {year}\n"
            "- MSCI ACWI Return: {msci_acwi_return}\n"
            "- S&P 500 Return: {sp500_return}\n"
            "- Macro Drivers: {drivers}\n"
            "{style}\n\n"
            "New Report Draft (Strictly Output Markdown Only):"
        )
        chain = prompt | llm
        response = chain.invoke({
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
