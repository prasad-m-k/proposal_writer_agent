import os
import pandas as pd
import numpy as np
import re
import markdown
import pdfkit
import time # Added for unique filenames
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai
from docx import Document
from convert import MarkdownToDocxConverter

app = Flask(__name__)

def _initialize():
    load_dotenv()
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)

def generate_proposal_from_row(district="N/A", cost_proposal="N/A"):
    """
    Generates a proposal, saves it as a .docx file with a unique name,
    and returns the AI text and the filename.
    """
    model = genai.GenerativeModel('gemini-1.5-flash') # Updated model

    prompt = f"""
    **Generate a professional Executive Summary:**

    - **Musical Instruments N Kids Hands (M.I.N.K.H.) / Music Science Group (MSG) :** is presenting to {district}

    **The proposal summary should be well-structured and include the following sections:**
    1.  **Close the Opportunity Gap:** 
    2.  **Cultivate 21st-Century Skills:** 
    3.  **Foster Social-Emotional Resilience:** 
    4.  **Improve academic performance:** 
  
    **Please write the proposal executive summary in a professional and persuasive tone. Highlight (MSG) rather than (M.I.N.K.H.) in the summary.**
    """
    
    try:
        print("Generating proposal using Gemini model...")
        response = model.generate_content(prompt)
        content=""
        with open('uploads/proposal.txt', 'r') as file:
            content = file.read()
            print(content)

        content = content.replace("district_name", district)
        content = content.replace("executive_summary", response.text)
        proposal_text = content
        
        # Create a unique filename to prevent overwrites
        safe_district_name = re.sub(r'[^a-zA-Z0-9_]', '', district).replace(" ", "_")
        timestamp = int(time.time())
        filename = f"Proposal_{safe_district_name}_{timestamp}.docx"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Create an instance of the converter and generate the docx
        converter = MarkdownToDocxConverter()
        converter.convert(proposal_text, output_path)

        #html_text = markdown.markdown(proposal_text)

        # Step 3: Convert HTML to PDF
        #pdfkit.from_string(html_text, "uploads/output.pdf")

        # Return both the generated text and the filename
        return proposal_text, filename
    except Exception as e:
        error_text = f"An error occurred while generating the proposal: {e}"
        return error_text, None

def get_school_data():
    SCHOOL_WEEKS_PER_YEAR = 365 / 180
    STUDENTS_PER_CLASS = 10
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()
    df['cost_proposal_raw'] = np.where(
        df['Meal Program Participants'] > 0,
        df['Estimated Funding (USD)'] / df['Meal Program Participants'] / SCHOOL_WEEKS_PER_YEAR,
        0
    )
    df['Cost Proposal'] = df['cost_proposal_raw'].map('${:,.2f}'.format)
    df['raw_funding'] = df['Estimated Funding (USD)']
    if 'FRPM Percent (%)' in df.columns:
        df['FRPM Percent (%)'] = (df['FRPM Percent (%)'] * 100).map('{:.2f}%'.format)
    if 'Estimated Funding (USD)' in df.columns:
        df['Estimated Funding (USD)'] = df['Estimated Funding (USD)'].map('${:,.2f}'.format)
    return df

@app.route('/')
def index():
    df = get_school_data()
    districts = df['District Name'].unique().tolist()
    all_data_json = df.to_json(orient='records')
    return render_template('index.html', districts=districts, all_data=all_data_json)

@app.route('/proposal', methods=['POST'])
def generate_proposal():
    """
    Generates the proposal and renders a page with the AI text and a download link.
    """
    # Use the correct key 'district' from the form submission in index.html
    district_name = request.form.get('district')
    cost_proposal = request.form.get('cost_proposal')

    # Generate the proposal text and the .docx file
    proposal_text, filename = generate_proposal_from_row(district_name, cost_proposal)

    # Prepare all data to be passed to the template
    proposal_data = {
        'district': district_name,
        'cost_proposal': cost_proposal,
        'school_name': request.form.get('schoolname'), # Make sure school name is passed
        'proposal_text': proposal_text,
        'filename': filename # Pass the filename for the download button
    }

    return render_template('proposal.html', data=proposal_data)

# ADDED: New route to handle file downloads securely
@app.route('/download/<path:filename>')
def download_file(filename):
    """Serves files from the 'uploads' directory."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    _initialize()
    app.run(port=5001, debug=True)