import openai # type: ignore
import fitz   # type: ignore
from secret_key import openai_key
from resumeparser import ResumeParser

openai.api_key = openai_key

r1 = ResumeParser()

text = r1.read_pdf_file("CVs/cv82.pdf")
r1.cvParser(text)

openai.api_key = openai_key