import re
import json
import requests
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

def is_ollama_running():
    try:
        # Fast 1-second timeout ping
        requests.get("http://localhost:11434/", timeout=1)
        return True
    except:
        return False

def parse_temporal_query(query: str) -> dict:
    """
    Parses a natural language query for a quarter, year, and dynamic style parameters
    using a local Llama 3 model via Ollama. 
    Fallbacks to Regex if Ollama is not running.
    """
    try:
        if not is_ollama_running():
            raise Exception("Ollama server is not reachable on localhost:11434")
            
        llm = ChatOllama(model="llama3.2:3b", temperature=0, format="json")
        prompt = PromptTemplate.from_template(
            "Extract the target market quarter, year, and any style instructions from the following prompt.\n"
            "Style instructions are things like 'funny', 'bullet points', 'Shakespearean', etc.\n"
            "Return ONLY a JSON object with keys: 'quarter', 'year', 'style_instructions'.\n"
            "Prompt: {query}"
        )
        chain = prompt | llm
        response = chain.invoke({"query": query})
        data = json.loads(response.content)
        
        return {
            "quarter": data.get("quarter", "Unknown").upper(),
            "year": str(data.get("year", "Unknown")),
            "style_instructions": data.get("style_instructions", "None")
        }
    except Exception as e:
        # Fallback to simple regex if Ollama isn't running
        print("Falling back to regex extraction:", e)
        quarter_match = re.search(r'(Q[1-4])', query, re.IGNORECASE)
        year_match = re.search(r'(20\d{2})', query)
        
        quarter = quarter_match.group(1).upper() if quarter_match else "Unknown"
        year = year_match.group(1) if year_match else "Unknown"
        
        return {
            "quarter": quarter,
            "year": year,
            "style_instructions": "None"
        }
