#fastapi entry point
from fastapi import FastAPI
from qa_rag_agent.api.routes import router as api_router

app = FastAPI(title="QA RAG Agent API")
app.include_router(api_router)