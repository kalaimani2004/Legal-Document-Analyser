from flask import Flask, render_template, request
from flask_cors import CORS
from summarizer import summarize_document
from agentic_chatbot import agentic_legal_chatbot as legal_chatbot
from estimator import estimate_cost

import PyPDF2
import docx

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    summary = ''
    if request.method == 'POST':
        file = request.files['document']
        if file:
            filename = file.filename.lower()
            if filename.endswith('.pdf'):
                from io import BytesIO
                from PyPDF2 import PdfReader
                reader = PdfReader(BytesIO(file.read()))
                document = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif filename.endswith(('.doc', '.docx')):
                import docx
                doc = docx.Document(file)
                document = "\n".join([para.text for para in doc.paragraphs])
            else:
                return render_template('summarizer.html', summary="Unsupported file format.")
            
            summary = summarize_document(document)

    return render_template('summarizer.html', summary=summary)


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    response = ''
    if request.method == 'POST':
        question = request.form['question']
        response = legal_chatbot(question)
    return render_template('chatbot.html', response=response)

@app.route('/estimator', methods=['GET', 'POST'])
def estimator():
    result = ''
    if request.method == 'POST':
        case_type = request.form['case_type']
        court_level = request.form['court_level']
        result = estimate_cost(case_type, court_level)
    return render_template('estimator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5002)