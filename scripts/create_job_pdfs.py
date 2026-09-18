from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT


OUTPUT_DIR = Path("data/job_description")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

title_style = styles["Title"]
heading_style = styles["Heading2"]
body_style = styles["BodyText"]

body_style.alignment = TA_LEFT
body_style.leading = 16


job_descriptions = {

    "data_analyst": {
        "title": "Data Analyst",
        "summary": (
            "We are looking for a Data Analyst who can analyze business "
            "data, identify useful insights, and create clear reports "
            "and dashboards to support data-driven decision making."
        ),
        "skills": [
            "Python",
            "SQL",
            "Power BI",
            "Data Analysis",
            "Excel",
            "Statistics"
        ],
        "experience": "0-3 years",
        "education": (
            "Bachelor's degree in Computer Science, Information Technology, "
            "Data Science, Statistics, or a related field."
        ),
        "responsibilities": [
            "Analyze and clean structured datasets.",
            "Write SQL queries to extract and transform data.",
            "Use Python for data analysis and preprocessing.",
            "Create dashboards and reports using Power BI.",
            "Perform statistical analysis and identify trends.",
            "Communicate insights clearly to stakeholders.",
            "Support business decisions using data-driven insights."
        ]
    },

    "backend_developer": {
        "title": "Backend Developer",
        "summary": (
            "We are looking for a Backend Developer to build, maintain, "
            "and improve reliable server-side applications and APIs."
        ),
        "skills": [
            "Python",
            "REST API",
            "SQL",
            "PostgreSQL",
            "Git",
            "Docker"
        ],
        "experience": "1-4 years",
        "education": (
            "Bachelor's degree in Computer Science, Information Technology, "
            "Software Engineering, or a related field."
        ),
        "responsibilities": [
            "Develop and maintain backend applications.",
            "Design and implement REST APIs.",
            "Work with SQL databases and PostgreSQL.",
            "Write clean, maintainable, and efficient code.",
            "Use Git for version control and collaboration.",
            "Containerize applications using Docker.",
            "Debug backend issues and improve application performance.",
            "Collaborate with frontend developers and other team members."
        ]
    },

    "data_scientist": {
        "title": "Data Scientist",
        "summary": (
            "We are looking for a Data Scientist to analyze complex "
            "datasets, build predictive models, and generate actionable "
            "insights."
        ),
        "skills": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Data Visualization"
        ],
        "experience": "1-4 years",
        "education": (
            "Bachelor's or Master's degree in Computer Science, Data Science, "
            "Statistics, Mathematics, or a related field."
        ),
        "responsibilities": [
            "Analyze and preprocess large datasets.",
            "Build and evaluate machine learning models.",
            "Perform statistical analysis.",
            "Use Python, Pandas, and NumPy for data analysis.",
            "Write SQL queries for data extraction.",
            "Create meaningful data visualizations.",
            "Identify patterns and trends in datasets.",
            "Communicate technical findings and business insights."
        ]
    },

    "machine_learning_engineer": {
        "title": "Machine Learning Engineer",
        "summary": (
            "We are looking for a Machine Learning Engineer to develop, "
            "train, evaluate, and deploy machine learning models."
        ),
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "TensorFlow",
            "PyTorch"
        ],
        "experience": "0-3 years",
        "education": (
            "Bachelor's or Master's degree in Computer Science, Data Science, "
            "Artificial Intelligence, Mathematics, or a related field."
        ),
        "responsibilities": [
            "Develop and evaluate machine learning models.",
            "Prepare and preprocess datasets for machine learning.",
            "Use Python, Pandas, and NumPy for data processing.",
            "Apply machine learning algorithms using Scikit-learn.",
            "Work with SQL databases and structured datasets.",
            "Build and optimize model training pipelines.",
            "Use TensorFlow or PyTorch for machine learning projects.",
            "Evaluate model performance and improve model accuracy.",
            "Collaborate with software engineers and data scientists."
        ]
    },

    "python_developer": {
        "title": "Python Developer",
        "summary": (
            "We are looking for a Python Developer to design, develop, "
            "test, and maintain reliable software applications."
        ),
        "skills": [
            "Python",
            "Django",
            "Flask",
            "REST API",
            "SQL",
            "Git",
            "Docker"
        ],
        "experience": "0-3 years",
        "education": (
            "Bachelor's degree in Computer Science, Information Technology, "
            "Software Engineering, or a related field."
        ),
        "responsibilities": [
            "Develop applications using Python.",
            "Build and maintain backend services.",
            "Develop and integrate REST APIs.",
            "Work with SQL databases.",
            "Use Django or Flask for web application development.",
            "Write clean and maintainable Python code.",
            "Use Git for version control.",
            "Containerize applications using Docker.",
            "Test and debug applications.",
            "Collaborate with developers and other technical teams."
        ]
    }
}


def create_pdf(filename, job):
    file_path = OUTPUT_DIR / f"{filename}.pdf"

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    story = []

    story.append(
        Paragraph(
            f"JOB TITLE: {job['title']}",
            title_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "JOB SUMMARY",
            heading_style
        )
    )

    story.append(
        Paragraph(
            job["summary"],
            body_style
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "REQUIRED SKILLS",
            heading_style
        )
    )

    for skill in job["skills"]:
        story.append(
            Paragraph(
                f"• {skill}",
                body_style
            )
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "EXPERIENCE",
            heading_style
        )
    )

    story.append(
        Paragraph(
            job["experience"],
            body_style
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "EDUCATION",
            heading_style
        )
    )

    story.append(
        Paragraph(
            job["education"],
            body_style
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "RESPONSIBILITIES",
            heading_style
        )
    )

    for responsibility in job["responsibilities"]:
        story.append(
            Paragraph(
                f"• {responsibility}",
                body_style
            )
        )

    document.build(story)

    print(f"Created: {file_path}")


for filename, job in job_descriptions.items():
    create_pdf(filename, job)

print("\nAll job description PDFs created successfully.")