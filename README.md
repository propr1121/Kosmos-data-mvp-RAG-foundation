# 🏗️ Kosmos ETL + RAG AI Pipeline

**Process, understand, and query messy engineering spreadsheets using a fully local AI pipeline with Mistral + RAG.**

---

## 🚀 What It Does

* Extracts unstructured data from `.xlsx`, `.docx`, `.pdf`
* Transforms it into a standardized ICMS-like format
* Semantically classifies and summarizes sheets using Mistral (via Ollama)
* Indexes results into a FAISS vector store
* Enables natural-language querying via terminal or FastAPI

---

## 📂 Project Structure

```
kosmos-etl/
│
├── etl/
│   ├── extractor.py           # Reads messy Excel, Word, PDF
│   ├── transformer.py         # Maps to ICMS format
│   ├── analyzer.py            # Detects sheet types heuristically
│   ├── summary_generator.py   # AI summaries + column classification
│   ├── loader.py              # Saves outputs
│   └── mistral_client.py      # Runs local LLM (Mistral via Ollama)
│
├── rag/
│   ├── embedder.py            # SentenceTransformers embedding
│   ├── vector_store.py        # Handles ChromaDB or FAISS vector storage
│   ├── indexer.py             # Creates index from summaries
│   └── rag_api.py            # RAG-based API using FastAPI
│
├── chat/
│   └── chat_rag.py            # Terminal chatbot with RAG
│
├── data/                      # Input documents
├── output/                    # ETL & embedding outputs
└── main.py                    # Runs full ETL pipeline
```

---

## 💠 Setup

1. **Clone + Environment**

   ```bash
   git clone https://github.com/your-org/kosmos-etl.git
   cd kosmos-etl
   pyenv install 3.11.9
   pyenv virtualenv 3.11.9 kosmos-etl-env
   pyenv activate kosmos-etl-env
   pip install -r requirements.txt
   ```

2. **Install Ollama + Mistral**

   ```bash
   brew install ollama
   ollama pull mistral
   ```

---

## 🧲 Run the Pipeline

### 1. Extract, Transform, Analyze

```bash
python main.py
```

### 2. Generate Sheet Summaries (Mistral)

```bash
python etl/summary_generator.py
```

### 3. Index for RAG

```bash
python rag/indexer.py
```

---

## 💬 Ask Questions

### Terminal Chat

```bash
python chat/chat_rag.py
```

### API (FastAPI)

```bash
uvicorn rag.rag_api:app --reload
```

POST to `http://localhost:8000/ask` with:

```json
{ "question": "Which columns contain unit prices?" }
```

---

## 🧠 Model & Search Strategy

* **LLM**: Mistral 7B via [Ollama](https://ollama.ai)
* **Embedding**: `all-MiniLM-L6-v2` (SentenceTransformers)
* **Vector Search**: FAISS

---

## 📌 Notes

* RAG avoids hallucinations by feeding only the most relevant data slices to the model.
* All computation is local: zero cloud dependencies.
* Ideal for multilingual and messy engineering files.


---

## 🧐 Authors

Built by Jacaranda Labs for Kosmos.
