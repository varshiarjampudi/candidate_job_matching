import pytest

from src.document_loader import load_documents
from src.chunking import chunk_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store
from src.retriveal import (
    create_retriever,
    retrieve_unique_candidates
)


@pytest.fixture(scope="module")
def retriever():
    """
    Build the retrieval pipeline once for the test module.
    """

    documents = load_documents("data/resumes")

    assert len(documents) > 0

    nodes = chunk_documents(documents)

    assert len(nodes) > 0

    embed_model = get_embedding_model()

    index = create_vector_store(
        nodes,
        embed_model
    )

    return create_retriever(
        index,
        similarity_top_k=5
    )


def test_retriever_is_created(retriever):
    """
    Verify that the retriever is created successfully.
    """

    assert retriever is not None


def test_retriever_returns_results(retriever):
    """
    Verify that semantic retrieval returns results.
    """

    query = (
        "Find candidates with Python, SQL and "
        "Power BI experience."
    )

    results = retriever.retrieve(query)

    assert results is not None
    assert len(results) > 0


def test_retrieved_results_contain_metadata(retriever):
    """
    Verify that retrieved results contain source metadata.
    """

    query = (
        "Find candidates with Python, SQL and "
        "Power BI experience."
    )

    results = retriever.retrieve(query)

    for result in results:

        file_name = result.node.metadata.get(
            "file_name"
        )

        assert file_name is not None


def test_unique_candidate_retrieval(retriever):
    """
    Verify that duplicate resume chunks are reduced
    to unique candidates.
    """

    query = (
        "Find candidates with Python, SQL and "
        "Power BI experience."
    )

    candidates = retrieve_unique_candidates(
        retriever,
        query,
        max_candidates=5
    )

    assert candidates is not None
    assert len(candidates) > 0

    file_names = [
        candidate["file_name"]
        for candidate in candidates
    ]

    assert len(file_names) == len(set(file_names))