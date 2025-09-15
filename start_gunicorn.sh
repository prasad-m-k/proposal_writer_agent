#!/bin/bash
# start_gunicorn.sh

# Activate the virtual environment
source /home/deepamk/proposal/proposal_writer_agent/venv/bin/activate


# Change to the project directory
cd /home/deepamk/proposal/proposal_writer_agent

# Set environment variables (e.g., for production deployment)
#export DEPL="PROD"
#export GEMINI_API_KEY="your_actual_gemini_api_key" # Or ensure it's in .env and loaded by load_dotenv()

source .env
# Start Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:5001 --access-logfile - --error-logfile - app:app
