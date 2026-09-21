from pydantic import BaseModel, model_validator
from typing import List

class Education(BaseModel):
    school: str = ""
    college: str = ""
    degree: str = ""
    start_year: str = ""
    end_year: str = ""

class WorkExperience(BaseModel):
    company: str = ""
    position: str = ""
    years: str = ""
    description: str = ""

class Resume(BaseModel):
    name: str = ""
    email: str = ""
    skills: list[str] = []
    education: List[Education] | Education = []
    work_experience: List[WorkExperience] | WorkExperience = []

    @model_validator(mode="before")
    @classmethod
    def normalize_resume_lists(cls, values):
        if isinstance(values, dict):
            for field in ("education", "work_experience"):
                item = values.get(field)
                if isinstance(item, dict):
                    values[field] = [item]
        return values


