import openai  
import fitz    
from docx import Document  

from secret_key import openai_key

openai.api_key = openai_key

class JDparser:
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

    # parses a JD into a json string
    def jdParser(self, data):
        prompt = (
            "You are a professional and consistent job description parser.\n"
            "Parse the following job description text and extract the following fields. Return the output strictly in JSON format with keys in camelCase.\n"
            "Ensure all keys are always present, even if the value is null, empty string, or an empty list.\n"
            "\n"
            "The output JSON should contain these keys:\n"
            "- jobTitle: string\n"
            "- jobCode: string\n"
            "- department: string\n"
            "- officeLocation: string\n"
            "- workplace: list of strings (e.g., ['On-site', 'Hybrid'])\n"
            "- showOnCareersPage: boolean\n"
            "- additionalLocations: list of strings\n"
            "- about: string (short overview)\n"
            "- describeTheJob: string (full job description)\n"
            "- requirements: list of strings\n"
            "- benefits: list of strings\n"
            "- industry: string\n"
            "- jobFunction: string\n"
            "- companyName: string\n"
            "- aboutCompany: string\n"
            "\n"
            "Follow this format strictly. Output only valid JSON, and do not include any explanation or notes.or anything except JSON string"
        )

        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in parsing Job descriptions."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": data} 
            ]
        )
        content = response.choices[0].message.content
        with open(f"output_JD.json", "w", encoding="utf-8") as json_file:
            json_file.write(content)

    # Generates JD just by job title by predicting default data        
    def jdCreator(self,title):
        prompt = (
            "You are a professional job description writer.\n"
            "Generate a detailed and structured job description for the role provided.\n"
            "The output should be in the following format and written clearly and professionally.\n"
            "\n"
            f"Input Role: {title}\n"
            "\n"
            "Output JSON format (use camelCase keys and make sure all keys are included):\n"
            "{\n"
            "  \"jobTitle\": string,\n"
            "  \"jobCode\": string,\n"
            "  \"about\": string (1-2 sentence summary),\n"
            "  \"describeTheJob\": string (detailed role and responsibilities),\n"
            "  \"requirements\": list of strings,\n"
            "  \"desired skills\" :list of strings\n"
            "  \"benefits\": list of strings,\n"
            "  \"industry\": string,\n"
            "  \"jobFunction\": string,\n"
            "  \"companyName\": string,\n"
            "  \"aboutCompany\": string\n"
            "}\n"
            "\n"
            "Only return valid JSON. Do not include any explanations, markdown, or headings. All fields must be present even if empty."
            "Do not include any markdown"
        )
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in creating Job descriptions."},
                {"role": "user", "content": prompt},
            ]
        )
        content = response.choices[0].message.content
        with open(f"output_JD.json", "w", encoding="utf-8") as json_file:
            json_file.write(content)

r1 = JDparser()
text = r1.read_pdf_file("JDs/jd.pdf")
r1.jdParser(text)
