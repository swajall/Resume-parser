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
            "You are a professional and consistent resume parser.\n"
            "Parse the following CV text and extract the following fields. Return the output strictly in JSON format with keys in camelCase.\n"
            "Ensure all keys are always present, even if the value is null or an empty list.\n"
            "\n"
            "The output JSON should contain these keys:\n"
            "- name: string\n"
            "- phoneNumber: string\n"
            "- email: string\n"
            "- linkedinProfile: string or null\n"
            "- githubProfile: string or null\n"
            "- experience: list of objects with {company, role, duration, responsibilities (list of strings)}\n"
            "- education: list of objects with {institution, degree, duration, percentage ,cgpa}\n"
            "- skillset: list of strings\n"
            "- pastOrganisations: list of strings\n"
            "- technicalSkills: list of strings\n"
            "- workExperience: list of strings\n"
            "- projects: list of objects with {title, description} if available, else null\n"
            "- location: list of objects with {firstline,city,pincode,district,state,country}\n"
            "- institutionTier: string value indicating the tier of the college or institution{eg: 'one','two','three'}\n"
            "- companyTier: string value indicating the tier of the company or organisation{eg: 'one','two','three'}\n"
            "\n"
            "Follow this format strictly. Output only valid JSON, and do not include any explanation or notes."
    )
        client = openai.OpenAI(api_key=openai.api_key)
        print("key called")
        response = client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {"role": "system", "content": "You are an expert in parsing resumes."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": data} 
            ]
        )
        print("response received")
        content = response.choices[0].message.content
        print("content received")
        with open(f"output_cv.json", "w", encoding="utf-8") as json_file:
            json_file.write(content)
        

r1 = ResumeParser()
text = r1.read_pdf_file("CVs/vicky_kumar.pdf")
r1.cvParser(text)
