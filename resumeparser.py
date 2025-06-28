import openai  
import fitz    
from docx import Document  

from secret_key import openai_key

openai.api_key = openai_key

class ResumeParser:
    def read_word_file(self,file_path):
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    

    def read_pdf_file(self,file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    
    def cvParser(self, data):
        prompt = (
            "You are a CV parser. Extract the following from the CV text: "
            "name, phone number, email, LinkedIn profile link, experience, education (institutes), "
            "Then, based on the overall CV quality, **assign a score out of 100**, considering:"
            "- Relevance of experience"
            "- Strength of education background"
            "- Skillset match to modern industry expectations"
            "- Clarity and completeness of the resume"
            "- Overall impression "
            "Output should be a valid JSON format, and every key in camelcase"
        )
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are an expert in parsing resumes."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": data}
            ]
        )
        content = response.choices[0].message.content
        with open("output2_cv_data.json", "w", encoding="utf-8") as json_file:
            json_file.write(content)

# r1 = ResumeParser
# text = r1.read_pdf_file("CVs/mycv.pdf")
# r1.cvParser(text)

