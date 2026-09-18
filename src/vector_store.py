import chromadb

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore


def create_vector_store(nodes, embed_model):

    print("Creating ChromaDB vector store...")

    # Connect to persistent ChromaDB
    chroma_client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    # Start with a fresh collection each time
    # This prevents duplicate resumes during testing
    try:
        chroma_client.delete_collection("candidate_resumes")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        "candidate_resumes"
    )

    # Connect ChromaDB to LlamaIndex
    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    # Create storage context
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    # Create vector index
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model
    )

    print("Vector store created successfully.")

    return index