from src.resume_parser import extract_candidate_name as parse_candidate_name


def extract_candidate_name(text, file_name):
    """
    Extract a candidate name from a resume header.

    The fallback keeps the source filename available while avoiding
    fabricated names when the resume does not identify the candidate.
    """

    return parse_candidate_name(text, file_name)


def calculate_match_score(candidate, required_skills):
    """
    Calculate candidate match score based on required skills.
    """

    text = candidate["text"].lower()

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_score = 0

    return {
        "file_name": candidate["file_name"],
        "candidate_name": extract_candidate_name(
            candidate["text"],
            candidate["file_name"]
        ),
        "similarity_score": candidate["score"],
        "text": candidate["text"],
        "match_score": round(skill_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


def rank_candidates(candidates, required_skills):
    """
    Calculate match scores and rank candidates from highest
    to lowest match score.
    """

    scored_candidates = []

    for candidate in candidates:
        result = calculate_match_score(
            candidate,
            required_skills
        )

        scored_candidates.append(result)

    scored_candidates.sort(
        key=lambda x: (
            x["match_score"],
            x["similarity_score"] if x["similarity_score"] is not None else 0
        ),
        reverse=True
    )

    return scored_candidates