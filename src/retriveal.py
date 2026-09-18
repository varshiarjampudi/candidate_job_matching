def create_retriever(index, similarity_top_k=10):
    """
    Create a retriever that returns relevant resume chunks.
    """

    retriever = index.as_retriever(
        similarity_top_k=similarity_top_k
    )

    return retriever


def retrieve_unique_candidates(retriever, query, max_candidates=5):
    """
    Retrieve resume chunks and remove duplicate candidates.
    """

    results = retriever.retrieve(query)

    candidates = {}

    for result in results:

        source = result.node.metadata.get(
            "file_name",
            "Unknown"
        )

        # Prevent the same candidate from appearing multiple times
        if source not in candidates:

            candidates[source] = {
                "file_name": source,
                "text": result.text,
                "score": result.score
            }

    # Sort candidates by similarity score
    sorted_candidates = sorted(
        candidates.values(),
        key=lambda x: x["score"] if x["score"] is not None else 0,
        reverse=True
    )

    return sorted_candidates[:max_candidates]