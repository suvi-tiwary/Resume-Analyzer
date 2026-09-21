from pydantic import BaseModel, Field
from typing import List


class EducationItem(BaseModel):
    """Schema representing an education entry in a parsed resume."""
    degree: str = Field(default="", description="Degree earned (e.g. B.Tech, M.S.)")
    institution: str = Field(default="", description="Name of the university/college")
    field: str = Field(default="", description="Field of study / specialization")
    start_year: str = Field(default="", description="Starting year")
    end_year: str = Field(default="", description="Completion / expected year")


class WorkExperienceItem(BaseModel):
    """Schema representing a work experience entry in a parsed resume."""
    job_title: str = Field(default="", description="Role or job designation")
    company: str = Field(default="", description="Company or organization name")
    start_date: str = Field(default="", description="Start date (e.g. June 2026)")
    end_date: str = Field(default="", description="End date (e.g. August 2026)")
    description: str = Field(default="", description="Brief summary of duties and achievements")


class ResumeResponse(BaseModel):
    """Consistent structured schema for the resume parsing API response."""
    name: str = Field(default="", description="Full name of the candidate")
    email: str = Field(default="", description="Email address")
    phone: str = Field(default="", description="Contact phone number")
    skills: List[str] = Field(default_factory=list, description="Extracted skills list")
    education: List[EducationItem] = Field(default_factory=list, description="List of education entries")
    work_experience: List[WorkExperienceItem] = Field(default_factory=list, description="List of work experience entries")
