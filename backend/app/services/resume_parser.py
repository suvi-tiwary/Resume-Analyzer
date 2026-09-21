import re
import logging
from typing import List
# pyrefly: ignore [missing-import]
from ..schemas.resume import ResumeResponse, EducationItem, WorkExperienceItem

logger = logging.getLogger(__name__)

# Configurable list of recognized technical skills
DEFAULT_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "React",
    "React Native",
    "Angular",
    "Vue.js",
    "Node.js",
    "Express",
    "FastAPI",
    "Django",
    "Flask",
    "SQL",
    "NoSQL",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "Redis",
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "CI/CD",
    "Linux",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Computer Vision",
    "Data Science",
    "HTML",
    "CSS",
    "Tailwind CSS",
    "REST API",
    "GraphQL",
]


def extract_email(text: str) -> str:
    """Extracts the first valid email address from the text."""
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(email_pattern, text)
    return match.group(0).strip() if match else ""


def extract_phone(text: str) -> str:
    """
    Extracts phone numbers supporting common Indian (+91) and international formats.
    e.g. +91 98765 43210, +91-9876543210, 9876543210, (555) 123-4567
    """
    patterns = [
        r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}",  # Indian 10-digit mobile
        r"\+?\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}",  # International
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Clean up extra spacing
            cleaned = match.group(0).strip()
            # Verify reasonable digit count
            digits = re.sub(r"\D", "", cleaned)
            if 10 <= len(digits) <= 15:
                return cleaned
    return ""


def extract_name(text: str) -> str:
    """
    Heuristically extracts the candidate's name from the top lines of the resume text.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    invalid_keywords = {
        "resume", "curriculum", "vitae", "cv", "page", "contact",
        "email", "phone", "profile", "summary", "objective", "experience",
        "education", "skills", "projects", "http", "https", "github", "linkedin"
    }

    for line in lines[:8]:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in invalid_keywords):
            continue
        if "@" in line or re.search(r"\d", line):
            continue
        # Names are typically 2-4 words, alphabet characters
        words = line.split()
        if 2 <= len(words) <= 4 and all(re.match(r"^[A-Za-z.'-]+$", w) for w in words):
            return " ".join(words)

    # Fallback to first non-empty line if reasonably short
    if lines and len(lines[0].split()) <= 4 and not re.search(r"[@\d]", lines[0]):
        return lines[0]

    return ""


def extract_skills(text: str, skill_list: List[str] = DEFAULT_SKILLS) -> List[str]:
    """
    Finds skills from the text against a configurable list of technical skills.
    Avoids duplicate entries while preserving canonical casing.
    """
    matched_skills = []
    text_lower = f" {text.lower()} "

    for skill in skill_list:
        # Regex to handle special characters like C++, C#, .NET, etc.
        escaped_skill = re.escape(skill.lower())
        pattern = rf"(?<!\w){escaped_skill}(?!\w)"
        if re.search(pattern, text_lower):
            if skill not in matched_skills:
                matched_skills.append(skill)

    return matched_skills


def extract_education(text: str) -> List[EducationItem]:
    """
    Rule-based education extraction with degree, field, institution, and year matching.
    """
    education_entries = []
    common_degrees = [
        "b.tech", "b.e.", "b.e", "btech", "m.tech", "mtech",
        "bca", "mca", "b.sc", "m.sc", "bachelor", "master", "phd"
    ]
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        for deg in common_degrees:
            if re.search(rf"\b{re.escape(deg)}\b", line_lower):
                degree_text = line
                field = ""
                # Check for "in <Field>"
                in_match = re.search(r"\b(?:in|of)\s+([A-Za-z\s]+?)(?:,|\(|$)", line, re.IGNORECASE)
                if in_match:
                    field = in_match.group(1).strip()
                    degree_text = line[:in_match.start()].strip().rstrip(",")

                # Search current and next line for years
                context = line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
                year_match = re.search(r"\b(19\d\d|20\d\d)\b[\s–—-]+(\b(?:19\d\d|20\d\d|present)\b)?", context, re.IGNORECASE)
                start_year = year_match.group(1) if year_match else ""
                end_year = year_match.group(2) if year_match and year_match.group(2) else ""

                # Institution is usually the next line or rest of current line
                institution = ""
                if i + 1 < len(lines) and len(lines[i + 1]) < 90 and not any(d in lines[i + 1].lower() for d in common_degrees):
                    institution_line = lines[i + 1]
                    # Clean any trailing years from institution line
                    institution = re.sub(r"\b(19\d\d|20\d\d)\b[\s–—-]+(\b(?:19\d\d|20\d\d|present)\b)?", "", institution_line).strip().rstrip("-—,")

                entry = EducationItem(
                    degree=degree_text,
                    institution=institution,
                    field=field,
                    start_year=start_year,
                    end_year=end_year
                )
                education_entries.append(entry)
                break
        if len(education_entries) >= 3:
            break

    return education_entries


def extract_experience(text: str) -> List[WorkExperienceItem]:
    """
    Rule-based work experience extraction searching for role titles and companies.
    """
    experience_entries = []
    job_titles = [
        "software developer intern", "software engineer intern", "web developer intern",
        "frontend developer", "backend developer", "full stack developer",
        "software engineer", "software developer", "data scientist",
        "data analyst", "devops engineer", "intern", "engineer"
    ]
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        for title in job_titles:
            pattern = rf"\b{re.escape(title)}\b"
            if re.search(pattern, line_lower):
                job_title = line
                company = ""
                start_date = ""
                end_date = ""
                description = ""

                # Check "at <Company>" or "— <Company>"
                at_match = re.search(r"\b(?:at|@|—|-)\s+([A-Za-z0-9\s.,]+)", line)
                if at_match:
                    company = at_match.group(1).strip()
                    job_title = line[:at_match.start()].strip()
                elif i + 1 < len(lines) and len(lines[i + 1]) < 60:
                    company = lines[i + 1].strip()

                # Look for dates
                date_match = re.search(
                    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*(19\d\d|20\d\d)\b[\s–—-]+(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*(19\d\d|20\d\d|Present|present))\b",
                    line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
                )
                if date_match:
                    parts = date_match.group(0).split("–") if "–" in date_match.group(0) else date_match.group(0).split("-")
                    if len(parts) == 2:
                        start_date = parts[0].strip()
                        end_date = parts[1].strip()

                # Look for brief description in following lines
                for j in range(i + 1, min(i + 4, len(lines))):
                    if len(lines[j]) > 30 and not any(k in lines[j].lower() for k in ["education", "skills", "projects", "experience"]):
                        description = lines[j].strip()
                        break

                experience_entries.append(WorkExperienceItem(
                    job_title=job_title,
                    company=company,
                    start_date=start_date,
                    end_date=end_date,
                    description=description
                ))
                break
        if len(experience_entries) >= 3:
            break

    return experience_entries


def parse_resume_text(text: str) -> ResumeResponse:
    """
    Parses raw resume text into a structured ResumeResponse model.
    """
    if not text:
        return ResumeResponse()

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    work_experience = extract_experience(text)

    return ResumeResponse(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        education=education,
        work_experience=work_experience,
    )
