# rag/vector_store.py
import chromadb
from rag.embedder import embed_text

client = chromadb.Client()
collection = client.get_or_create_collection("kosmos_data")

def normalize_id(project, file, sheet):
    return f"{project}_{file}_{sheet}".replace(" ", "_").replace("/", "_")

def index_sheet(project, file, sheet, summary, columns):
    text = f"{project} {file} {sheet} {summary} {columns}"
    vector = embed_text(text)
    doc_id = normalize_id(project, file, sheet)

    try:
        collection.add(
            documents=[text],
            embeddings=[vector],
            ids=[doc_id]
        )
        print(f"✅ Indexed: {doc_id}")
    except chromadb.errors.IDAlreadyExistsError:
        print(f"⚠️ ID {doc_id} already exists. Skipping...")

def query_relevant_context(user_question, k=3):
    vector = embed_text(user_question)
    results = collection.query(query_embeddings=[vector], n_results=k)

    if not results["documents"]:
        return []

    return results["documents"][0]
