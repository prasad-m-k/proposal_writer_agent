# app.py

import os
import pandas as pd
import numpy as np
import re
import time
from flask import Flask, render_template, request, url_for, send_from_directory
from dotenv import load_dotenv
import google.generativeai as genai
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from convert import MarkdownToDocxConverter # Your updated converter

app = Flask(__name__)
env = {}

def _initialize():
    global env
    load_dotenv()
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEPL=os.getenv("DEPL")
    genai.configure(api_key=GEMINI_API_KEY)

def create_document_header(document):
    """
    Adds a pre-defined, crisp header with a smaller font to a document object.

    Args:
        document: The python-docx document object.
    """
    # --- Configuration ---
    # Make sure the logo is in your static/assets folder
    LOGO_PATH = 'static/assets/msg_logo.png'
    ADDRESS_LINES = [
        ("Musical Instruments N Kids Hands", True, 10),  # (Text, Is_Bold, Font_Size)
        ("Music Science Group", True, 10),
        ("2150 Capitol Avenue Sacramento, CA 95816", False, 8),
        ("Ph. (916) 670-9950", False, 8)
    ]

    section = document.sections[0]
    header = section.header
    # Clear any existing content in the header
    header.is_linked_to_previous = False
    header.paragraphs[0].text = ""

    header_table = header.add_table(rows=1, cols=2, width=Inches(6.5))
    header_table.autofit = False
    header_table.columns[0].width = Inches(1.5)
    header_table.columns[1].width = Inches(5.0)

    # --- Left Column: Logo ---
    logo_cell = header_table.cell(0, 0)
    logo_paragraph = logo_cell.paragraphs[0]
    logo_run = logo_paragraph.add_run()
    logo_run.add_picture(LOGO_PATH, height=Inches(0.75)) # Slightly adjusted for proportion

    # --- Right Column: Address ---
    address_cell = header_table.cell(0, 1)
    # It's better to add a new paragraph to have full control over its properties
    address_paragraph = address_cell.paragraphs[0]
    address_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for text, is_bold, font_size in ADDRESS_LINES:
        run = address_paragraph.add_run(text + '\n') # Using '\n' for line break
        run.bold = is_bold
        font = run.font
        font.size = Pt(font_size)

def generate_proposal_from_row(district="N/A", cost_proposal="N/A"):
    """
    Generates a proposal with a custom header, saves it as a .docx file,
    and returns the AI text and the filename.
    """
    try:
        all_districts_info=""
        with open('uploads/district.csv', 'r') as f:
            all_districts_info = f.read()
            print(all_districts_info)

        about=""
        with open('uploads/about_msg.txt', 'r') as f:
            about_msg = f.read()
            print(about_msg)

        proposal_context = ""
        # Make sure this template file exists in your 'uploads' folder or change path
        with open('uploads/proposal.txt', 'r') as file:
            proposal_context = file.read()

            #content = content.replace("district_name", district)
            #content = content.replace("executive_summary", response.text)
            proposal_text = proposal_context

        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        **Generate a professional Proposal Document to school district selected with today's date:**
        - **Musical Instruments N Kids Hands (M.I.N.K.H.) / Music Science Group (MSG) :** is sending proposal to {district}
        - Use the following guidelines to create a compelling executive summary for the proposal to {district}.
        - Use today's date as the proposal date.
      
        Use the {all_districts_info} to fetch the school district specific data for {district}, like address and contact person.
        - **Incorporate the provided cost proposal:** {cost_proposal} based on number schools in the district.

        The context about MSG is as follows: {about_msg}
        - **Tone and Style:** Ensure the summary is formal, persuasive, and tailored to educational stakeholders.
        - **some more context and outlines are here too: {proposal_text}

        **The proposal should be well-structured... **
        """
    

        print("Generating proposal using Gemini model...")
        response = model.generate_content(prompt)
        
         
        # 1. Create a new document object
        document = Document()
        
        # 2. Add the custom header to it
        create_document_header(document)

        # 3. Initialize the converter WITH the document that now has a header
        converter = MarkdownToDocxConverter(document=document)
        
        # 4. Add the body content from the AI to the document
        converter.convert(proposal_text)

        # 5. Save the final document
        safe_district_name = re.sub(r'[^a-zA-Z0-9_]', '', district).replace(" ", "_")
        timestamp = int(time.time())
        filename = f"Proposal_{safe_district_name}_{timestamp}.docx"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        document.save(output_path)
        print(f"Successfully created '{filename}' with custom header.")

        return proposal_text, filename
    except Exception as e:
        error_text = f"An error occurred while generating the proposal: {e}"
        return error_text, None

# ... (get_school_data, index, generate_proposal, and download_file routes remain unchanged) ...
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
    district_name = request.form.get('district')
    cost_proposal = request.form.get('cost_proposal')

    proposal_text, filename = generate_proposal_from_row(district_name, cost_proposal)

    proposal_data = {
        'district': district_name,
        'cost_proposal': cost_proposal,
        'school_name': request.form.get('schoolname'),
        'proposal_text': proposal_text,
        'filename': filename
    }
    return render_template('proposal.html', data=proposal_data)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    _initialize()
    if os.getenv("DEPL") == "PROD":
        #app.run(host='0.0.0.0', port=443, debug=True)
        app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('/etc/letsencrypt/live/qaproposalmusicsciencegroup.com/fullchain.pem',
                                               '/etc/letsencrypt/live/qaproposalmusicsciencegroup.com/privkey.pem'))
    else:
        app.run(port=5001, debug=True)

