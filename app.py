import html
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)

import streamlit as st

from src.rag_pipeline import (
    build_rag_pipeline,
    generate_answer,
    match_candidates_to_role,
    get_role_job_description
)

from src.job_description_loader import (
    get_available_roles,
    extract_required_skills,
    parse_job_description
)

from config.settings import (
    APP_NAME,
    get_role_skills,
    get_role_experience
)
from src.resume_parser import parse_resume


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .role-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333842;
        background-color: #16191f;
        margin-bottom: 15px;
    }

    .candidate-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333842;
        background-color: #16191f;
        margin-bottom: 12px;
    }

    .score {
        font-size: 30px;
        font-weight: 700;
    }

    .small-text {
        color: #9ca3af;
        font-size: 14px;
    }

    .resume-card {
        border: 1px solid #333842;
        border-radius: 10px;
        padding: 18px;
        background: #16191f;
    }

    .resume-header {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: flex-start;
        margin-bottom: 14px;
    }

    .resume-rank {
        color: #9ca3af;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .resume-name {
        font-size: 24px;
        font-weight: 700;
        margin-top: 3px;
    }

    .resume-role {
        color: #b7c0cc;
        font-size: 15px;
        margin-top: 3px;
    }

    .resume-score {
        color: #7dd3a8;
        font-size: 22px;
        font-weight: 700;
        white-space: nowrap;
    }

    .resume-section {
        border-top: 1px solid #2b3038;
        margin-top: 16px;
        padding-top: 14px;
    }

    .resume-section h4 {
        color: #d8dee8;
        font-size: 14px;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .skill-chip {
        background: #252c36;
        border: 1px solid #414b59;
        border-radius: 999px;
        color: #e5e7eb;
        display: inline-block;
        font-size: 13px;
        margin: 0 6px 6px 0;
        padding: 5px 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    f'<div class="main-title">🤖 {APP_NAME}</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered candidate screening, matching and recruitment analysis.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================================================
# LOAD RAG PIPELINE
# ==================================================

@st.cache_resource
def load_pipeline():
    return build_rag_pipeline()


try:
    with st.spinner("Loading recruitment AI..."):
        retriever = load_pipeline()

except Exception as e:
    st.error("Failed to load the RAG pipeline.")
    st.exception(e)
    st.stop()


# ==================================================
# LOAD AVAILABLE JOB ROLES
# ==================================================

roles = get_available_roles()

if not roles:
    st.error(
        "No job descriptions were found in "
        "`data/job_description/`."
    )
    st.stop()


# ==================================================
# JOB ROLE SELECTION
# ==================================================

st.markdown(
    '<div class="section-title">💼 Select Job Role</div>',
    unsafe_allow_html=True
)

selected_role = st.selectbox(
    "Choose a job role",
    roles
)


# ==================================================
# LOAD SELECTED JOB DESCRIPTION
# ==================================================

try:
    job_description = get_role_job_description(
        selected_role
    )

except Exception as e:
    st.error(
        "Unable to load the selected job description."
    )
    st.exception(e)
    st.stop()


# ==================================================
# DISPLAY JOB DESCRIPTION
# ==================================================

with st.expander("📄 View Job Description"):
    job_sections = parse_job_description(job_description)

    if job_sections["job_title"]:
        st.markdown("#### JOB TITLE")
        st.write(" ".join(job_sections["job_title"]))

    if job_sections["job_summary"]:
        st.markdown("#### JOB SUMMARY")
        st.write(" ".join(job_sections["job_summary"]))

    if job_sections["required_skills"]:
        st.markdown("#### REQUIRED SKILLS")
        for skill in job_sections["required_skills"]:
            st.markdown(f"- {skill}")

    if job_sections["experience"]:
        st.markdown("#### EXPERIENCE")
        st.write(" ".join(job_sections["experience"]))

    if job_sections["education"]:
        st.markdown("#### EDUCATION")
        st.write(" ".join(job_sections["education"]))

    if job_sections["responsibilities"]:
        st.markdown("#### RESPONSIBILITIES")
        for responsibility in job_sections["responsibilities"]:
            st.markdown(f"- {responsibility}")


# ==================================================
# ROLE REQUIREMENTS
# ==================================================

st.markdown(
    '<div class="section-title">🛠️ Role Requirements</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Extract skills directly from the selected PDF
# --------------------------------------------------

required_skills = extract_required_skills(
    job_description
)


# --------------------------------------------------
# Fallback to settings.py if extraction fails
# --------------------------------------------------

if not required_skills:

    required_skills = get_role_skills(
        selected_role
    )


# --------------------------------------------------
# Get expected experience
# --------------------------------------------------

required_experience = get_role_experience(
    selected_role
)


# --------------------------------------------------
# Display required skills
# --------------------------------------------------

if required_skills:

    st.write(
        " • ".join(required_skills)
    )

else:

    st.warning(
        "No required skills were found for this role."
    )


# --------------------------------------------------
# Display experience
# --------------------------------------------------

if required_experience:

    st.write(
        f"**Expected Experience:** {required_experience}"
    )


# ==================================================
# CANDIDATE MATCHING
# ==================================================

st.markdown(
    '<div class="section-title">🔍 Candidate Matching</div>',
    unsafe_allow_html=True
)


analyze = st.button(
    "🔍 Analyze Candidates",
    type="primary",
    use_container_width=True
)


# ==================================================
# ANALYZE CANDIDATES
# ==================================================

if analyze:

    # --------------------------------------------------
    # Retrieve and rank candidates
    # --------------------------------------------------

    with st.spinner(
        "Retrieving and ranking candidates..."
    ):

        try:

            ranked_candidates = match_candidates_to_role(
                retriever,
                selected_role,
                required_skills
            )

        except Exception as e:

            st.error(
                "An error occurred during candidate matching."
            )

            st.exception(e)
            st.stop()


    # --------------------------------------------------
    # No candidates
    # --------------------------------------------------

    if not ranked_candidates:

        st.warning(
            "No relevant candidates were found."
        )


    # --------------------------------------------------
    # Candidates found
    # --------------------------------------------------

    else:

        # ==================================================
        # TOP CANDIDATE
        # ==================================================

        top_candidate = ranked_candidates[0]
        top_profile = parse_resume(
            top_candidate.get("text", ""),
            top_candidate.get("file_name")
        )

        st.markdown(
            '<div class="section-title">'
            '🏆 Top Candidate'
            '</div>',
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # Candidate metrics
        # --------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric("Candidate", top_candidate["candidate_name"])


        with col2:

            st.metric(
                "Match Score",
                f'{top_candidate["match_score"]}%'
            )


        with col3:

            similarity = top_candidate.get(
                "similarity_score"
            )

            if similarity is not None:

                st.metric(
                    "Similarity",
                    f"{similarity:.3f}"
                )

            else:

                st.metric(
                    "Similarity",
                    "N/A"
                )

        with col4:
            st.metric(
                "Required Skills",
                f"{len(top_candidate['matched_skills'])} / "
                f"{len(required_skills)}"
            )

        st.caption(
            f"Role: {top_profile['role'] or 'Not specified in the resume'} "
            f"| Best fit role: {selected_role}"
        )


        # ==================================================
        # MATCHED AND MISSING SKILLS
        # ==================================================

        col1, col2 = st.columns(2)


        # --------------------------------------------------
        # Matched skills
        # --------------------------------------------------

        with col1:

            st.markdown(
                "### ✅ Matched Skills"
            )

            if top_candidate["matched_skills"]:

                for skill in top_candidate["matched_skills"]:

                    st.write(
                        f"✓ {skill}"
                    )

            else:

                st.write(
                    "No required skills matched."
                )


        # --------------------------------------------------
        # Missing skills
        # --------------------------------------------------

        with col2:

            st.markdown(
                "### ⚠️ Missing Skills"
            )

            if top_candidate["missing_skills"]:

                for skill in top_candidate["missing_skills"]:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.write("None")


        # ==================================================
        # CANDIDATE RANKING
        # ==================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Candidate Ranking'
            '</div>',
            unsafe_allow_html=True
        )


        ranking_data = []


        for rank, candidate in enumerate(
            ranked_candidates,
            start=1
        ):

            ranking_data.append(
                {
                    "Rank": rank,

                    "Candidate": candidate["candidate_name"],

                    "Match Score": candidate[
                        "match_score"
                    ],

                    "Similarity Score": candidate.get(
                        "similarity_score",
                        "N/A"
                    ),

                    "Matched Skills": ", ".join(
                        candidate[
                            "matched_skills"
                        ]
                    ),

                    "Missing Skills": (
                        ", ".join(
                            candidate[
                                "missing_skills"
                            ]
                        )
                        if candidate[
                            "missing_skills"
                        ]
                        else "None"
                    )
                }
            )


        st.dataframe(
            ranking_data,
            use_container_width=True,
            hide_index=True
        )


        # ==================================================
        # CANDIDATE EVIDENCE
        # ==================================================

        st.markdown(
            '<div class="section-title">'
            '📄 Candidate Evidence'
            '</div>',
            unsafe_allow_html=True
        )


        for rank, candidate in enumerate(
            ranked_candidates[:5],
            start=1
        ):

            profile = parse_resume(
                candidate.get("text", ""),
                candidate.get("file_name")
            )

            with st.expander(
                f'#{rank} — {candidate["candidate_name"]} '
                f'({candidate["match_score"]}% match)'
            ):

                safe_name = html.escape(candidate["candidate_name"])
                safe_role = html.escape(
                    profile["role"] or "Role not specified in the resume"
                )
                st.markdown(
                    f"""
                    <div class="resume-card">
                        <div class="resume-header">
                            <div>
                                <div class="resume-rank">#{rank}</div>
                                <div class="resume-name">{safe_name}</div>
                                <div class="resume-role">{safe_role}</div>
                            </div>
                            <div class="resume-score">
                                {candidate["match_score"]}% Match
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("#### Match Information")
                match_col, missing_col = st.columns(2)

                with match_col:
                    st.markdown("**Matched Skills**")
                    if candidate["matched_skills"]:
                        for skill in candidate["matched_skills"]:
                            st.write(f"✓ {skill}")
                    else:
                        st.write("None")

                with missing_col:
                    st.markdown("**Missing Skills**")
                    if candidate["missing_skills"]:
                        for skill in candidate["missing_skills"]:
                            st.write(f"• {skill}")
                    else:
                        st.write("None")

                if profile["professional_summary"]:
                    st.markdown("#### Professional Summary")
                    st.write(" ".join(profile["professional_summary"]))

                if profile["technical_skills"]:
                    st.markdown("#### Technical Skills")
                    skill_chips = "".join(
                        f'<span class="skill-chip">{html.escape(skill)}</span>'
                        for skill in profile["technical_skills"]
                    )
                    st.markdown(skill_chips, unsafe_allow_html=True)

                section_labels = [
                    ("Work Experience", "work_experience"),
                    ("Projects", "projects"),
                    ("Education", "education"),
                    ("Certifications", "certifications")
                ]

                for label, section_key in section_labels:
                    if not profile[section_key]:
                        continue

                    st.markdown(f"#### {label}")
                    for line in profile[section_key]:
                        st.markdown(f"- {html.escape(line)}")


        # ==================================================
        # AI RECRUITMENT ANALYSIS
        # ==================================================

        st.markdown(
            '<div class="section-title">'
            '🤖 AI Recruitment Analysis'
            '</div>',
            unsafe_allow_html=True
        )


        recruiter_query = (
            f"Analyze the candidates for the "
            f"{selected_role} role. "

            f"Explain why the top candidates "
            f"are suitable, "

            f"mention their matched and missing "
            f"skills, "

            f"and provide a recruitment "
            f"recommendation."
        )


        with st.spinner(
            "Generating AI recruitment analysis..."
        ):

            try:

                answer = generate_answer(
                    ranked_candidates,
                    recruiter_query,
                    role=selected_role,
                    required_skills=required_skills
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "Failed to generate AI analysis."
                )

                st.exception(e)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🤖 Recruitment AI")


    st.write(
        "AI-powered recruitment intelligence "
        "for candidate screening and job matching."
    )


    st.divider()


    # ==================================================
    # SYSTEM
    # ==================================================

    st.subheader("⚙️ System")


    st.write(
        """
        **Resume Processing**

        PDF → Text → Chunks

        **Semantic Search**

        Sentence Transformers

        **Vector Database**

        ChromaDB

        **Candidate Matching**

        Skill-based ranking

        **LLM**

        Groq

        **Application**

        Streamlit
        """
    )


    st.divider()


    # ==================================================
    # RAG PIPELINE
    # ==================================================

    st.subheader("🔄 RAG Pipeline")


    st.code(
        """
Resumes
   ↓
Document Loader
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
Semantic Retrieval
   ↓
Candidate Scoring
   ↓
Ranking
   ↓
Groq LLM
   ↓
Recruitment Analysis
        """,
        language="text"
    )