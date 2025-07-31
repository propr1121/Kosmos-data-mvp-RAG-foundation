import os
import json
import faiss
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from etl.mistral_client import ask_mistral
from rag.embedder import embed_text

os.environ["TOKENIZERS_PARALLELISM"] = "false"
INDEX_PATH = "output/vector.index"
METADATA_PATH = "output/vector_metadata.json"

app = FastAPI()

print("🔄 Loading FAISS index and metadata...")
index = faiss.read_index(INDEX_PATH)
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)
print("✅ Index and metadata ready.")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    q_emb = embed_text(query.question)
    q_emb = np.array([q_emb]).astype("float32")

    distances, indices = index.search(q_emb, k=3)
    context_snippets = []
    for i in indices[0]:
        if i < len(metadata):
            context_snippets.append(metadata[i])

    context_text = "\n".join(
        f"- Project: {c['project']}, File: {c['file']}, Sheet: {c['sheet']}, Desc: {c['description'] or 'N/A'}"
        for c in context_snippets
    )

    prompt = (
        "You are a helpful assistant for analyzing messy construction project data.\n"
        "Use the context below to answer the user's question clearly and accurately.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {query.question}\n"
        "Answer:"
    )

    print("\n📤 Prompt sent to Mistral:\n", prompt[:1000])
    answer = ask_mistral(prompt)

    return {
        "answer": answer,
        "context_snippets": context_snippets
    }

# run: uvicorn rag.rag_api:app --reload
