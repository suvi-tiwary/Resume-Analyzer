"""
Legacy schema module kept for backward compatibility.
New code should import from app.schemas.resume.
"""
from app.schemas.resume import (
    EducationItem as Education,
    WorkExperienceItem as workExperience,
    ResumeResponse as Resume,
)

__all__ = ["Education", "workExperience", "Resume"]
