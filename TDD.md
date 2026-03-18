# Technical Design Document: Automated Equity Market Report Generation

## Background
The organization requires the recurring generation of Quarterly Equity Market Reports. Historically, these reports (spanning Q1 2024 to Q2 2025) follow a specific narrative structure. The workflow is currently manual and needs to be automated to accelerate future report generation while strictly maintaining the established style, clarity, and structure.

## Problem Statement
Build an automated engine capable of ingesting a natural language prompt (e.g., “Generate the Equity market report for Q4 2025”) and outputting a highly accurate, stylized quarterly market report. The success metric is zero quantitative hallucinations (accurate financial data) paired with a 95%+ stylistic alignment with previous reports.

## Business Logic
The core value proposition is executed across three user phases:
1. **Instruction Phase**: The user submits a temporal query specifying the target quarter and year.
2. **Data Aggregation Phase**: The system programmatically fetches quantitative metrics (e.g., MSCI ACWI and S&P 500 performance) and qualitative drivers (e.g., macroeconomic events) for the specified period.
3. **Synthesis Phase**: The engine merges the aggregated data with the established stylistic template to generate the final narrative.

## Algorithm
1. Receive and parse the natural language user instruction to extract Target_Quarter and Target_Year.
2. Query the internal financial database or external market API for core metrics specific to the target timeframe: MSCI ACWI return, S&P 500 total return, YTD gains, and record highs.
3. Query a macroeconomic news index for the top 3 market drivers during the target timeframe (e.g., inflation, central bank policy, geopolitical events).
4. Construct a strict JSON payload combining the retrieved quantitative data and qualitative drivers.
5. Retrieve 3 historical report examples from a local JSON database and inject them alongside the payload into an LLM using a strict Retrieval-Augmented Generation (RAG) framework.
6. Execute the LLM generation step with a highly deterministic temperature setting (0.2) and explicit formatting guards (e.g., prohibiting unauthorized markdown headers) to enforce exact structural adherence to the historical examples.
7. Output the generated text to the user interface for final human-in-the-loop validation.

## Data Model (Exchange Format)
The core contract between the Natural Language Parser, the Market API, and the Prompt Engine operates on a strict JSON payload:
```json
{
  "quarter": "Q4",
  "year": "2025",
  "style_instructions": "Make it sound optimistic",
  "msci_acwi_return": "10.6%",
  "sp500_return": "12.4%",
  "macro_drivers": [
    "Easing inflation",
    "Strong corporate tech earnings",
    "Stable geopolitical environment"
  ]
}
```
This data model ensures that the LLM is completely isolated from *retrieving* facts, and is solely responsible for *styling* the provided JSON properties into the final Markdown strings.

## Business Constraints
- **Time**: The system prototype must be architected and implemented within a strict project window.
- **Accuracy**: Zero tolerance for hallucinated financial figures.
- **Formatting**: Must seamlessly match the provided legacy examples in tone and structure.

## Technical Constraints
- **Dependency**: Relies on the availability and latency of third-party APIs for real-time or historical financial data.
- **Context Window**: The LLM must support a context window large enough to hold at least 4 historical quarters of text for few-shot prompting.

## Assumptions
- A reliable financial data API (e.g., Bloomberg, Alpha Vantage, or internal SQL warehouse) is accessible.
- The user prompt will adhere to a predictable temporal format (Quarter + Year).
- The established reporting format (focusing heavily on MSCI ACWI and S&P 500) remains constant.

## Scope
### In Scope
- Prompt engineering using Few-Shot techniques with dynamically retrieved historical reports, alongside custom style modifiers.
- Local Retrieval-Augmented Generation (RAG) architecture using high-speed open-source models (Llama 3.2 3B via Ollama).
- A basic API or CLI interface to accept user commands.

### Out of Scope
- Dynamic chart or graph generation.
- Automated publishing directly to a Content Management System (CMS) without human review.
- Fine-tuning a proprietary foundational LLM (unfeasible within the project window).

