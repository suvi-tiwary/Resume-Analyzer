from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema import Resume
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


structured_llm = llm.with_structured_output(Resume)


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


def resume_parse(resume_text: str) -> Resume:

    chain = prompt | structured_llm

    result = chain.invoke({
        "resume_text": resume_text
    })

    return result