# embed_assessments.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load your collected data
df = pd.read_csv("shl_data.csv")

# Load a pre-trained sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Combine title + description for semantic search
texts = (df["Assessment Name"] + " " + df["Description"]).tolist()
embeddings = model.encode(texts, convert_to_tensor=False)

# Create FAISS index
dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))

# Save the FAISS index to a file
faiss.write_index(index, "shl_index.faiss")

# Save the original data (metadata) for later use
with open("shl_metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient='records'), f)

print("✅ Embeddings generated and stored.")
