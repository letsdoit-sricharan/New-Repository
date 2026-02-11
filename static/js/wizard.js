// Wizard for Slot Table and Course Entry
// Handles multi-step form with dynamic field generation

let slotTableData = null;

// Step navigation
function goToStep(stepNumber) {
    // Update progress indicators
    for (let i = 1; i <= 3; i++) {
        const step = document.getElementById(`step-${i}`);
        const indicator = document.getElementById(`step-indicator-${i}`);

        if (i === stepNumber) {
            step.classList.add('active');
            indicator.classList.add('active');
        } else {
            step.classList.remove('active');
            indicator.classList.remove('active');
        }
    }
}

// Step 1: Slot Table Definition

// Initialize day and period inputs
document.getElementById('num-days').addEventListener('change', generateDayInputs);
document.getElementById('num-periods').addEventListener('change', generatePeriodInputs);

function generateDayInputs() {
    const numDays = parseInt(document.getElementById('num-days').value);
    const container = document.getElementById('days-container');
    container.innerHTML = '';

    const defaultDays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

    for (let i = 0; i < numDays; i++) {
        const input = createElement('input', 'day-input');
        input.type = 'text';
        input.placeholder = `Day ${i + 1}`;
        input.value = defaultDays[i] || '';
        input.required = true;
        container.appendChild(input);
    }
}

function generatePeriodInputs() {
    const numPeriods = parseInt(document.getElementById('num-periods').value);
    const container = document.getElementById('periods-container');
    container.innerHTML = '';

    const defaultPeriods = ['8-8:50', '9-9:50', '10-10:50', '11-11:50', '12-12:50', '1-1:50', '2-2:50', '3-3:50', '4-4:50'];

    for (let i = 0; i < numPeriods; i++) {
        const input = createElement('input', 'period-input');
        input.type = 'text';
        input.placeholder = `Period ${i + 1}`;
        input.value = defaultPeriods[i] || '';
        input.required = true;
        container.appendChild(input);
    }
}

// Initialize with default values
generateDayInputs();
generatePeriodInputs();

// Build slot grid
document.getElementById('build-grid-btn').addEventListener('click', buildSlotGrid);

