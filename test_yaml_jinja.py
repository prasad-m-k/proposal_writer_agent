#!/usr/bin/env python3

"""Test script to verify YAML + Jinja2 integration"""

import os
import sys
import yaml
import jinja2

def test_yaml_jinja_integration():
    """Test the YAML + Jinja2 integration"""
    print("Testing YAML+Jinja Integration for Request for Qualifications...")

    try:
        # Change to app directory to access input files
        os.chdir('app')

        # Test loading the YAML file
        with open('input_data/natomas_school_district_rfp1.yaml', 'r') as f:
            yaml_data = yaml.safe_load(f)
        print('✓ YAML file loaded successfully')

        # Test loading the Jinja template
        with open('input_data/natomas_school_district_jinja1.md', 'r') as f:
            template_content = f.read()
        print('✓ Jinja template loaded successfully')

        # Test basic rendering with sample data
        template = jinja2.Template(template_content)
        test_vars = yaml_data['vars']

        # Populate with sample data (similar to what populate_yaml_vars would do)
        test_vars['submission']['company_name'] = 'Musical Instruments N Kids Hands (M.I.N.K.H.) - Music Science & Technology Group (MSTG)'
        test_vars['submission']['rep_name'] = 'A.P. Moore, Program Coordinator'
        test_vars['submission']['title'] = 'Program Coordinator'
        test_vars['submission']['email'] = 'aphilanda@musicsciencegroup.com'
        test_vars['submission']['phone'] = '(216) 903-3756'
        test_vars['submission']['address'] = '2150 Capitol Avenue Sacramento, CA 95816'
        test_vars['submission']['signature_name'] = 'A.P. Moore, Program Coordinator'
        test_vars['submission']['signature_date'] = '2025-09-24'

        # Add budget data
        test_vars['budget']['categories']['staffing'] = 12000
        test_vars['budget']['categories']['instructional_materials'] = 2000
        test_vars['budget']['categories']['program_supplies'] = 1500
        test_vars['budget']['categories']['supervision'] = 2000
        test_vars['budget']['categories']['professional_development'] = 1000
        test_vars['budget']['categories']['transportation'] = 500
        test_vars['budget']['categories']['admin_costs'] = 500

        # Add narrative content (TBD placeholders will be filled by Gemini)
        test_vars['narrative']['org_overview'] = 'TBD - Organization overview content'
        test_vars['narrative']['program_design'] = 'TBD - Program design content'
        test_vars['narrative']['hq_elements'] = 'TBD - High quality elements content'
        test_vars['narrative']['staffing_training'] = 'TBD - Staffing and training content'
        test_vars['narrative']['evaluation_outcomes'] = 'TBD - Evaluation and outcomes content'
        test_vars['narrative']['sustainability_innovation'] = 'TBD - Sustainability and innovation content'

        # Add application questions (TBD placeholders)
        for key in test_vars['application_questions']:
            test_vars['application_questions'][key] = f'TBD - Content for {key}'

        # Add references with sample data
        sample_refs = [
            {
                'organization': 'Natomas Unified School District',
                'contact_name': 'Program Administrator',
                'phone': '(916) 567-5000',
                'email': 'programs@natomas.net',
                'dates_of_service': '2023-2024',
                'description': 'Extended Learning Opportunities Program'
            },
            {
                'organization': 'Sacramento City Unified School District',
                'contact_name': 'Enrichment Coordinator',
                'phone': '(916) 643-7400',
                'email': 'enrichment@scusd.edu',
                'dates_of_service': '2022-2023',
                'description': 'Music & STEAM Integration Program'
            },
            {
                'organization': 'Elk Grove Unified School District',
                'contact_name': 'After School Programs Manager',
                'phone': '(916) 686-7700',
                'email': 'afterschool@egusd.net',
                'dates_of_service': '2021-2022',
                'description': 'Arts & Wellness Programs'
            }
        ]

        for i, ref in enumerate(test_vars['references'][:3]):
            if i < len(sample_refs):
                test_vars['references'][i].update(sample_refs[i])

        # Add legal information
        test_vars['legal']['nda_disclosee_name'] = 'Musical Instruments N Kids Hands (M.I.N.K.H.) - Music Science & Technology Group (MSTG)'
        test_vars['legal']['workers_comp_company_name'] = 'Musical Instruments N Kids Hands (M.I.N.K.H.) - Music Science & Technology Group (MSTG)'
        test_vars['legal']['workers_comp_rep_name'] = 'A.P. Moore, Program Coordinator'

        # Render the template
        rendered = template.render(**test_vars)
        print('✓ Template rendered successfully')
        print(f'✓ Rendered content length: {len(rendered)} characters')

        # Show some sample sections
        lines = rendered.split('\n')
        print('\n--- Sample rendered content (first 15 lines) ---')
        for i, line in enumerate(lines[:15]):
            print(f'{i+1:2d}: {line}')
        print('...\n')

        # Check that key sections are populated
        if 'Musical Instruments N Kids Hands' in rendered:
            print('✓ Company name populated correctly')
        if 'A.P. Moore' in rendered:
            print('✓ Representative name populated correctly')
        if '$12,000' in rendered or '12000' in rendered:
            print('✓ Budget values populated correctly')
        if 'TBD' in rendered:
            print('✓ TBD placeholders remain for Gemini to fill')

        # Save a sample for inspection
        with open('../test_rendered_output.md', 'w') as f:
            f.write(rendered)
        print('✓ Sample rendered output saved to test_rendered_output.md')

        return True

    except Exception as e:
        print(f'✗ Error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_yaml_jinja_integration()
    print(f'\nTest {"PASSED" if success else "FAILED"}')
    sys.exit(0 if success else 1)