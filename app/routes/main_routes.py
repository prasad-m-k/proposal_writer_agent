"""
Main application routes
"""
import os
import signal
from flask import Blueprint, render_template, request, url_for, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename

from services.proposal_service import ProposalService, DataService

# Create blueprint
main_bp = Blueprint('main', __name__)

def init_services(app):
    """Initialize services with app config"""
    global proposal_service, data_service
    proposal_service = ProposalService(app.config)
    data_service = DataService(app.config)

@main_bp.route('/')
def index():
    """Main page route"""
    try:
        districts = data_service.get_districts()
        df = data_service.get_school_data()
        all_data_json = df.to_json(orient='records')
        
        return render_template('index.html', 
                             districts=districts, 
                             all_data=all_data_json)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('error.html', error="Failed to load data"), 500

@main_bp.route('/proposal', methods=['POST'])
def generate_proposal():
    """Generate proposal route"""
    try:
        # Extract form data
        form_data = {
            'district': request.form.get('district'),
            'rfp_type': request.form.get('rfp_type', 'Extended Learning Opportunities Program'),
            'cost_proposal': request.form.get('cost_proposal'),
            'num_weeks': request.form.get('num_weeks'),
            'days_per_week': request.form.get('days_per_week'),
            'selected_schools': request.form.getlist('schoolname'),
            'total_students': request.form.get('total_students_display'),
            'cost_per_student': request.form.get('cost_per_student_display'),
            'hours_per_day': request.form.get('hours_per_day', '3'),
            'daily_cost': request.form.get('daily_cost_for_ai'),
            'weekly_cost': request.form.get('weekly_cost_for_ai')
        }
        
        # Validate required fields
        if not form_data['district']:
            return render_template('error.html', error="District is required"), 400
            
        if not form_data['selected_schools']:
            return render_template('error.html', error="At least one school must be selected"), 400
        
        # Generate proposal
        proposal_text, filename = proposal_service.generate_proposal(**form_data)
        
        # Prepare data for template
        proposal_data = {
            'district': form_data['district'],
            'rfp_type': form_data['rfp_type'],
            'cost_proposal': form_data['cost_proposal'],
            'school_name': ", ".join(form_data['selected_schools']),
            'proposal_text': proposal_text,
            'filename': filename,
            'num_weeks': form_data['num_weeks'],
            'days_per_week': form_data['days_per_week'],
            'hours_per_day': form_data['hours_per_day'],
            'total_students': form_data['total_students'],
            'cost_per_student': form_data['cost_per_student'],
            'daily_cost': form_data['daily_cost'],
            'weekly_cost': form_data['weekly_cost']
        }
        
        return render_template('proposal.html', data=proposal_data)
        
    except Exception as e:
        print(f"Error in generate_proposal route: {e}")
        return render_template('error.html', error=f"Failed to generate proposal: {str(e)}"), 500

@main_bp.route('/download/<path:filename>')
def download_file(filename):
    """Download generated proposal file"""
    try:
        safe_filename = secure_filename(filename)
        download_dir = proposal_service.config['DOWNLOAD_FOLDER']
        file_path = os.path.join(download_dir, safe_filename)
        
        # Security check
        if not os.path.normpath(file_path).startswith(download_dir) or not os.path.isfile(file_path):
            abort(404)

        return send_from_directory(download_dir, safe_filename, as_attachment=True)
        
    except Exception as e:
        print(f"Error in download_file route: {e}")
        abort(404)

@main_bp.route('/api/schools/<district>')
def get_schools_by_district(district):
    """API endpoint to get schools by district"""
    try:
        df = data_service.get_school_data()
        schools = df[df['District Name'] == district].to_dict('records')
        return jsonify(schools)
    except Exception as e:
        print(f"Error in get_schools_by_district route: {e}")
        return jsonify({'error': 'Failed to fetch schools'}), 500

@main_bp.route('/api/validate-form', methods=['POST'])
def validate_form():
    """API endpoint to validate form data"""
    try:
        data = request.get_json()
        
        # Validation rules
        validation_errors = []
        
        # Check required fields
        required_fields = ['district', 'rfp_type', 'selected_schools']
        for field in required_fields:
            if not data.get(field):
                validation_errors.append(f"{field.replace('_', ' ').title()} is required")
        
        # Check numeric constraints
        total_students = int(data.get('total_students', 0))
        if total_students <= 0 or total_students > 200:
            validation_errors.append("Total students must be between 1 and 200")
        
        num_weeks = int(data.get('num_weeks', 0))
        if num_weeks <= 0 or num_weeks > 52:
            validation_errors.append("Number of weeks must be between 1 and 52")
        
        hours_per_day = float(data.get('hours_per_day', 0))
        if hours_per_day <= 0 or hours_per_day > 12:
            validation_errors.append("Hours per day must be between 1 and 12")
        
        # Check school count
        selected_schools = data.get('selected_schools', [])
        if len(selected_schools) > 10:
            validation_errors.append("Maximum 10 schools can be selected")
        
        return jsonify({
            'valid': len(validation_errors) == 0,
            'errors': validation_errors
        })
        
    except Exception as e:
        print(f"Error in validate_form route: {e}")
        return jsonify({'error': 'Validation failed'}), 500

@main_bp.route('/stopServer', methods=['GET'])
def stop_server():
    """Development route to stop server"""
    try:
        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({"success": True, "message": "Server is shutting down..."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error stopping server: {e}"}), 500

@main_bp.route("/healthz")
def health_check():
    """Health check endpoint"""
    return "ok", 200

# Error handlers
@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', error="Page not found"), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error="Internal server error"), 500
