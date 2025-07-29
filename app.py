from dotenv import load_dotenv
import os
import pandas as pd
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for

# Load environment variables from the .env file
load_dotenv()
# --- Basic Flask App Setup ---
app = Flask(__name__)
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
#model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_proposal_from_row(row):
    """Generates a proposal for a single row of data."""
    # Create a detailed prompt for the Gemini model
    prompt = f"""
    **Generate a professional and comprehensive project proposal based on the following details:**

    - **Client Name:** {row.get('client_name', 'N/A')}
    - **Project Title:** {row.get('project_title', 'N/A')}
    - **Project Description:** {row.get('project_description', 'N/A')}
    - **Scope of Work:** {row.get('scope_of_work', 'N/A')}
    - **Timeline:** {row.get('timeline', 'N/A')}
    - **Budget:** {row.get('budget', 'N/A')}

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
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the proposal: {e}"

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            # Save the uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process the CSV and generate proposals
            try:
                df = pd.read_csv(filepath)
                proposals = []
                for index, row in df.iterrows():
                    generated_text = generate_proposal_from_row(row)
                    proposals.append({
                        'client': row.get('client_name', f'Row {index + 1}'),
                        'proposal': generated_text
                    })

                # Clean up the uploaded file
                #os.remove(filepath)

                # Render the results page with the generated proposals
                return render_template('results.html', proposals=proposals)

            except Exception as e:
                # Clean up the file even if an error occurs
                if os.path.exists(filepath):
                    os.remove(filepath)
                return f"An error occurred while processing the file: {e}"

    # Render the main upload page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
