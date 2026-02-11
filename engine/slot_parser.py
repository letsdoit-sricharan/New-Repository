"""
Slot Table Parser
=================
Parses and validates user-defined slot table structures.
Converts grid-based input into an efficient lookup dictionary.
"""

from typing import Dict, List, Tuple, Optional


class SlotTable:
    """
    Represents a slot table that maps slot labels to (day, time) positions.
    
    This class handles user-defined timetable structures with no assumptions
    about number of days, time periods, or slot naming conventions.
    """
    
    def __init__(self):
        """Initialize an empty slot table."""
        self.days: List[str] = []
        self.time_periods: List[str] = []
        self.slot_map: Dict[str, List[Tuple[str, str]]] = {}
        self.grid: Dict[Tuple[str, str], str] = {}
    
    def parse_from_grid(self, days: List[str], time_periods: List[str], 
                       grid: Dict[Tuple[str, str], str]) -> None:
        """
        Parse slot table from a grid structure.
        
        Args:
            days: List of day names (e.g., ['MON', 'TUE', 'WED', 'THU', 'FRI'])
            time_periods: List of time slots (e.g., ['8-8:50', '9-9:50', ...])
            grid: Dictionary mapping (day, time) to slot label
                  Example: {('MON', '8-8:50'): 'A', ('MON', '9-9:50'): 'F', ...}
        
        Raises:
            ValueError: If the input structure is invalid
        """
        if not days:
            raise ValueError("Days list cannot be empty")
        
        if not time_periods:
            raise ValueError("Time periods list cannot be empty")
        
        self.days = days
        self.time_periods = time_periods
        self.grid = grid
        
        # Build inverted index: slot_label -> [(day, time), ...]
        self.slot_map = {}
        
        for (day, time), slot_label in grid.items():
            # Skip empty cells (e.g., lunch breaks)
            if not slot_label or slot_label.strip() == '' or slot_label.lower() == 'lunch':
                continue
            
            if slot_label not in self.slot_map:
                self.slot_map[slot_label] = []
            
            self.slot_map[slot_label].append((day, time))
    
    def get_slot_positions(self, slot_label: str) -> List[Tuple[str, str]]:
        """
        Get all (day, time) positions for a given slot label.
        
        Args:
            slot_label: The slot label to lookup (e.g., 'A', 'H1', 'L2')
        
        Returns:
            List of (day, time) tuples where this slot appears
        
        Raises:
            KeyError: If the slot label doesn't exist
        """
        if slot_label not in self.slot_map:
            raise KeyError(f"Slot label '{slot_label}' not found in slot table")
        
        return self.slot_map[slot_label]
    
    def get_all_slots(self) -> List[str]:
        """
        Get all unique slot labels defined in the table.
        
        Returns:
            Sorted list of all slot labels
        """
        return sorted(self.slot_map.keys())
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the slot table structure.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for duplicate assignments (one cell with multiple slots)
        # This shouldn't happen with our data structure, but good to check
        
        # Check that all referenced days exist
        for slot_label, positions in self.slot_map.items():
            for day, time in positions:
                if day not in self.days:
                    errors.append(f"Slot '{slot_label}' references unknown day '{day}'")
                if time not in self.time_periods:
                    errors.append(f"Slot '{slot_label}' references unknown time '{time}'")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict:
        """
        Convert slot table to a dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the slot table
        """
        return {
            'days': self.days,
            'time_periods': self.time_periods,
            'slot_map': {
                label: [(day, time) for day, time in positions]
                for label, positions in self.slot_map.items()
            },
            'grid': {f"{day}_{time}": label for (day, time), label in self.grid.items()}
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'SlotTable':
        """
        Create a SlotTable from a dictionary.
        
        Args:
            data: Dictionary with 'days', 'time_periods', and 'grid' keys
        
        Returns:
            SlotTable instance
        """
        slot_table = SlotTable()
        
        days = data.get('days', [])
        time_periods = data.get('time_periods', [])
        
        # Reconstruct grid from serialized format
        grid_data = data.get('grid', {})
        grid = {}
        for key, label in grid_data.items():
            parts = key.split('_', 1)
            if len(parts) == 2:
                day, time = parts
                grid[(day, time)] = label
        
        slot_table.parse_from_grid(days, time_periods, grid)
        
        return slot_table
    
    def __repr__(self) -> str:
        return f"<SlotTable: {len(self.days)} days, {len(self.time_periods)} periods, {len(self.slot_map)} slots>"
