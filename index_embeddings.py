import faiss
import numpy as np


def index_embeddings():
    """
    Indexes the embeddings using Faiss library.

    This function loads the embeddings from 'embeddings.npy' file,
    creates an index using Faiss library, trains the index with the embeddings,
    and saves the index to 'legal_cases.index' file.

    Returns:
        None
    """
    embeddings = np.load('embeddings.npy')
    d = embeddings.shape[1]  # Dimensions
    quantizer = faiss.IndexFlatL2(d)
    index = faiss.IndexIVFFlat(quantizer, d, 100, faiss.METRIC_L2)
    index.train(embeddings)
    index.add(embeddings)

    # Save
    faiss.write_index(index, 'legal_cases.index')
