import faiss
import numpy as np


embeddings = np.load('embeddings.npy')
d = embeddings.shape[1]  # Dimensions
index = faiss.IndexFlatL2(d)  # Use L2 distance
index.add(embeddings)

# Save
faiss.write_index(index, 'legal_cases.index')

