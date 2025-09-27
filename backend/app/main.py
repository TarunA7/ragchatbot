# main.py - FastAPI app with /ingest-file and /chat endpoints
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from rag import ingest_texts, get_conversational_chain

app = FastAPI(title="RAG Chatbot API")

class ChatRequest(BaseModel):
    question: str
    chat_history: List[List[str]] = []  # optional list of [user, assistant] pairs

@app.post("/ingest-file")
async def ingest_file(file: UploadFile = File(...)):
    # Accept plain text uploads
    data = await file.read()
    try:
        text = data.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Only plain text (.txt, .md) supported here.")
    res = ingest_texts([text], metadatas=[{"filename": file.filename}])
    return res

@app.post("/chat")
async def chat(req: ChatRequest):
    chain = get_conversational_chain()
    out = chain({"question": req.question, "chat_history": req.chat_history})
    answer = out.get("answer")
    sources = out.get("source_documents", [])
    # Limit the length of returned page content for safety
    sdocs = [{"page_content": d.page_content[:1000], "metadata": d.metadata} for d in sources]
    return {"answer": answer, "source_documents": sdocs}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
