import re
from pathlib import Path


SECTION_ALIASES = {
    "PROFESSIONAL SUMMARY": "professional_summary",
    "SUMMARY": "professional_summary",
    "PROFILE": "professional_summary",
    "TECHNICAL SKILLS": "technical_skills",
    "SKILLS": "technical_skills",
    "TECHNOLOGIES": "technical_skills",
    "WORK EXPERIENCE": "work_experience",
    "EXPERIENCE": "work_experience",
    "INTERNSHIP": "work_experience",
    "PROJECTS": "projects",
    "PROJECT EXPERIENCE": "projects",
    "EDUCATION": "education",
    "ACADEMIC QUALIFICATIONS": "education",
    "CERTIFICATIONS": "certifications",
    "CERTIFICATES": "certifications"
}


def _clean_line(line):
    return line.strip().lstrip("\x7f•-* ").strip()


def _fallback_name(file_name):
    if not file_name:
        return "Candidate"

    candidate_match = re.search(
        r"candidate[_ -]?(\d+)",
        Path(file_name).stem,
        flags=re.IGNORECASE
    )

    if candidate_match:
        return f"Candidate {int(candidate_match.group(1)):02d}"

    return "Candidate"


def parse_resume(text, file_name=None):
    """Parse known resume sections without inventing missing information."""

    parsed = {
        "name": _fallback_name(file_name),
        "role": "",
        "professional_summary": [],
        "technical_skills": [],
        "work_experience": [],
        "projects": [],
        "education": [],
        "certifications": []
    }
    current_section = None

    for raw_line in (text or "").splitlines():
        line = _clean_line(raw_line)
        if not line:
            continue

        metadata_match = re.match(
            r"^(Name|Role)\s*:\s*(.+)$",
            line,
            flags=re.IGNORECASE
        )
        if metadata_match:
            field = metadata_match.group(1).lower()
            parsed[field] = metadata_match.group(2).strip()
            current_section = None
            continue

        normalized = line.upper().rstrip(":").strip()
        section = SECTION_ALIASES.get(normalized)
        if section:
            current_section = section
            continue

        if current_section:
            parsed[current_section].append(line)

    if parsed["technical_skills"]:
        skills = []
        for line in parsed["technical_skills"]:
            skills.extend(
                skill.strip()
                for skill in re.split(r"[;,|]", line)
                if skill.strip()
            )
        parsed["technical_skills"] = skills

    return parsed


def extract_candidate_name(text, file_name=None):
    """Return the resume name or a safe filename-based fallback."""

    return parse_resume(text, file_name)["name"]
