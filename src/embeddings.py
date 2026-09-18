from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def get_embedding_model():
    """
    Load the embedding model used to convert resume
    chunks into numerical vectors.
    """

    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embed_model