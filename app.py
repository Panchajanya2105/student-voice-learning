from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

# Sample database (normally comes from real DB or CSV)
students = {
    "9876543210": {
        "grade": "6",
        "subjects": {
            "1": "Math",
            "2": "Science"
        },
        "chapters": {
            "1": "math_ch1.pdf",
            "2": "sci_ch1.pdf"
        }
    }
}

def pdf_to_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route("/get-student-info", methods=["GET"])
def get_student_info():
    phone = request.args.get("phone")
    return jsonify(students.get(phone, {}))

@app.route("/get-chapter", methods=["GET"])
def get_chapter():
    phone = request.args.get("phone")
    subject_no = request.args.get("subject")
    chapter_no = request.args.get("chapter")
    chapter_file = students[phone]["chapters"].get(chapter_no)
    text = pdf_to_text(f"./pdfs/{chapter_file}")
    return jsonify({"text": text[:1000000]})  # Limit output length

app.run(host="0.0.0.0", port=5000)
