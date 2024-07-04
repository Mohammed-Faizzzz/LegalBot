import numpy as np
import faiss

def index_embeddings():
    """
    Indexes the embeddings using Faiss library with FlatL2 index.

    This function loads the embeddings from 'embeddings.npy' file,
    creates a FlatL2 index using Faiss library, adds the embeddings to the index,
    and saves the index to 'legal_cases.index' file.

    Returns:
        None
    """
    embeddings = np.load('embeddings.npy')
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    # Save the index
    faiss.write_index(index, 'legal_cases.index')
    print(f"Indexed {index.ntotal} vectors of dimension {d}")

index_embeddings()