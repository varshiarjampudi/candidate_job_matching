import re
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOB_DESCRIPTION_DIR = PROJECT_ROOT / "data" / "job_description"

SECTION_HEADERS = {
    "JOB TITLE",
    "JOB SUMMARY",
    "REQUIRED SKILLS",
    "REQUIRED SKILL",
    "TECHNICAL SKILLS",
    "EXPERIENCE",
    "EDUCATION",
    "RESPONSIBILITIES",
    "PREFERRED SKILLS",
    "QUALIFICATIONS"
}


def get_available_roles():
    """
    Return all available job roles based on job description PDF files.
    """

    if not JOB_DESCRIPTION_DIR.exists():
        return []

    roles = []

    for file in JOB_DESCRIPTION_DIR.glob("*.pdf"):
        role_name = file.stem.replace("_", " ").title()
        roles.append(role_name)

    return sorted(roles)


def get_job_description(role):
    """
    Load the complete job description for a selected role.
    """

    file_name = role.lower().replace(" ", "_") + ".pdf"

    file_path = JOB_DESCRIPTION_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Job description not found for role: {role}"
        )

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n".join(pages).strip()


def extract_required_skills(job_description):
    """
    Extract required skills from the REQUIRED SKILLS
    section of a job description.
    """

    return parse_job_description(job_description)["required_skills"]


def parse_job_description(job_description):
    """Parse the recruiter-facing sections from extracted PDF text."""

    sections = {
        "job_title": [],
        "job_summary": [],
        "required_skills": [],
        "experience": [],
        "education": [],
        "responsibilities": []
    }
    current_section = None

    for raw_line in job_description.splitlines():
        line = raw_line.strip().lstrip("\x7f•-* ").strip()
        if not line:
            continue

        normalized = line.upper().rstrip(":").strip()
        header = normalized if normalized in SECTION_HEADERS else None

        if header:
            current_section = {
                "JOB TITLE": "job_title",
                "JOB SUMMARY": "job_summary",
                "REQUIRED SKILLS": "required_skills",
                "REQUIRED SKILL": "required_skills",
                "TECHNICAL SKILLS": "required_skills",
                "EXPERIENCE": "experience",
                "EDUCATION": "education",
                "RESPONSIBILITIES": "responsibilities"
            }.get(header)
            continue

        inline_title = re.match(r"^JOB TITLE\s*:\s*(.+)$", line, re.IGNORECASE)
        if inline_title:
            sections["job_title"].append(inline_title.group(1).strip())
            current_section = "job_title"
            continue

        if current_section:
            sections[current_section].append(line)

    return sections