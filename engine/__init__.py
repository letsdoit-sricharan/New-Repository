"""
Timetable Generation Engine
===========================
Core logic for parsing slot tables, mapping courses, detecting conflicts,
and generating timetables.
"""

from .slot_parser import SlotTable
from .mapper import CourseMapper
from .conflict_detector import ConflictDetector
from .generator import TimetableGenerator

__all__ = [
    'SlotTable',
    'CourseMapper',
    'ConflictDetector',
    'TimetableGenerator'
]
