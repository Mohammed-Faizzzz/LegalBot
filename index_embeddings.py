import faiss
import numpy as np


embeddings = np.load('embeddings.npy')
d = embeddings.shape[1]  # Dimensions
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexFlatL2(quantizer, d, nlist = 100)  # Use L2 distance
index.train(embeddings)
index.add(embeddings)

# Save
faiss.write_index(index, 'legal_cases.index')

