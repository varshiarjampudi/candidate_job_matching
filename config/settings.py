# --------------------------------------------------
# Application Settings
# --------------------------------------------------

APP_NAME = "Recruitment Intelligence AI"

LLM_MODEL = "openai/gpt-oss-120b"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

RETRIEVAL_TOP_K = 10

MAX_CANDIDATES = 10


# --------------------------------------------------
# Job Role Configuration
# --------------------------------------------------

ROLE_CONFIG = {

    "Data Analyst": {
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Data Analysis"
        ],
        "experience": "0-3 years"
    },

    "Python Developer": {
        "skills": [
            "Python",
            "Django",
            "Flask",
            "REST API",
            "SQL",
            "Git",
            "Docker"
        ],
        "experience": "0-3 years"
    },

    "Backend Developer": {
        "skills": [
            "Python",
            "REST API",
            "SQL",
            "PostgreSQL",
            "Git",
            "Docker"
        ],
        "experience": "1-4 years"
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL"
        ],
        "experience": "0-3 years"
    },

    "Data Scientist": {
        "skills": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Data Visualization"
        ],
        "experience": "1-4 years"
    }
}


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def get_role_skills(role):
    """
    Return required skills for a job role.
    """

    role_config = ROLE_CONFIG.get(role)

    if not role_config:
        return []

    return role_config["skills"]


def get_role_experience(role):
    """
    Return expected experience for a job role.
    """

    role_config = ROLE_CONFIG.get(role)

    if not role_config:
        return ""

    return role_config["experience"]