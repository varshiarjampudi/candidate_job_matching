import pytest

from src.rag_pipeline import (
    build_rag_pipeline,
    match_candidates_to_role,
    generate_answer
)


@pytest.fixture(scope="module")
def retriever():
    """
    Build the RAG pipeline once for the test module.
    """
    return build_rag_pipeline()


def test_rag_pipeline_builds(retriever):
    """
    Verify that the RAG pipeline builds successfully.
    """
    assert retriever is not None


def test_generate_answer(retriever):
    """
    Verify that candidate ranking and LLM analysis work together.
    """

    role = "Data Analyst"

    required_skills = [
        "Python",
        "SQL",
        "Power BI",
        "Data Analysis"
    ]

    ranked_candidates = match_candidates_to_role(
        retriever,
        role,
        required_skills
    )

    assert ranked_candidates is not None
    assert isinstance(ranked_candidates, list)
    assert len(ranked_candidates) > 0

    query = (
        "Which candidates are the best fit for a Data Analyst "
        "role requiring Python, SQL, Power BI and data analysis?"
    )

    answer = generate_answer(
        ranked_candidates,
        query,
        role=role,
        required_skills=required_skills
    )

    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0