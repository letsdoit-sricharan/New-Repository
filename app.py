"""
Slot-Based Timetable Generator
===============================
A Flask web application for generating weekly timetables from user-defined
slot tables and course assignments.

Author: Resume Project
Description: Professional timetable generator with conflict detection
"""

from flask import Flask, render_template, request, jsonify, session
import json
from datetime import timedelta
from engine import SlotTable, TimetableGenerator

app = Flask(__name__)
app.secret_key = 'timetable-generator-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)


@app.route('/')
def index():
    """Main page - slot table input and course entry form."""
    return render_template('index.html')


@app.route('/api/save-slot-table', methods=['POST'])
def save_slot_table():
    """
    Save user-defined slot table to session.
    
    Expected JSON format:
    {
        "days": ["MON", "TUE", "WED", "THU", "FRI"],
        "time_periods": ["8-8:50", "9-9:50", ...],
        "grid": {
            "MON_8-8:50": "A",
            "MON_9-9:50": "F",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'days' not in data or 'time_periods' not in data or 'grid' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: days, time_periods, grid'
            }), 400
        
        # Parse slot table
        slot_table = SlotTable()
        
        # Convert grid format from "DAY_TIME" to (DAY, TIME)
        grid = {}
        for key, value in data['grid'].items():
            parts = key.split('_', 1)
            if len(parts) == 2:
                day, time = parts
                grid[(day, time)] = value
        
        slot_table.parse_from_grid(data['days'], data['time_periods'], grid)
        
        # Validate
        is_valid, errors = slot_table.validate()
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Slot table validation failed',
                'details': errors
            }), 400
        
        # Save to session
        session['slot_table'] = slot_table.to_dict()
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Slot table saved successfully',
            'stats': {
                'days': len(slot_table.days),
                'time_periods': len(slot_table.time_periods),
                'total_slots': len(slot_table.get_all_slots())
            }
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/api/generate-timetable', methods=['POST'])
def generate_timetable():
    """
    Generate timetable from course input.
    
    Expected JSON format:
    {
        "courses": [
            {"name": "Data Structures", "slots": ["A", "B", "H1"]},
            {"name": "DBMS", "slots": ["C", "D", "I1"]},
            ...
        ]
    }
    """
    try:
        # Check if slot table exists in session
        if 'slot_table' not in session:
            return jsonify({
                'success': False,
                'error': 'No slot table found. Please define slot table first.'
            }), 400
        
        data = request.get_json()
        
        if not data or 'courses' not in data:
            return jsonify({'success': False, 'error': 'No course data provided'}), 400
        
        courses = data['courses']
        
        # Reconstruct slot table from session
        slot_table = SlotTable.from_dict(session['slot_table'])
        
        # Create generator
        generator = TimetableGenerator(slot_table)
        
        # Validate course input
        is_valid, errors = generator.validate_course_input(courses)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Course validation failed',
                'details': errors
            }), 400
        
        # Generate timetable
        result = generator.generate(courses)
        
        # Save to session for export
        session['timetable_result'] = {
            'courses': courses,
            'result': {
                'grid': result['grid'],
                'conflicts': result['conflicts'],
                'summary': result['summary'],
                'has_conflicts': result['has_conflicts']
            }
        }
        
        return jsonify({
            'success': True,
            'data': {
                'grid': result['grid'],
                'conflicts': result['conflicts'],
                'summary': result['summary'],
                'has_conflicts': result['has_conflicts'],
                'days': slot_table.days,
                'time_periods': slot_table.time_periods
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/api/get-available-slots', methods=['GET'])
def get_available_slots():
    """Get all available slot labels from the saved slot table."""
    try:
        if 'slot_table' not in session:
            return jsonify({
                'success': False,
                'error': 'No slot table found'
            }), 400
        
        slot_table = SlotTable.from_dict(session['slot_table'])
        
        return jsonify({
            'success': True,
            'slots': slot_table.get_all_slots()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/timetable')
def view_timetable():
    """View generated timetable page."""
    if 'timetable_result' not in session or 'slot_table' not in session:
        return render_template('error.html', 
                             error='No timetable generated. Please go back and create one.')
    
    return render_template('timetable.html')


@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export timetable as PDF (placeholder for now)."""
    # TODO: Implement PDF export using ReportLab
    return jsonify({
        'success': False,
        'error': 'PDF export not yet implemented'
    }), 501


@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """Clear session data and start fresh."""
    session.clear()
    return jsonify({'success': True, 'message': 'Session cleared'})


if __name__ == '__main__':
    print("=" * 60)
    print("Slot-Based Timetable Generator")
    print("=" * 60)
    print("Starting Flask development server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