## Business Implementation
The recommended product approach is a **Data-First Few-Shot Generation System**. We must separate the retrieval of facts from the generation of text. LLMs are excellent at mimicking style but poor at calculating or retrieving exact historical market data. By fetching the hard numbers (e.g., 10.6% total return, 21 record highs) deterministically via code and forcing the LLM to write the narrative around those injected variables, we eliminate the primary risk of AI hallucination. This ensures that the qualitative storytelling aligns with the data rather than inventing it.

### Q&A
- **How does the system handle nuance?** Nuance is handled by the data pipeline fetching macroeconomic drivers (e.g., "Trump tariff program"). The LLM is instructed to synthesize these specific variables into the introductory paragraph, mirroring the historical structure.
- **How do we evaluate/improve the output over time?** We implement a feedback loop where the human reviewer flags stylistic deviations. These corrected reports are then appended to the vector database to be used as future few-shot examples, allowing the system's style library to evolve organically.

### Alternative Approaches Evaluated
- **Concept**: LLM Fine-Tuning.
- **Verdict**: Rejected. Fine-tuning models on the provided reports would capture the style perfectly but would hardcode outdated financial data into the model weights, increasing hallucination risks. It also violates the build constraint.

## Technical Implementation

### Technical Algorithm
1. Frontend receives string: “Generate the Equity market report for Q4 2025”.
2. Backend Regex/NLP extracts `{quarter: "Q4", year: 2025}`.
3. Data Pipeline triggers API calls to fetch MSCI_ACWI_Return, SP500_Return, and Macro_Drivers for Q4 2025.
4. Backend compiles a system prompt containing strict formatting rules, 3 historical examples retrieved dynamically from the RAG dataset, and the retrieved data variables.
5. ML service processes the prompt and streams the generated markdown response.
6. Frontend renders the response for human review.

### Frontend
- **Recommended Approach**: React.js
  - **Pros**: 1. Component-based architecture allows rapid UI building, 2. Extensive ecosystem for state management, 3. Ideal for handling streamed text responses from LLMs.
  - **Cons**: 1. Boilerplate setup.
- **Alternative 1**: Streamlit (Python)
  - **Pros**: 1. Extremely fast to deploy within a short window, 2. Native integration with Python data/ML stacks.
  - **Cons**: 1. Limited custom UI styling, 2. Less scalable for a full production SaaS platform.
- **Alternative 2**: Vanilla HTML/JS
  - **Pros**: 1. Zero dependencies, 2. Maximum control over the DOM.
  - **Cons**: 1. Slower development speed, 2. Difficult to manage complex state transitions.

### Backend
- **Recommended Approach**: Python (FastAPI)
  - **Pros**: 1. Native asynchronous support for fast API routing, 2. Seamless integration with LLM libraries, 3. Self-documenting via Swagger.
  - **Cons**: 1. Python lacks the strict type safety of compiled languages, 2. Slower execution speed for highly CPU-bound tasks.
- **Alternative 1**: Node.js (Express)
  - **Pros**: 1. Unifies the stack if using React on the frontend, 2. Excellent asynchronous I/O handling.
  - **Cons**: 1. Weaker ecosystem for complex data science and ML integrations, 2. Callback/Promise overhead can become messy.
- **Alternative 2**: Go (Gin)
  - **Pros**: 1. Extremely high performance and low latency, 2. Strongly typed and memory safe.
  - **Cons**: 1. Steep learning curve, 2. Overkill for an API primarily acting as a proxy to an LLM.

### Data Pipeline (Mocked in Demo)
- **Recommended Approach**: Python Pandas + Financial APIs (e.g., Alpha Vantage)
  - **Pros**: 1. Pandas is the industry standard for financial time-series manipulation, 2. Rapid calculation of YTD and quarterly metrics, 3. Easy integration into the FastAPI backend.
  - **Cons**: 1. API rate limits can throttle generation, 2. High memory consumption for massive datasets.
