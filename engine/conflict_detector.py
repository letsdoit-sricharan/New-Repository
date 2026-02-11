"""
Conflict Detector
=================
Detects scheduling conflicts when multiple courses occupy the same time slot.
"""

from typing import Dict, List, Tuple


class ConflictDetector:
    """
    Identifies and reports scheduling conflicts in the timetable.
    """
    
    def detect_conflicts(self, timetable: Dict[Tuple[str, str], List[str]]) -> List[Dict]:
        """
        Detect conflicts in the timetable.
        
        A conflict occurs when multiple courses are scheduled at the same (day, time).
        
        Args:
            timetable: Dictionary mapping (day, time) to list of course names
        
        Returns:
            List of conflict dictionaries with details:
            [
                {
                    'day': 'MON',
                    'time': '8-8:50',
                    'courses': ['Data Structures', 'DBMS'],
                    'severity': 'high'  # 'high' for 2+, 'critical' for 3+
                },
                ...
            ]
        """
        conflicts = []
        
        for (day, time), courses in timetable.items():
            # Conflict exists if more than one course at the same time
            if len(courses) > 1:
                severity = 'critical' if len(courses) >= 3 else 'high'
                
                conflicts.append({
                    'day': day,
                    'time': time,
                    'courses': courses,
                    'count': len(courses),
                    'severity': severity
                })
        
        return conflicts
    
    def has_conflicts(self, timetable: Dict[Tuple[str, str], List[str]]) -> bool:
        """
        Check if the timetable has any conflicts.
        
        Args:
            timetable: Dictionary mapping (day, time) to list of course names
        
        Returns:
            True if conflicts exist, False otherwise
        """
        return any(len(courses) > 1 for courses in timetable.values())
    
    def get_conflict_summary(self, conflicts: List[Dict]) -> Dict:
        """
        Generate a summary of all conflicts.
        
        Args:
            conflicts: List of conflict dictionaries from detect_conflicts()
        
        Returns:
            Summary dictionary with statistics:
            {
                'total_conflicts': 3,
                'high_severity': 2,
                'critical_severity': 1,
                'affected_courses': ['DS', 'DBMS', 'OS']
            }
        """
        if not conflicts:
            return {
                'total_conflicts': 0,
                'high_severity': 0,
                'critical_severity': 0,
                'affected_courses': []
            }
        
        high_count = sum(1 for c in conflicts if c['severity'] == 'high')
        critical_count = sum(1 for c in conflicts if c['severity'] == 'critical')
        
        # Get all unique courses involved in conflicts
        affected_courses = set()
        for conflict in conflicts:
            affected_courses.update(conflict['courses'])
        
        return {
            'total_conflicts': len(conflicts),
            'high_severity': high_count,
            'critical_severity': critical_count,
            'affected_courses': sorted(list(affected_courses))
        }
    
    def get_conflict_report(self, conflicts: List[Dict]) -> str:
        """
        Generate a human-readable conflict report.
        
        Args:
            conflicts: List of conflict dictionaries
        
        Returns:
            Formatted string report
        """
        if not conflicts:
            return "No scheduling conflicts detected. ✓"
        
        summary = self.get_conflict_summary(conflicts)
        
        report = f"⚠️ SCHEDULING CONFLICTS DETECTED\n"
        report += f"Total conflicts: {summary['total_conflicts']}\n"
        report += f"High severity: {summary['high_severity']}, Critical: {summary['critical_severity']}\n\n"
        report += "Conflict Details:\n"
        report += "-" * 60 + "\n"
        
        for i, conflict in enumerate(conflicts, 1):
            report += f"{i}. {conflict['day']} @ {conflict['time']}\n"
            report += f"   Courses: {', '.join(conflict['courses'])}\n"
            report += f"   Severity: {conflict['severity'].upper()}\n\n"
        
        return report
