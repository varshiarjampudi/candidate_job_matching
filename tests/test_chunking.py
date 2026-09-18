import pytest

from src.document_loader import load_documents
from src.chunking import chunk_documents


@pytest.fixture(scope="module")
def documents():
    """
    Load the resume documents once for the test module.
    """
    return load_documents("data/resumes")


@pytest.fixture(scope="module")
def nodes(documents):
    """
    Create chunks from the loaded resume documents.
    """
    return chunk_documents(documents)


def test_documents_are_loaded(documents):
    """
    Verify that resume documents are loaded successfully.
    """
    assert documents is not None
    assert len(documents) > 0


def test_documents_are_chunked(nodes):
    """
    Verify that loaded documents are converted into chunks.
    """
    assert nodes is not None
    assert len(nodes) > 0


def test_chunks_contain_text(nodes):
    """
    Verify that generated chunks contain text.
    """
    for node in nodes:
        assert node.text is not None
        assert len(node.text.strip()) > 0


def test_chunks_contain_source_metadata(nodes):
    """
    Verify that chunks retain their source filename.
    """
    for node in nodes:
        assert node.metadata.get("file_name") is not None