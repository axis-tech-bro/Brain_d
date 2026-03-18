# Automated Equity Market Report Generation

## Overview
This project is an automated engine capable of generating quarterly equity market reports. It takes a natural language prompt (e.g., “Generate the Equity market report for Q4 2025”) and outputs a highly accurate, stylized market report. The system ensures zero quantitative hallucinations by injecting verified financial data and achieves stylistic alignment using a Few-Shot Prompting framework along with historical reports.

## Features
- **Temporal Query Parsing**: Extracts the target quarter and year from natural language user input.
- **Automated Data Aggregation**: Fetches market metrics (e.g., MSCI ACWI, S&P 500 performance) and macroeconomic drivers deterministically.
- **Fact-Preserving Synthesis**: Combines accurate fetched data with strict stylistic constraints using an LLM.
- **Human-in-the-loop**: Presents the drafted text for final validation and structural adjustments, ensuring high-quality output.

## Architecture
- **Frontend**: React (Next.js/Vite) for a fast, component-based user interface.
- **Backend/Logic**: Python FastAPI handling NLP extraction, data fetching, and prompt orchestration.
- **Data Pipeline**: Python + Financial Data API integration (or mocked JSON data for the initial MVP/prototype).
- **Machine Learning**: Local Open-Source LLMs (e.g., Llama 3 via Ollama) + LangChain for structure extraction and text synthesis.
- **Infrastructure**: Currently runs entirely locally for the MVP prototype (`localhost:8000` / `localhost:5173`).

## Deviations from Original Scope
During the 6-hour MVP sprint, several architectural pivots were made:
1. **Monolith to Decoupled**: The interface was originally scoped as a `Streamlit` app but was transitioned to a `React + FastAPI` stack for superior control over the UI components (Tailwind CSS) and the asynchronous API endpoint behavior.
2. **Proprietary API to Local OS**: The AI provider was pivoted from `OpenAI / GPT-4o` to `Llama 3` running locally via Ollama. This was executed to support dynamic user styling parameters without incurring API costs or requiring the user to provision keys during the demo. 
3. **No Cloud Deployment**: DevOps and CI/CD infrastructure (AWS/Vercel) were intentionally excluded from this 6-hour demo window in order to monopolize engineering completely around the core AI generation stability—specifically preventing financial data hallucinations using the Data-First injection block.

## Quick Start
*Details on how to clone, install dependencies, and run the project will be added as the implementation progresses.*

## Documentation
- [Technical Design Document (TDD)](TDD.md): Full technical specifications, evaluating alternatives, and algorithmic logic.

## Contribution & Evaluation
Future iterations of this tool will implement a feedback loop. Any reports flagged for stylistic deviations by human reviewers will be added to the vector database to be used as future few-shot examples. This will allow the system's style library to evolve organically.
