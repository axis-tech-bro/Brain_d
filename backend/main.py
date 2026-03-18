from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from services.nlp_parser import parse_temporal_query
from data.market_api import fetch_market_data
from services.prompt_engine import generate_report_text

load_dotenv()

app = FastAPI(title="Automated Equity Market Report Generation API")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Equity Market Report API is running"}

@app.post("/api/generate")
async def generate_report(request: ReportRequest):
    # 1. Parse Query
    parsed_query = parse_temporal_query(request.query)
    
    # 2. Fetch Data
    market_data = fetch_market_data(parsed_query['quarter'], parsed_query['year'])
    
    # Merge for Context
    context = {**parsed_query, **market_data}
    
    # 3. Generate Report
    report = generate_report_text(context)
    
    return {
        "status": "success", 
        "query": request.query,
        "parsed_query": parsed_query,
        "market_data": market_data,
        "report": report
    }
