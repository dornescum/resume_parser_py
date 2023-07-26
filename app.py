from flask import Flask, render_template, request
import spacy
import re
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
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

        # verificare selectare
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

    # trec prin text
    resume_text = resume_text.strip()
    resume_text = resume_text.lower()

    # folosesc spaCy
    doc = nlp(resume_text)
    name = ""
    email = ""
    skills = []
    skill_patterns = [
        "java", "c++", "html5", "css3", "scss", "less", "sass", "bootstrap 4", "tailwind css",
        "javascript", "typescript", "react js", "angular", "vue.js", "ember.js", "backbone.js",
        "node.js", "express.js", "meteor.js", "next.js", "styled components", "redux",
        "jest", "mocha", "cypress", "selenium", "postman", "swagger",
        "django", "flask", "fastapi", "rails", "sinatra", "laravel", "codeigniter",
        "mongodb", "mysql", "postgresql", "sqlite", "oracle", "sql server",
        "git", "svn", "mercurial", "docker", "kubernetes", "aws", "azure", "google cloud",
        "jenkins", "travis ci", "circleci", "github actions",
        "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy", "opencv",
        "webpack", "babel", "gulp", "grunt", "rollup",
        "storybook", "storybook", "storybook", "storybook", "storybook",
        "karma", "jasmine", "chai", "enzyme", "react testing library", "testing library",
        "webpack", "babel", "gulp", "grunt", "rollup",
        "firebase", "auth0", "oauth", "jwt",
        "rest api", "graphql", "soap",
        "docker", "kubernetes", "aws", "azure", "google cloud",
        "jenkins", "travis ci", "circleci", "github actions",
        "unity", "unreal engine", "cocos2d", "godot",
        "photoshop", "illustrator", "sketch", "figma", "zeplin",
        "agile", "scrum", "kanban", "lean",
        "data analysis", "data visualization", "data engineering", "data science",
        "machine learning", "deep learning", "artificial intelligence",
        "blockchain", "smart contracts", "ethereum", "solidity",
        "iot", "arduino", "raspberry pi", "esp8266", "esp32"
    ]

    # cauta in prima rand
    lines = resume_text.split("\n")
    if lines:
        name = lines[0].strip()

    # cauta nume
    for ent in doc.ents:
        if "name" in ent.text.lower() and not name:
            name = ent.text.strip()

    for pattern in skill_patterns:
        if pattern in resume_text:
            skills.append(pattern)

    # Use regular expression to find email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email_match = re.search(email_pattern, resume_text)
    if email_match:
        email = email_match.group()

    parsed_result = {
        "Name": name,
        "Email": email,
        "Skills": skills
    }

    return parsed_result


if __name__ == "__main__":
    app.run(debug=True)