- **Alternative 1**: Direct SQL Queries (Internal DB)
  - **Pros**: 1. Eliminates third-party API dependency, 2. Highly secure and deterministic.
  - **Cons**: 1. Requires existing structured data infrastructure, 2. Slower to prototype if the database schema is complex.
- **Alternative 2**: GraphQL API
  - **Pros**: 1. Fetches only the exact data needed without over-fetching, 2. Strongly typed data contracts.
  - **Cons**: 1. Requires a pre-existing GraphQL server, 2. Adds complexity to the query logic.

### Machine Learning
- **Implemented Approach**: Local Open-Source LLM (Llama 3.2 3B via Ollama) + LangChain
  - **Pros**: 1. Zero recurring API costs. 2. Absolute data privacy (financial metrics never leave the local machine). 3. Extremely high generation speeds yielding near-instant real-time text streams.
  - **Cons**: 1. Highly deterministic prompts with rigid formatting rules (e.g., "no headers") are required because smaller 3B models struggle with complex implicit instructions. 2. Bound by the host machine's RAM capability.
  - **Production Problems & Mitigation**: In a production environment handling dozens of concurrent analyst requests, a single local Llama 3.2 instance will bottleneck. To solve this, production deployments must horizontally scale via a cluster of dedicated GPU instances (e.g., AWS EC2 instances) fronted by a load balancer, or migrate to a serverless open-source provider like Groq or Together AI.
- **Alternative 1**: Proprietary Managed APIs (OpenAI GPT-4o / Anthropic Claude 3.5 Sonnet)
  - **Deep Dive**: Migrating from an open-source local model to GPT-4o or Claude is the standard enterprise play for alleviating local hardware constraints. Claude 3.5 Sonnet specifically excels at nuanced financial writing and maintaining a rigid, professional tone over an infinitely large context window.
  - **Production Problems & Mitigation**: 1. **Data Leakage Risk**: Sending sensitive internal financial metrics to external third-party endpoints. Solved by using "Zero Data Retention" enterprise agreements or Azure OpenAI. 2. **Prompt Injection**: Analysts could accidentally or maliciously inject instructions to alter the report's facts. Solved by decoupling the metric injection from the stylistic LLM prompt (as designed in our MVP Data Model).

### Infrastructure (Not in Demo)
- **Recommended Approach**: AWS Lambda / API Gateway
  - **Pros**: 1. True serverless architecture scales to zero, 2. Pay only for compute time used during report generation, 3. Fast deployment for PoCs.
  - **Cons**: 1. Cold start latency, 2. Hard 15-minute execution limit.
- **Alternative 1**: Docker + AWS ECS
  - **Pros**: 1. Complete control over the runtime environment, 2. No execution time limits.
  - **Cons**: 1. Requires managing container orchestration, 2. Higher baseline costs.
- **Alternative 2**: Vercel (Serverless Functions)
  - **Pros**: 1. One-click deployment for frontend and backend, 2. Exceptional developer experience.
  - **Cons**: 1. Strict payload size and timeout limits, 2. Tied to the Vercel ecosystem.

### Deployment Plan & Infrastructure
For the prototype MVP, the frontend is a React application communicating via REST to a FastAPI backend entirely on `localhost`. Financial data is mocked using a static JSON dictionary. Llama 3.2 3B handles text synthesis via a local Ollama server drawing dynamic styling from a RAG JSON database.

**Why production infrastructure (AWS/Serverless) was not deployed for the Demo MVP**:
Given the short implementation window, the core engineering focus was dedicated entirely to solving the complex behavioral application logic: successfully decoupling hard metrics from LLM generation to eliminate hallucinations, and enforcing legacy report structures via Few-Shot Prompting. Deploying VPCs, API Gateways, or Vercel containers would have consumed the time block with devops configuration overhead rather than proving the viability of the AI RAG engine. The application is, however, completely Docker-ready and gracefully handles missing connections (failing back to mocked strings if Ollama is unavailable), ensuring rapid transition to cloud infrastructure in phase 2.

