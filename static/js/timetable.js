// Timetable Display JavaScript
// Handles rendering and exporting the generated timetable

document.addEventListener('DOMContentLoaded', async () => {
    await loadTimetable();
});

async function loadTimetable() {
    try {
        // Fetch timetable data from backend (stored in session)
        const response = await fetch('/api/generate-timetable', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ courses: [] }) // Will use session data
        }).catch(() => null);

        // If API fails, try to get data from session via a new endpoint
        // For now, we'll redirect if no data
        if (!response || !response.ok) {
            // Try alternate method: render from session
            renderFromSession();
            return;
        }

        const result = await response.json();

        if (result.success) {
            renderTimetable(result.data);
        } else {
            showError('Failed to load timetable data');
        }

    } catch (error) {
        console.error('Error loading timetable:', error);
        renderFromSession();
    }
}

function renderFromSession() {
    // This would be populated by the template if session has data
    // For now, show a placeholder
    Toast.info('Rendering timetable from session...');
}

function renderTimetable(data) {
    const { grid, days, time_periods, conflicts, summary, has_conflicts } = data;

    // Update summary
    const summaryText = `${summary.total_courses} Courses | ${summary.total_periods} Total Periods | ${summary.days} Days`;
    document.getElementById('timetable-summary').textContent = summaryText;

    // Show conflicts if any
    if (has_conflicts) {
        renderConflicts(conflicts);
    }

    // Render timetable grid
    const table = document.getElementById('timetable');
    const thead = table.querySelector('thead tr');
    const tbody = document.getElementById('timetable-body');

    // Clear existing content (except first th)
    while (thead.children.length > 1) {
        thead.removeChild(thead.lastChild);
    }
    tbody.innerHTML = '';

    // Add day headers
    days.forEach(day => {
        const th = createElement('th', '', day);
        thead.appendChild(th);
    });

    // Add rows for each time period
    time_periods.forEach((time, timeIdx) => {
        const row = createElement('tr');

        // Time header
        const timeHeader = createElement('th', 'time-header', time);
        row.appendChild(timeHeader);

        // Cells for each day
        days.forEach((day, dayIdx) => {
            const cellData = grid[dayIdx][timeIdx];
            const cell = createElement('td');

            if (cellData.has_conflict) {
                cell.className = 'conflict-cell';
                cell.innerHTML = cellData.courses.join('<br>');
                cell.title = 'CONFLICT: Multiple courses at same time!';
            } else if (!cellData.is_empty) {
                cell.className = 'course-cell';
                cell.textContent = cellData.courses[0];
            } else {
                cell.className = 'empty-cell';
                cell.textContent = '-';
            }

            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });

    // Render statistics
    renderStats(summary);
}

function renderConflicts(conflicts) {
    const section = document.getElementById('conflicts-section');
    section.style.display = 'block';
    section.innerHTML = '';

    const warning = createElement('div', 'conflict-warning');

    const title = createElement('h3', '', '⚠️ Scheduling Conflicts Detected');
    warning.appendChild(title);

    const desc = createElement('p', '', `Found ${conflicts.length} conflict(s). The following time slots have multiple courses scheduled:`);
    warning.appendChild(desc);

    const list = createElement('ul');
    conflicts.forEach(conflict => {
        const item = createElement('li', '',
            `${conflict.day} @ ${conflict.time}: ${conflict.courses.join(', ')} (${conflict.severity})`
        );
        list.appendChild(item);
    });
    warning.appendChild(list);

    section.appendChild(warning);
}

function renderStats(summary) {
    const container = document.getElementById('stats-grid');
    container.innerHTML = '';

    const stats = [
        { label: 'Total Courses', value: summary.total_courses },
        { label: 'Total Periods', value: summary.total_periods },
        { label: 'Working Days', value: summary.days },
        { label: 'Conflicts', value: summary.conflicts?.total_conflicts || 0 }
    ];

    stats.forEach(stat => {
        const item = createElement('div', 'stat-item');
        const value = createElement('div', 'stat-value', stat.value);
        const label = createElement('div', 'stat-label', stat.label);

        item.appendChild(value);
        item.appendChild(label);
        container.appendChild(item);
    });
}

function showError(message) {
    document.querySelector('.timetable-container').innerHTML = `
        <div class="card">
            <div class="card-body text-center">
                <h2>❌ Error</h2>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.location.href='/'">
                    Go Back
                </button>
            </div>
        </div>
    `;
}

// Export functionality
document.getElementById('export-pdf-btn')?.addEventListener('click', async () => {
    Toast.info('PDF export coming soon!');

    // For now, use print dialog
    window.print();
});
