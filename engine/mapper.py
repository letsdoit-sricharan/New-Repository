"""
Course Mapper
=============
Maps courses to their assigned time slots using the slot table.
"""

from typing import Dict, List, Tuple
from .slot_parser import SlotTable


class CourseMapper:
    """
    Maps courses to timetable positions based on their assigned slot labels.
    """
    
    def __init__(self, slot_table: SlotTable):
        """
        Initialize the course mapper.
        
        Args:
            slot_table: The SlotTable instance to use for mapping
        """
        self.slot_table = slot_table
    
    def map_course(self, course_name: str, slot_labels: List[str]) -> List[Tuple[str, str, str]]:
        """
        Map a course to its timetable positions.
        
        Args:
            course_name: Name of the course (e.g., "Data Structures")
            slot_labels: List of slot labels assigned to this course (e.g., ['A', 'B', 'H1'])
        
        Returns:
            List of (day, time, course_name) tuples representing all positions
            where this course appears in the timetable
        
        Raises:
            KeyError: If any slot label is not found in the slot table
        """
        positions = []
        
        for slot_label in slot_labels:
            # Get all (day, time) positions for this slot
            slot_positions = self.slot_table.get_slot_positions(slot_label)
            
            # Add course name to each position
            for day, time in slot_positions:
                positions.append((day, time, course_name))
        
        return positions
    
    def map_all_courses(self, courses: List[Dict[str, any]]) -> Dict[Tuple[str, str], List[str]]:
        """
        Map all courses to timetable positions.
        
        Args:
            courses: List of course dictionaries with 'name' and 'slots' keys
                    Example: [
                        {'name': 'Data Structures', 'slots': ['A', 'B', 'H1']},
                        {'name': 'DBMS', 'slots': ['C', 'D', 'I1']},
                    ]
        
        Returns:
            Dictionary mapping (day, time) to list of course names
            Example: {
                ('MON', '8-8:50'): ['Data Structures'],
                ('MON', '9-9:50'): ['DBMS', 'OS'],  # Conflict!
            }
        """
        timetable = {}
        
        for course in courses:
            course_name = course['name']
            slot_labels = course['slots']
            
            # Map this course to its positions
            positions = self.map_course(course_name, slot_labels)
            
            # Add to timetable
            for day, time, _ in positions:
                key = (day, time)
                if key not in timetable:
                    timetable[key] = []
                timetable[key].append(course_name)
        
        return timetable
    
    def get_course_schedule(self, course_name: str, slot_labels: List[str]) -> Dict[str, List[str]]:
        """
        Get the weekly schedule for a specific course.
        
        Args:
            course_name: Name of the course
            slot_labels: Slot labels assigned to this course
        
        Returns:
            Dictionary mapping day to list of time periods
            Example: {
                'MON': ['8-8:50', '9-9:50'],
                'WED': ['10-10:50'],
            }
        """
        positions = self.map_course(course_name, slot_labels)
        
        schedule = {}
        for day, time, _ in positions:
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(time)
        
        return schedule
