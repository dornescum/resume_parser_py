from flask import Flask, render_template, request
import spacy
import re
import pdfminer
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
import os
import tempfile
from io import BytesIO

app = Flask(__name__)

# Load the English language model
nlp = spacy.load("en_core_web_sm")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if "resume_file" not in request.files:
            return "No file part!"

        resume_file = request.files["resume_file"]

        # Check if a file was selected
        if resume_file.filename == "":
            return "No selected file!"

        # Read the content of the file as bytes
        resume_bytes = resume_file.read()

        try:
            parsed_resume = parse_resume(resume_bytes)
        except (PDFSyntaxError, PDFTextExtractionNotAllowed):
            return "Invalid PDF file! Please upload a valid PDF file."

        return render_template("result.html", parsed_resume=parsed_resume)

    return render_template("index.html")


def parse_resume(resume_bytes):
    try:
        resume_text = extract_text(BytesIO(resume_bytes))
    except (PDFSyntaxError, PDFTextExtractionNotAllowed):
        raise PDFSyntaxError("Invalid PDF file! Please upload a valid PDF file.")

    # Preprocess the text
    resume_text = resume_text.strip()
    resume_text = resume_text.lower()

    # Process the resume text with spaCy
    doc = nlp(resume_text)
    # print('doc :', doc)
    # Initialize variables to store the extracted entities
    name = ""
    email = ""
    skills = []
    skill_patterns = ["java", "c++", "html5", "css3", "scss", "bootstrap 4", "tailwind css",
                      "javascript", "react js", "next js", "styled components", "jest test framework", "cypress",
                      "postman",
                      "angular", "ionic", "sqlite", "node js (express)", "mysql"]
    test = []

    # Entity Recognition for Name and Email
    for ent in doc.ents:
        print('ent2: ', ent.text)
        print('ent3: ', ent)
        # if ent.label_ == "Name" and not name:
        #     name = ent.text
        # elif ent.label_ == "email" and not email:
        #     email = ent.text
        # elif ent.label_ == "skills" and not skills:
        #     print('ent label', ent.label_)
        #     test.append(ent.text)
        if "name" in ent.text.lower() and not name:
            name = ent.text.strip()
            print('name', name)
        elif "email" in ent.text.lower() and not email:
            email = ent.text.strip()
            print('email : ', email)

    for pattern in skill_patterns:
        if pattern in resume_text:
            skills.append(pattern)
        # for pattern in skill_patterns:
        #     if pattern in ent.text:
        #         print('patern : ', pattern)
        #         skills.append(pattern)
    # print('name : ', name)
    # print('email : ', email)

    # Prepare the results as a dictionary
    parsed_result = {
        "Name": name,
        "Email": email,
        "Skills": skills
    }
    return parsed_result


if __name__ == "__main__":
    app.run(debug=True)
