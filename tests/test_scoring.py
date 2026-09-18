import pytest

from src.scoring import (
    calculate_match_score,
    rank_candidates
)


@pytest.fixture
def candidate():
    return {
        "file_name": "candidate_05.pdf",
        "score": 0.51,
        "text": """
        Python SQL Power BI Excel Pandas NumPy
        Data Analysis Statistics
        """
    }


@pytest.fixture
def required_skills():
    return [
        "Python",
        "SQL",
        "Power BI",
        "Data Analysis"
    ]


def test_calculate_match_score(candidate, required_skills):
    """
    Verify that the candidate match score is calculated correctly.
    """

    result = calculate_match_score(
        candidate,
        required_skills
    )

    assert result is not None
    assert result["file_name"] == "candidate_05.pdf"
    assert result["match_score"] == 100.0


def test_matched_skills(candidate, required_skills):
    """
    Verify that required skills are correctly identified.
    """

    result = calculate_match_score(
        candidate,
        required_skills
    )

    assert set(result["matched_skills"]) == set(
        required_skills
    )

    assert result["missing_skills"] == []


def test_missing_skills():
    """
    Verify that missing skills are correctly identified.
    """

    candidate = {
        "file_name": "candidate_test.pdf",
        "score": 0.50,
        "text": "Python SQL"
    }

    required_skills = [
        "Python",
        "SQL",
        "Power BI",
        "Excel"
    ]

    result = calculate_match_score(
        candidate,
        required_skills
    )

    assert result["match_score"] == 50.0

    assert set(result["matched_skills"]) == {
        "Python",
        "SQL"
    }

    assert set(result["missing_skills"]) == {
        "Power BI",
        "Excel"
    }


def test_rank_candidates():
    """
    Verify that candidates are ranked by match score.
    """

    candidates = [
        {
            "file_name": "candidate_01.pdf",
            "score": 0.70,
            "text": "Python SQL"
        },
        {
            "file_name": "candidate_02.pdf",
            "score": 0.80,
            "text": "Python SQL Power BI Excel"
        }
    ]

    required_skills = [
        "Python",
        "SQL",
        "Power BI",
        "Excel"
    ]

    ranked = rank_candidates(
        candidates,
        required_skills
    )

    assert len(ranked) == 2

    assert ranked[0]["file_name"] == "candidate_02.pdf"
    assert ranked[0]["match_score"] == 100.0

    assert ranked[1]["file_name"] == "candidate_01.pdf"
    assert ranked[1]["match_score"] == 50.0