from pydantic import BaseModel
from typing import List

class Education(BaseModel):
    school:str
    collge:str
    degree:str
    start_year:str
    end_year:str

class workExperience(BaseModel):
    company:str
    position:str
    years:int
    description:str

class Resume(BaseModel):
    name:str
    email:str
    skills:list[str]
    education:List[Education]    
    work_experience=List[workExperience]


