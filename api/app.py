from flask import Flask, render_template, request, redirect, url_for
from resume_analysis import analyze_resume
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Upload & Analyze
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('home'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    analysis_result = analyze_resume(filepath)

    return render_template('results.html', result=analysis_result)

import os

def handler(event, context):
    os.system("gunicorn -w 4 -b 0.0.0.0:8000 api.app:app")

