"""
Timetable Generator
===================
Main orchestrator that combines all engine components to generate timetables.
"""

from typing import Dict, List, Tuple, Optional
from .slot_parser import SlotTable
from .mapper import CourseMapper
from .conflict_detector import ConflictDetector


class TimetableGenerator:
    """
    Main timetable generation engine that orchestrates the entire process.
    """
    
    def __init__(self, slot_table: SlotTable):
        """
        Initialize the timetable generator.
        
        Args:
            slot_table: The SlotTable instance defining the slot structure
        """
        self.slot_table = slot_table
        self.mapper = CourseMapper(slot_table)
        self.conflict_detector = ConflictDetector()
    
    def generate(self, courses: List[Dict[str, any]]) -> Dict:
        """
        Generate a complete timetable with conflict detection.
        
        Args:
            courses: List of course dictionaries
                    Example: [
                        {'name': 'Data Structures', 'slots': ['A', 'B', 'H1']},
                        {'name': 'DBMS', 'slots': ['C', 'D']},
                    ]
        
        Returns:
            Dictionary containing:
            {
                'timetable': {...},  # Grid structure
                'conflicts': [...],  # List of conflicts
                'summary': {...},    # Statistics
                'has_conflicts': bool
            }
        """
        # Step 1: Map all courses to timetable positions
        timetable = self.mapper.map_all_courses(courses)
        
        # Step 2: Detect conflicts
        conflicts = self.conflict_detector.detect_conflicts(timetable)
        
        # Step 3: Generate grid structure for display
        grid = self._generate_grid(timetable)
        
        # Step 4: Compile summary statistics
        summary = self._generate_summary(courses, conflicts)
        
        return {
            'timetable': timetable,
            'grid': grid,
            'conflicts': conflicts,
            'summary': summary,
            'has_conflicts': len(conflicts) > 0
        }
    
    def _generate_grid(self, timetable: Dict[Tuple[str, str], List[str]]) -> List[List[Dict]]:
        """
        Generate a 2D grid structure for HTML table display.
        
        Args:
            timetable: Dictionary mapping (day, time) to list of courses
        
        Returns:
            2D list where grid[day_idx][time_idx] = {
                'courses': [...],
                'has_conflict': bool,
                'is_empty': bool
            }
        """
        grid = []
        
        for day in self.slot_table.days:
            day_row = []
            
            for time in self.slot_table.time_periods:
                key = (day, time)
                courses = timetable.get(key, [])
                
                day_row.append({
                    'courses': courses,
                    'has_conflict': len(courses) > 1,
                    'is_empty': len(courses) == 0,
                    'display': self._format_cell(courses)
                })
            
            grid.append(day_row)
        
        return grid
    
    def _format_cell(self, courses: List[str]) -> str:
        """
        Format course names for display in a cell.
        
        Args:
            courses: List of course names in this cell
        
        Returns:
            Formatted string for display
        """
        if not courses:
            return "-"
        elif len(courses) == 1:
            return courses[0]
        else:
            # Multiple courses (conflict)
            return " / ".join(courses)
    
    def _generate_summary(self, courses: List[Dict], conflicts: List[Dict]) -> Dict:
        """
        Generate summary statistics.
        
        Args:
            courses: Original course list
            conflicts: Detected conflicts
        
        Returns:
            Summary dictionary
        """
        conflict_summary = self.conflict_detector.get_conflict_summary(conflicts)
        
        # Calculate total scheduled periods
        total_periods = 0
        for course in courses:
            for slot_label in course['slots']:
                positions = self.slot_table.get_slot_positions(slot_label)
                total_periods += len(positions)
        
        return {
            'total_courses': len(courses),
            'total_periods': total_periods,
            'conflicts': conflict_summary,
            'days': len(self.slot_table.days),
            'time_slots': len(self.slot_table.time_periods)
        }
    
    def validate_course_input(self, courses: List[Dict[str, any]]) -> Tuple[bool, List[str]]:
        """
        Validate course input before generating timetable.
        
        Args:
            courses: List of course dictionaries
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        if not courses:
            errors.append("No courses provided")
            return False, errors
        
        for i, course in enumerate(courses):
            # Check required fields
            if 'name' not in course:
                errors.append(f"Course {i+1}: Missing 'name' field")
            
            if 'slots' not in course:
                errors.append(f"Course {i+1}: Missing 'slots' field")
            elif not course['slots']:
                errors.append(f"Course '{course.get('name', i+1)}': No slot labels assigned")
            
            # Validate slot labels exist in slot table
            if 'slots' in course:
                for slot_label in course['slots']:
                    if slot_label not in self.slot_table.slot_map:
                        errors.append(f"Course '{course.get('name', i+1)}': Invalid slot label '{slot_label}'")
        
        return len(errors) == 0, errors
