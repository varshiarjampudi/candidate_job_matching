import os

from dotenv import load_dotenv
from llama_index.llms.groq import Groq

from src.document_loader import load_documents
from src.chunking import chunk_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store
from src.retriveal import (
    create_retriever,
    retrieve_unique_candidates
)
from src.prompts import create_prompt
from src.scoring import rank_candidates
from src.job_description_loader import get_job_description


load_dotenv()


def build_rag_pipeline():
    """
    Build the complete RAG pipeline for candidate resumes.
    """

    print("Loading resumes...")

    documents = load_documents("data/resumes")

    print(f"Loaded {len(documents)} documents")

    nodes = chunk_documents(documents)

    print(f"Created {len(nodes)} chunks")

    embed_model = get_embedding_model()

    index = create_vector_store(
        nodes,
        embed_model
    )

    retriever = create_retriever(
        index,
        similarity_top_k=10
    )

    print("RAG pipeline ready!")

    return retriever


def match_candidates_to_role(
    retriever,
    role,
    required_skills
):
    """
    Retrieve candidates and rank them
    according to the selected job role.
    """

    query = (
        f"Find candidates suitable for a "
        f"{role} position with relevant skills "
        f"and experience."
    )

    candidates = retrieve_unique_candidates(
        retriever,
        query,
        max_candidates=10
    )

    if not candidates:
        return []

    ranked_candidates = rank_candidates(
        candidates,
        required_skills
    )

    return ranked_candidates


def generate_answer(
    ranked_candidates,
    query,
    role=None,
    required_skills=None
):
    """
    Explain an already-ranked candidate set with the LLM.

    Retrieval, scoring, and ranking must happen before this function.
    The LLM receives those exact results and is not allowed to recalculate
    or reorder them.
    """

    if not ranked_candidates:
        return "No relevant candidates were found."

    # --------------------------------------------------
    # Build context from the deterministic ranking
    # --------------------------------------------------

    context_parts = []

    for rank, candidate in enumerate(ranked_candidates, start=1):
        matched_skills = ", ".join(candidate["matched_skills"]) or "None"
        missing_skills = ", ".join(candidate["missing_skills"]) or "None"

        context_parts.append(
            f"""
Rank:
{rank}

Candidate Name:
{candidate["candidate_name"]}

Source Filename:
{candidate["file_name"]}

Match Score:
{candidate["match_score"]}%

Similarity Score:
{candidate.get("similarity_score", "Not available")}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Resume Evidence:
{candidate.get(
    "text",
    "Resume evidence unavailable."
)}
"""
        )

    context = "\n".join(context_parts)

    # --------------------------------------------------
    # Create prompt
    # --------------------------------------------------

    if role:
        role_context = (
            f"The selected job role is: {role}\n"
            f"Required skills: "
            f"{', '.join(required_skills)}\n\n"
        )
    else:
        role_context = ""

    final_query = (
        role_context +
        f"Recruiter Query:\n{query}"
    )

    prompt = create_prompt(
        final_query,
        context
    )

    # --------------------------------------------------
    # Groq LLM
    # --------------------------------------------------

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Check your .env file."
        )

    llm = Groq(
        model="openai/gpt-oss-120b",
        api_key=api_key
    )

    response = llm.complete(prompt)

    return response.text


def get_role_job_description(role):
    """
    Load the job description for a selected role.
    """

    return get_job_description(role)