function buildSlotGrid() {
    const days = Array.from(document.querySelectorAll('.day-input')).map(input => input.value.trim());
    const periods = Array.from(document.querySelectorAll('.period-input')).map(input => input.value.trim());

    // Validate
    if (days.some(d => !d) || periods.some(p => !p)) {
        Toast.error('Please fill in all day and period fields');
        return;
    }

    // Show grid section
    document.getElementById('slot-grid-section').style.display = 'block';

    // Build grid table
    const gridContainer = document.getElementById('slot-grid');
    gridContainer.innerHTML = '';

    const table = createElement('table');

    // Header row
    const thead = createElement('thead');
    const headerRow = createElement('tr');
    headerRow.appendChild(createElement('th', '', 'Time / Day'));

    days.forEach(day => {
        headerRow.appendChild(createElement('th', '', day));
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body rows
    const tbody = createElement('tbody');
    periods.forEach(period => {
        const row = createElement('tr');
        row.appendChild(createElement('th', '', period));

        days.forEach(day => {
            const cell = createElement('td');
            const input = createElement('input');
            input.type = 'text';
            input.placeholder = 'Slot';
            input.dataset.day = day;
            input.dataset.time = period;
            cell.appendChild(input);
            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    gridContainer.appendChild(table);

    // Scroll to grid
    document.getElementById('slot-grid-section').scrollIntoView({ behavior: 'smooth' });
}

// Edit structure button
document.getElementById('edit-structure-btn').addEventListener('click', () => {
    document.getElementById('slot-grid-section').style.display = 'none';
});

// Save slot table
document.getElementById('save-slot-table-btn').addEventListener('click', async () => {
    const days = Array.from(document.querySelectorAll('.day-input')).map(input => input.value.trim());
    const periods = Array.from(document.querySelectorAll('.period-input')).map(input => input.value.trim());

    // Collect grid data
    const gridInputs = document.querySelectorAll('#slot-grid input');
    const grid = {};

    gridInputs.forEach(input => {
        const day = input.dataset.day;
        const time = input.dataset.time;
        const value = input.value.trim().toUpperCase();

        if (value) {
            grid[`${day}_${time}`] = value;
        }
    });

    // Validate at least some slots are filled
    if (Object.keys(grid).length === 0) {
        Toast.error('Please fill in at least some slot labels');
        return;
    }

    // Save to server
    const data = { days, time_periods: periods, grid };

    try {
        const result = await API.post('/api/save-slot-table', data);

        if (result.success) {
            slotTableData = data;
            Toast.success('Slot table saved successfully!');

            // Move to step 2
            setTimeout(() => {
                goToStep(2);
                loadAvailableSlots();
            }, 1000);
        } else {
            Toast.error(result.error || 'Failed to save slot table');
        }
    } catch (error) {
        Toast.error('Network error: ' + error.message);
    }
});

// Step 2: Course Entry

async function loadAvailableSlots() {
    try {
        const result = await API.get('/api/get-available-slots');

        if (result.success) {
            const container = document.getElementById('available-slots');
            container.innerHTML = '';

            result.slots.forEach(slot => {
                const chip = createElement('span', 'slot-chip', slot);
                container.appendChild(chip);
            });
        }
    } catch (error) {
        Toast.error('Failed to load slots');
    }
}

// Generate course fields
document.getElementById('generate-course-fields-btn').addEventListener('click', generateCourseFields);

function generateCourseFields() {
    const numCourses = parseInt(document.getElementById('num-courses').value);
    const container = document.getElementById('courses-container');
    container.innerHTML = '';

    for (let i = 1; i <= numCourses; i++) {
        const courseItem = createElement('div', 'course-item');

        // Course name
        const nameDiv = createElement('div');
        const nameLabel = createElement('label', '', `Course ${i} Name`);
        const nameInput = createElement('input');
        nameInput.type = 'text';
        nameInput.placeholder = 'e.g., Data Structures';
        nameInput.className = 'course-name';
        nameInput.required = true;
        nameDiv.appendChild(nameLabel);
        nameDiv.appendChild(nameInput);

        // Slots
        const slotsDiv = createElement('div');
        const slotsLabel = createElement('label', '', 'Slot Labels (comma-separated)');
        const slotsInput = createElement('input');
        slotsInput.type = 'text';
        slotsInput.placeholder = 'e.g., A, B, H1';
        slotsInput.className = 'course-slots';
        slotsInput.required = true;
        slotsDiv.appendChild(slotsLabel);
        slotsDiv.appendChild(slotsInput);

        // Number
        const numDiv = createElement('div', 'course-number');
        numDiv.innerHTML = `<div style="font-size: 2rem; font-weight: bold; opacity: 0.3;">${i}</div>`;

        courseItem.appendChild(nameDiv);
        courseItem.appendChild(slotsDiv);
        courseItem.appendChild(numDiv);

        container.appendChild(courseItem);
    }

    document.getElementById('generate-actions').style.display = 'flex';
}

// Back button
document.getElementById('back-to-step1-btn').addEventListener('click', () => {
    goToStep(1);
});

// Generate timetable
document.getElementById('generate-timetable-btn').addEventListener('click', async () => {
    const courseNames = Array.from(document.querySelectorAll('.course-name'));
    const courseSlots = Array.from(document.querySelectorAll('.course-slots'));

    // Validate
    if (courseNames.some(input => !input.value.trim()) || courseSlots.some(input => !input.value.trim())) {
        Toast.error('Please fill in all course fields');
        return;
    }

    // Build courses array
    const courses = courseNames.map((nameInput, index) => {
        const name = nameInput.value.trim();
        const slotsString = courseSlots[index].value.trim();
        const slots = slotsString.split(',').map(s => s.trim().toUpperCase()).filter(s => s);

        return { name, slots };
    });

    // Show loading
    goToStep(3);

    try {
        const result = await API.post('/api/generate-timetable', { courses });

        if (result.success) {
            Toast.success('Timetable generated!');

            // Redirect to timetable page
            setTimeout(() => {
                window.location.href = '/timetable';
            }, 500);
        } else {
            Toast.error(result.error || 'Failed to generate timetable');
            if (result.details) {
                console.error('Validation errors:', result.details);
            }
            goToStep(2);
        }
    } catch (error) {
        Toast.error('Network error: ' + error.message);
        goToStep(2);
    }
});
