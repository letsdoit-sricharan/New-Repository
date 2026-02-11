# 📅 Slot-Based Timetable Generator

A professional web application that generates weekly timetables from user-defined slot tables and course assignments, featuring intelligent conflict detection and a modern, responsive UI.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)

## 🌟 Features

### Core Functionality
- **User-Defined Slot Tables**: No hardcoded assumptions - define your own working days, time periods, and slot labels
- **Flexible Course Management**: Add any number of courses with multiple slot assignments
- **Intelligent Conflict Detection**: Automatically identifies scheduling conflicts with severity levels
- **Visual Timetable Generation**: Clean, color-coded weekly schedule displayed in an interactive grid
- **Export Options**: Export your timetable as PDF or print directly from the browser

### Technical Highlights
- **Modular Engine Architecture**: Separated slot parsing, course mapping, conflict detection, and generation logic
- **Rule-Based Constraint System**: Deterministic scheduling with clear validation and error reporting
- **Session Management**: Persistent data storage across multiple steps
- **RESTful API Design**: Clean endpoint structure with comprehensive error handling
- **Modern UI/UX**: Dark theme with glassmorphism effects, smooth animations, and responsive design

## 🏗️ Project Structure

```
time_table_generator/
├── engine/                    # Core timetable generation logic
│   ├── __init__.py
│   ├── slot_parser.py         # Parses user-defined slot tables
│   ├── mapper.py              # Maps courses to time slots
│   ├── conflict_detector.py   # Detects scheduling conflicts
│   └── generator.py           # Main orchestrator
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern, responsive styling
│   └── js/
│       ├── app.js             # Core utilities
│       ├── wizard.js          # Multi-step form logic
│       └── timetable.js       # Timetable rendering
│
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Main wizard interface
│   └── timetable.html         # Generated timetable view
│
├── app.py                     # Flask application
├── requirements.txt           # Python dependencies
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd time_table_generator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### Step 1: Define Your Slot Table

1. Specify the number of working days (exclude holidays)
2. Enter day names (e.g., MON, TUE, WED, THU, FRI)
3. Define time periods (e.g., 8-8:50, 9-9:50, etc.)
4. Click "Build Slot Grid" to generate the interactive table
5. Fill in slot labels for each time period (leave empty for breaks/lunch)
6. Save your slot table

### Step 2: Enter Courses

1. Specify the number of courses you're taking
2. For each course:
   - Enter the course name
   - Assign slot labels (comma-separated, e.g., "A, B, H1")
3. Generate your timetable

### Step 3: View & Export

- Review your generated timetable
- Check for any scheduling conflicts (highlighted in red)
- Export as PDF or print

## 🎯 Example Use Case

**Scenario**: University student with 5 courses across 5 weekdays

**Slot Table**: 
- Days: MON, TUE, WED, THU, FRI
- Time periods: 8-8:50, 9-9:50, 10-10:50, 11-11:50, 12-12:50, 1-1:50, 2-2:50, 3-3:50, 4-4:50
- Theory slots: A, B, C, D, E, F, G
- Lab slots: H1-H3, I1-I3, J1-J3, K1-K2, L1-L3

**Courses**:
- Data Structures: A, B, H1
- DBMS: C, D, I1
- Operating Systems: E, F, J1
- Computer Networks: G, K1
- Software Engineering: L1

The system automatically maps each course to its time slots and detects any conflicts!

## 🔧 Technical Details

### Core Engine Logic

#### Slot Parser (`engine/slot_parser.py`)
- Parses user-defined slot table structure
- Creates inverted index for O(1) slot lookups
- Validates data integrity

#### Course Mapper (`engine/mapper.py`)
- Maps courses to (day, time, course_name) tuples
- Handles multi-period slots (e.g., lab sessions)
- Generates course schedules

#### Conflict Detector (`engine/conflict_detector.py`)
- Identifies overlapping courses
- Classifies conflicts by severity (high/critical)
- Generates detailed conflict reports

#### Timetable Generator (`engine/generator.py`)
- Orchestrates the entire generation process
- Produces grid structure for HTML rendering
- Compiles summary statistics

### API Endpoints

- `POST /api/save-slot-table`: Save user-defined slot table
- `POST /api/generate-timetable`: Generate timetable from courses
- `GET /api/get-available-slots`: Retrieve available slot labels
- `POST /api/clear-session`: Reset session data

## 🎨 Design Philosophy

- **No Assumptions**: Completely user-driven configuration
- **Modular Architecture**: Easy to extend and maintain
- **Visual Excellence**: Premium UI that stands out
- **Developer-Friendly**: Well-commented code with clear structure

## 🚧 Future Enhancements

- [ ] Excel/CSV file upload for slot tables
- [ ] Advanced PDF export with custom styling
- [ ] Save and load multiple timetable configurations
- [ ] Email/calendar integration
- [ ] Mobile app version

## 📝 Resume Highlights

This project demonstrates:
- ✅ Full-stack web development (Python/Flask + HTML/CSS/JS)
- ✅ Object-oriented programming and design patterns
- ✅ RESTful API design
- ✅ Algorithm design (constraint satisfaction)
- ✅ Modern UI/UX implementation
- ✅ Session management and state handling
- ✅ Data validation and error handling
- ✅ Responsive web design

## 👨‍💻 Author

Resume Project - Slot-Based Timetable Generator

## 📄 License

This project is created for educational and portfolio purposes.

---

**Built with ❤️ using Flask, Modern JavaScript, and CSS**
