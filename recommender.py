from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

# ✅ Use a smaller model that loads faster
model = SentenceTransformer('./all-MiniLM-L6-v2')


# Load FAISS index
index = faiss.read_index("shl_index.faiss")

# Load metadata
with open("shl_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def recommend_assessments(query: str, top_k=10):
    query_vector = model.encode([query])[0]
    D, I = index.search(np.array([query_vector]), top_k)
    results = [metadata[i] for i in I[0]]
    return results
