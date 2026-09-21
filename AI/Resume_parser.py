from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import Resume
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert resume parser.

        Extract information from the resume and return it
        according to the provided structure.

        Rules:
        - Do not invent information.
        - If information is missing, return an empty string
          or empty list.
        - Extract skills mentioned in the resume.
        - Extract all education entries.
        - Extract all work experience entries.
        """
    ),
    (
        "human",
        """
        Parse the following resume:

        {resume_text}
        """
    )
])


@lru_cache(maxsize=1)
def get_structured_llm():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    return llm.with_structured_output(Resume)


def resume_parse(resume_text: str) -> Resume:

    chain = prompt | get_structured_llm()

    result = chain.invoke({
        "resume_text": resume_text
    })

    return result