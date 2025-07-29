import os
import pandas as pd
import numpy as np
import re
from flask import Flask, render_template, request, redirect, url_for
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

    # Create the uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # --- Gemini AI Configuration ---
    # Replace with your actual API key
    # Access environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    print(f"API Key: {GEMINI_API_KEY}")

    genai.configure(api_key=GEMINI_API_KEY)


def gemini_text_to_docx(text_from_gemini, output_filename="proposal.docx"):
    """
    Converts a string with Markdown formatting (## for headings, ** for bold)
    into a formatted Word document.

    Args:
        text_from_gemini (str): The multiline string from the AI.
        output_filename (str): The name of the Word file to create.
    """
    document = Document()
    
    # Split the input text into individual lines for processing
    lines = text_from_gemini.strip().split('\n')

    for line in lines:
        # Handle Headings: Check if the line starts with '## '
        if line.startswith('## '):
            # Remove the '## ' marker and add as a level 2 heading
            heading_text = line.lstrip('## ').strip()
            document.add_heading(heading_text, level=2)
            continue # Move to the next line

        # Handle other heading levels if needed
        if line.startswith('# '):
            heading_text = line.lstrip('# ').strip()
            document.add_heading(heading_text, level=1)
            continue
            
        # Handle Paragraphs with potential bold text
        # Create a new paragraph for the line
        p = document.add_paragraph()
        
        # Split the line by the bold marker '**'
        # This will create a list of parts. Parts at odd indices were inside **
        # Example: "This is **bold** text" -> ['This is ', 'bold', ' text']
        parts = line.split('**')
        
        for i, part in enumerate(parts):
            if part: # Ensure the part is not an empty string
                # If the index is odd, the text was between ** markers, so make it bold
                if i % 2 == 1:
                    run = p.add_run(part)
                    run.bold = True
                # Otherwise, add it as normal text
                else:
                    p.add_run(part)

    # Save the document
    document.save(output_filename)
    print(f"Document '{output_filename}' created successfully.")

def generate_proposal_from_row(a="N/A", b="N/A", c="N/A", d="N/A", e="N/A", f="N/A", g="N/A"):
    """Generates a proposal for a single row of data."""
 
     #model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Create a detailed prompt for the Gemini model
    prompt = f"""
    **Generate a professional and comprehensive project proposal based on the following details:**

    - **Client Name:** {a}
    - **Project Title:** {a}
    - **Project Description:** {a}
    - **Scope of Work:** {a}
    - **Timeline:** {a}
    - **Budget:** {a}

    **The proposal should be well-structured and include the following sections:**
    1.  **Introduction:** A compelling opening that introduces our company and the project.
    2.  **Understanding of Client Needs:** Show that we have a clear grasp of the client's goals.
    3.  **Proposed Solution:** A detailed description of the solution we are offering.
    4.  **Detailed Scope of Work:** A clear and itemized list of all deliverables.
    5.  **Project Timeline:** A realistic timeline with key milestones.
    6.  **Investment & Budget:** A breakdown of the costs.
    7.  **Call to Action:** A clear next step for the client.

    **Please write the proposal in a professional and persuasive tone.**
    """
    print(f"Prompt: {prompt}")
    try:
        
        print("Generating proposal using Gemini model...")
        response = model.generate_content(prompt)
        #document = Document()
        #document.add_heading('Futuristic City', level=1)
        #document.add_paragraph(response.text)
        #document.save('futuristic_city_story.docx')

        #print("Word document 'futuristic_city_story.docx' generated successfully.")
        #gemini_text_to_docx(response.text, output_filename="uploads/proposal.docx")
            # Create an instance of the converter
        converter = MarkdownToDocxConverter()
        # Convert the markdown string to a docx file
        converter.convert(response.text, 'uploads/proposal.docx')


        return response.text
    except Exception as e:
        return f"An error occurred while generating the proposal: {e}"
    

def get_school_data():
    SCHOOL_WEEKS_PER_YEAR = 365/180
    STUDENTS_PER_CLASS = 10

    """Reads and processes the school data from the CSV."""
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()

    # Create a clean, unformatted 'Cost Proposal' for calculations and default input value
    df['cost_proposal_raw'] = np.where(
        df['Meal Program Participants'] > 0,
        df['Estimated Funding (USD)'] / df['Meal Program Participants'] / SCHOOL_WEEKS_PER_YEAR,
        0
    )
    # Also create a formatted version for the initial JSON data
    df['Cost Proposal'] = df['cost_proposal_raw'].map('${:,.2f}'.format)

    # Keep a raw funding value for the proposal page
    df['raw_funding'] = df['Estimated Funding (USD)']

    # Format other columns for display on the main page
    if 'FRPM Percent (%)' in df.columns:
        df['FRPM Percent (%)'] = (df['FRPM Percent (%)'] * 100).map('{:.2f}%'.format)
    if 'Estimated Funding (USD)' in df.columns:
        df['Estimated Funding (USD)'] = df['Estimated Funding (USD)'].map('${:,.2f}'.format)
    
    return df

@app.route('/')
def index():
    """Displays the main page with filters and the interactive table."""
    df = get_school_data()
    districts = df['District Name'].unique().tolist()
    all_data_json = df.to_json(orient='records')
    return render_template('index.html', districts=districts, all_data=all_data_json)

@app.route('/proposal', methods=['POST'])
def generate_proposal():
    """Generates the proposal page based on submitted form data."""
    # Retrieve all the data submitted from the hidden form fields
    proposal_data = {
        'school_name': request.form.get('school_name'),
        'district_name': request.form.get('district_name'),
        'school_type': request.form.get('school_type'),
        'total_enrollment': request.form.get('total_enrollment'),
        'meal_participants': request.form.get('meal_program_participants'),
        'frpm_percent': request.form.get('frpm_percent'),
        'after_school_program': request.form.get('after_school_education_program'),
        'estimated_funding': request.form.get('estimated_funding_usd'),
        # Get the potentially edited cost proposal value from its input field
        'cost_proposal': request.form.get('cost_proposal') 
    }
    generate_proposal_from_row(request.form.get('district_name'))
    return render_template('proposal.html', data=proposal_data)

if __name__ == '__main__':
    _initialize()
    # Use the port number that works for you
    app.run(port=5001, debug=True)