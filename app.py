import pandas as pd
from flask import Flask, render_template
import numpy as np # Import numpy to handle potential division by zero safely

app = Flask(__name__)

# --- DEFINE CONSTANTS ---
SCHOOL_DAYS_PER_YEAR = 3

@app.route('/')
def index():
    # Read the CSV file fresh on each request to ensure data is current
    df = pd.read_csv("data.csv")

    # Clean up column names by stripping any leading/trailing whitespace
    df.columns = df.columns.str.strip()

    # --- CALCULATION LOGIC (PERFORM ON RAW NUMBERS FIRST) ---
    # Calculate 'Cost Proposal' using our formula.
    # We use np.where to avoid division by zero errors if a school has 0 participants.
    df['Cost Proposal'] = np.where(
        df['Meal Program Participants'] > 0,
        df['Estimated Funding (USD)'] / df['Meal Program Participants'] / SCHOOL_DAYS_PER_YEAR,
        0  # If no participants, the cost per session is $0
    )

    # --- FORMATTING FOR DISPLAY (AFTER ALL CALCULATIONS ARE DONE) ---
    # Format the new 'Cost Proposal' column as currency
    df['Cost Proposal'] = df['Cost Proposal'].map('${:,.2f}'.format)
    
    # Format the other columns as before
    if 'FRPM Percent (%)' in df.columns:
        df['FRPM Percent (%)'] = (df['FRPM Percent (%)'] * 100).map('{:.2f}%'.format)
    if 'Estimated Funding (USD)' in df.columns:
        df['Estimated Funding (USD)'] = df['Estimated Funding (USD)'].map('${:,.2f}'.format)


    # --- PREPARE DATA FOR THE TEMPLATE ---
    # Get a list of unique district names for the first dropdown
    districts = df['District Name'].unique().tolist()

    # Convert the entire DataFrame (with the new column) to a JSON string
    all_data_json = df.to_json(orient='records')

    return render_template('index.html', districts=districts, all_data=all_data_json)

# Remember to use the port number that works for you
if __name__ == '__main__':
    app.run(port=5001, debug=True)
