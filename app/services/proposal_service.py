"""
Proposal Generation Service Module
"""
import os
import re
import time
import pandas as pd
from datetime import date
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import google.generativeai as genai

from convert import MarkdownToDocxConverter
from config.settings import RFP_TYPE_FILES
import word_formatter


class ProposalService:
    """Service class for handling proposal generation"""
    
    def __init__(self, app_config):
        self.config = app_config
        self._configure_genai()
    
    def _configure_genai(self):
        """Configure Google Generative AI"""
        api_key = self.config.get('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
    
    def load_rfp_files(self, rfp_type):
        """Load the appropriate prompt and requirements files based on RFP type."""
        if rfp_type not in RFP_TYPE_FILES:
            rfp_type = "Extended Learning Opportunities Program"  # Default fallback
        
        files = RFP_TYPE_FILES[rfp_type]
        
        try:
            # Load prompt file
            prompt_path = os.path.join(self.config['INPUT_FILES_FOLDER'], files["prompt"])
            with open(prompt_path, 'r', encoding='utf-8') as f:
                print(f"reading from prompt_path: {prompt_path} ")
                prompt_template = f.read()
            
            # Load requirements file
            requirements_path = os.path.join(self.config['INPUT_FILES_FOLDER'], files["requirements"])
            with open(requirements_path, 'r', encoding='utf-8') as f:
                print(f"reading from requirements_path: {requirements_path} ")
                requirements_context = f.read()
                
            return prompt_template, requirements_context
            
        except FileNotFoundError as e:
            print(f"Warning: Could not load RFP files for {rfp_type}: {e}")
            # Fallback to default files
            try:
                with open(os.path.join(self.config['INPUT_FILES_FOLDER'], 'proposal_prompt.txt'), 'r', encoding='utf-8') as f:
                    prompt_template = f.read()
                with open(os.path.join(self.config['INPUT_FILES_FOLDER'], 'natomas_school_district_rfp_requirements.txt'), 'r', encoding='utf-8') as f:
                    requirements_context = f.read()
                return prompt_template, requirements_context
            except FileNotFoundError:
                raise ValueError(f"Could not load default prompt files for RFP type: {rfp_type}")
    
    def load_context_files(self):
        """Load common context files"""
        context_files = {}
        
        try:
            with open(os.path.join(self.config['INPUT_FILES_FOLDER'], 'district.csv'), 'r', encoding='utf-8') as f:
                context_files['all_districts_info'] = f.read()

            with open(os.path.join(self.config['INPUT_FILES_FOLDER'], 'about_mstg.txt'), 'r', encoding='utf-8') as f:
                context_files['about_mstg'] = f.read()

            with open(os.path.join(self.config['INPUT_FILES_FOLDER'], 'about_minkh.txt'), 'r', encoding='utf-8') as f:
                context_files['about_minkh'] = f.read()
                
        except FileNotFoundError as e:
            print(f"Warning: Could not load context file: {e}")
            
        return context_files
    
    def create_document_header(self, document):
        """Add a pre-defined header to the document"""
        LOGO_PATH = 'static/assets/msg_logo.png'
        ADDRESS_LINES = [
            ("Musical Instruments N Kids Hands", True, 8),
            ("Music Science & Technology Group", True, 8),
            ("2150 Capitol Avenue Sacramento, CA 95816", False, 8),
            ("Ph. (916) 670-9950", False, 8)
        ]

        section = document.sections[0]
        header = section.header
        header.is_linked_to_previous = False
        header.paragraphs[0].text = ""

        header_table = header.add_table(rows=1, cols=2, width=Inches(6.5))
        header_table.autofit = False
        header_table.columns[0].width = Inches(1.5)
        header_table.columns[1].width = Inches(5.0)

        logo_cell = header_table.cell(0, 0)
        logo_paragraph = logo_cell.paragraphs[0]
        logo_run = logo_paragraph.add_run()
        
        if os.path.exists(LOGO_PATH):
            logo_run.add_picture(LOGO_PATH, height=Inches(0.75))

        address_cell = header_table.cell(0, 1)
        address_paragraph = address_cell.paragraphs[0]
        address_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        for text, is_bold, font_size in ADDRESS_LINES:
            run = address_paragraph.add_run(text + '\n')
            run.bold = is_bold
            font = run.font
            font.size = Pt(font_size)
    
    def normalize_empty_lines(self, text):
        """Reduce any sequence of multiple newlines to single newlines"""
        return re.sub(r'\n{2,}', r'\n', text)
    
    def clean_and_format_currency(self, value, default="$0.00"):
        """Clean and format currency values"""
        try:
            # Handle empty or None values
            if not value or str(value).strip() == '':
                return default

            clean_value = re.sub(r'[^\d.-]', '', str(value))  # Allow negative sign

            if not clean_value or clean_value == '.':
                return default

            numeric_value = float(clean_value)

            # Use locale-independent formatting
            formatted_result = "${:,.2f}".format(numeric_value)
            return formatted_result
        except (ValueError, TypeError) as e:
            print(f"Warning: Invalid currency value received: {value}. Error: {e}. Defaulting to {default}.")
            return default
    
    def prepare_prompt_variables(self, **kwargs):
        """Prepare variables for the prompt template"""
        # Load context files
        context_files = self.load_context_files()
        
        # Clean and format financial values
        formatted_cost_proposal = self.clean_and_format_currency(kwargs.get('cost_proposal'))

        # Calculate actual cost per student based on fixed program structure
        # Program: 439 students, 7 weeks, $75,000 total cost
        ##program_total_cost = 75000.00
        ##total_students = 439
        ##actual_cost_per_student = program_total_cost / total_students if total_students > 0 else 0

        # Use calculated value or form value, prefer calculated
        cost_per_student_value = kwargs.get('cost_per_student')
        if cost_per_student_value and float(str(cost_per_student_value).replace('$', '').replace(',', '')) > 0:
            formatted_cost_per_student = self.clean_and_format_currency(cost_per_student_value)
        else:
            formatted_cost_per_student = self.clean_and_format_currency("0")

        formatted_daily_cost = self.clean_and_format_currency(kwargs.get('daily_cost'))
        formatted_weekly_cost = self.clean_and_format_currency(kwargs.get('weekly_cost'))

        # Debug output
        print(f"DEBUG: cost_per_student from form: {kwargs.get('cost_per_student')}")
        print(f"DEBUG: formatted_cost_per_student: {formatted_cost_per_student}")
        print(f"DEBUG: daily_cost from form: {kwargs.get('daily_cost')}")
        print(f"DEBUG: weekly_cost from form: {kwargs.get('weekly_cost')}")
        print(f"DEBUG: cost_per_school from form: {kwargs.get('cost_per_school')}")
        print(f"DEBUG: cost_proposal from form: {kwargs.get('cost_proposal')}")
        
        # Prepare school locations
        selected_schools = kwargs.get('selected_schools', [])
        school_locations = ", ".join(selected_schools) if selected_schools else "Selected school sites"

        # Parse selected schools list if available
        selected_schools_list = kwargs.get('selected_schools_list')
        if selected_schools_list:
            try:
                import json
                parsed_schools = json.loads(selected_schools_list)
                school_locations = ", ".join(parsed_schools) if parsed_schools else school_locations
            except (json.JSONDecodeError, TypeError):
                # Fallback to the original list
                pass

        # Format cost per school
        formatted_cost_per_school = self.clean_and_format_currency(kwargs.get('cost_per_school'))

        # Format program start date
        program_start_date = kwargs.get('program_start_date')
        if program_start_date:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(program_start_date, '%Y-%m-%d')
                formatted_start_date = date_obj.strftime('%B %d, %Y')  # e.g., "October 07, 2024"

                # Calculate end date (assuming 7 weeks)
                from datetime import timedelta
                end_date_obj = date_obj + timedelta(weeks=7)
                formatted_end_date = end_date_obj.strftime('%B %d, %Y')
                program_dates = f"{formatted_start_date} - {formatted_end_date}"
            except (ValueError, TypeError):
                program_dates = "January 13, 2025 - March 07, 2025"
        else:
            program_dates = "January 13, 2025 - March 07, 2025"
        
        # Format RFP instructions
        district = kwargs.get('district', 'N/A')
        rfp_type = kwargs.get('rfp_type', 'Extended Learning Opportunities Program')
        
        if rfp_type != "Extended Learning Opportunities Program":
            rfp_instruction_formatted = (
                f"\nWhen generating the proposal for {district}, it is crucial to explicitly address and demonstrate compliance with each of the listed RFP requirements for {rfp_type}, integrating them naturally into the relevant sections of the proposal."
            )
        else:
            rfp_instruction_formatted = ""
            if district == "Natomas Unified School District":
                rfp_instruction_formatted = (
                    "\nWhen generating the proposal for Natomas Unified School District, it is crucial to explicitly address and demonstrate compliance with each of the listed RFP requirements, integrating them naturally into the relevant sections of the proposal."
                )
        
        # Create comprehensive variables dictionary
        prompt_variables = {
            'district': district,
            'rfp_type': rfp_type,
            'today': date.today(),
            'days_per_week': kwargs.get('days_per_week', 'N/A'),
            'num_weeks': kwargs.get('num_weeks', 'N/A'),
            'hours_per_day': kwargs.get('hours_per_day', '3'),
            'school_locations': school_locations,
            'formatted_cost_proposal': formatted_cost_proposal,
            'formatted_daily_cost': formatted_daily_cost,
            'formatted_weekly_cost': formatted_weekly_cost,
            'total_students': kwargs.get('total_students', 'N/A'),
            'formatted_cost_per_student': formatted_cost_per_student,
            'formatted_cost_per_school': formatted_cost_per_school,
            'program_dates': program_dates,
            'year': date.today().year,
            'rfp_instruction_formatted': rfp_instruction_formatted,
            'client': f"{district} School District",
            'project': {rfp_type},
            'services': "Music Integration, S.T.E.A.M. Education, Wellness Programs, Student Engagement Activities",
            'benefits': "Enhanced Student Engagement, Improved Academic Performance, Increased Wellness, Community Involvement",
            'cta': "We look forward to the opportunity to collaborate and make a meaningful impact together."
        }
        
        # Add context files
        prompt_variables.update(context_files)
        
        # Add RFP requirements context
        _, requirements_context = self.load_rfp_files(rfp_type)
        prompt_variables['rfp_requirements_context_formatted'] = requirements_context
        
        # For backward compatibility
        prompt_variables.update({
            'natomas_rfp_requirements_context_formatted': requirements_context,
            'natomas_rfp_instruction_formatted': rfp_instruction_formatted
        })

        return prompt_variables
    
    def generate_proposal_text(self, prompt_template, prompt_variables):
        """Generate proposal text using AI"""
        try:
            prompt = prompt_template.format(**prompt_variables)
            model = genai.GenerativeModel('gemini-2.0-flash')

            print(f"Generating proposal using Gemini model for RFP type: {prompt_variables.get('rfp_type')}...")
            response = model.generate_content(prompt)
            return self.normalize_empty_lines(response.text)

        except Exception as e:
            error_text = f"An error occurred while generating the proposal text: {e}"
            print(error_text)
            return error_text
    
    def create_document(self, text, district, rfp_type):
        """Create and save the Word document"""
        try:
            document = Document()
            self.create_document_header(document)

            # Convert text to document
            converter = MarkdownToDocxConverter(document=document)
            text = text.replace('** ', '**').replace(' **', '**')
            converter.convert(text)

            # Generate filename
            safe_district_name = re.sub(r'[^a-zA-Z0-9_]', '', district).replace(" ", "_")
            safe_rfp_type = re.sub(r'[^a-zA-Z0-9_]', '', rfp_type).replace(" ", "_")
            timestamp = int(time.time())
            filename = f"Proposal_{safe_district_name}_{safe_rfp_type}_{timestamp}.docx"
            
            output_path = os.path.join(self.config['DOWNLOAD_FOLDER'], filename)
            document.save(output_path)

            # Format the document
            word_formatter.format_word_document(output_path, output_path)

            print(f"Successfully created '{filename}' in '{self.config['DOWNLOAD_FOLDER']}' with custom header.")

            return filename
            
        except Exception as e:
            print(f"Error creating document: {e}")
            return None
    
    def manage_file_rotation(self, district_name, max_files=5):
        """Manage file rotation to keep only recent files"""
        safe_district_name = re.sub(r'[^a-zA-Z0-9_]', '', district_name).replace(" ", "_")
        
        file_pattern = rf"Proposal_{re.escape(safe_district_name)}_.*_(\d+)\.docx"
        
        district_files = []
        download_folder = self.config['DOWNLOAD_FOLDER']
        
        for filename in os.listdir(download_folder):
            match = re.match(file_pattern, filename)
            if match:
                timestamp = int(match.group(1))
                district_files.append((timestamp, os.path.join(download_folder, filename)))
                
        # Sort files by timestamp, oldest first
        district_files.sort(key=lambda x: x[0])

        # Delete old files if we have more than max_files
        if len(district_files) > max_files:
            files_to_delete = district_files[:len(district_files) - max_files]
            for _, filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"Deleted old proposal file: {filepath}")
                except OSError as e:
                    print(f"Error deleting file {filepath}: {e}")
    
    def generate_proposal_text_only(self, **kwargs):
        """Generate only the proposal text without creating a document"""
        try:
            # Load appropriate files based on RFP type
            rfp_type = kwargs.get('rfp_type', 'Extended Learning Opportunities Program')
            prompt_template, _ = self.load_rfp_files(rfp_type)

            # Prepare variables
            prompt_variables = self.prepare_prompt_variables(**kwargs)

            # Generate proposal text
            proposal_text = self.generate_proposal_text(prompt_template, prompt_variables)

            return proposal_text

        except Exception as e:
            error_text = f"An error occurred while generating the proposal text: {e}"
            print(error_text)
            return error_text

    def generate_proposal(self, **kwargs):
        """Main method to generate a complete proposal"""
        try:
            # Load appropriate files based on RFP type
            rfp_type = kwargs.get('rfp_type', 'Extended Learning Opportunities Program')
            prompt_template, _ = self.load_rfp_files(rfp_type)

            # Prepare variables
            prompt_variables = self.prepare_prompt_variables(**kwargs)

            # Generate proposal text
            proposal_text = self.generate_proposal_text(prompt_template, prompt_variables)

            # Create document
            district = kwargs.get('district', 'N/A')
            filename = self.create_document(proposal_text, district, rfp_type)

            # Manage file rotation
            if filename:
                self.manage_file_rotation(district)

            return proposal_text, filename

        except Exception as e:
            error_text = f"An error occurred while generating the proposal: {e}"
            print(error_text)
            return error_text, None


class DataService:
    """Service class for handling data operations"""
    
    def __init__(self, app_config):
        self.config = app_config
    
    def get_school_data(self):
        """Read and return school data from CSV"""
        try:
            df = pd.read_csv(os.path.join(self.config['INPUT_FILES_FOLDER'], "data.csv"))
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            print(f"Error loading school data: {e}")
            return pd.DataFrame()
    
    def get_districts(self):
        """Get list of unique districts"""
        df = self.get_school_data()
        return df['District Name'].unique().tolist() if not df.empty else []
