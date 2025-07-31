import json
import warnings

import faiss
import numpy as np
from embedder import embed_text
warnings.filterwarnings("ignore", category=FutureWarning)

TRANSFORMED_PATH = "../output/transformed_data.json"
INDEX_PATH = "../output/vector.index"
METADATA_PATH = "../output/vector_metadata.json"

def load_transformed_data(path=TRANSFORMED_PATH, limit=None):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data[:limit] if limit else data

def build_text_representation(item):
    parts = [
        f"Project: {item.get('project')}",
        f"File: {item.get('file')}",
        f"Sheet: {item.get('sheet')}",
        f"Description: {item.get('description')}",
        f"Quantity: {item.get('quantity')}",
        f"Unit: {item.get('unit')}",
        f"Unit Price: {item.get('unit_price')}",
        f"Currency: {item.get('currency')}"
    ]
    return " | ".join(str(p) for p in parts if p)

def index_data():
    data = load_transformed_data(limit=1000)  # ajuste o limite se quiser performance
    texts = [build_text_representation(item) for item in data]
    embeddings = [embed_text(text) for text in texts]

    # Salva vetor FAISS
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, INDEX_PATH)

    # Salva o contexto (metadata) correspondente aos vetores
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Indexed {len(data)} items to {INDEX_PATH} and metadata to {METADATA_PATH}")

if __name__ == "__main__":
    index_data()
