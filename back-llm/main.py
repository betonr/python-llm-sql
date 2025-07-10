import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import bootstrap_db
from llm_engine import build_query_engine

# from dotenv import load_dotenv
# load_dotenv() # lê OPENAI_API_KEY do .env

app = FastAPI()

# CORS para permitir acesso do front-end local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # bootstrap_db()
    app.state.query_engine = build_query_engine()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(request: QueryRequest):
    try:
        response = app.state.query_engine.query(request.question)
        return {"answer": str(response)}
    except Exception as e:
        return {"answer": f"Erro ao processar a pergunta: {str(e)}"}

@app.get("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)