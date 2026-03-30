document.addEventListener('DOMContentLoaded', function () {
    const widget = document.getElementById('calendar-widget');
    if (!widget) return;

    let year = parseInt(widget.getAttribute('data-year'), 10);
    let month = parseInt(widget.getAttribute('data-month'), 10);
    const apiBase = '/events/api/calendar/';
    const titleEl = document.getElementById('calendar-title');
    const bodyEl = document.getElementById('calendar-body');
    const listEl = document.getElementById('calendar-events-list');

    function fetchAndRender(y, m) {
        fetch(`${apiBase}?year=${y}&month=${m}`)
            .then(r => r.json())
            .then(data => {
                if (!data.success) return;
                renderCalendar(y, m, data.days, data.month_name);
            })
            .catch(console.error);
    }

    function renderCalendar(y, m, daysMap, monthName) {
        titleEl.textContent = `${monthName} ${y}`;
        // build weeks using JS
        const firstDay = new Date(y, m - 1, 1).getDay();
        const daysInMonth = new Date(y, m, 0).getDate();

        // create 6 weeks x 7 days
        let html = '';
        let day = 1;
        for (let wk = 0; wk < 6; wk++) {
            html += '<tr>';
            for (let d = 0; d < 7; d++) {
                if (wk === 0 && d < firstDay) {
                    html += '<td class="empty"></td>';
                } else if (day > daysInMonth) {
                    html += '<td class="empty"></td>';
                } else {
                    const has = daysMap[String(day)] !== undefined;
                    html += `<td data-day="${day}" class="${has ? 'has-event' : ''}"><div class="day-number">${day}</div></td>`;
                    day++;
                }
            }
            html += '</tr>';
        }

        bodyEl.innerHTML = html;

        // attach click handlers
        bodyEl.querySelectorAll('td[data-day]').forEach(td => {
            td.addEventListener('click', () => {
                const d = td.getAttribute('data-day');
                showEventsForDay(d, daysMap);
            });
        });
    }

    function showEventsForDay(day, daysMap) {
        const events = daysMap[String(day)] || [];
        if (events.length === 0) {
            listEl.innerHTML = '<p>No events for this day.</p>';
            return;
        }
        let out = '<ul class="list-unstyled">';
        events.forEach(ev => {
            out += `<li><a href="/events/events/details/${ev.id}/">${ev.title}</a></li>`;
        });
        out += '</ul>';
        listEl.innerHTML = out;
    }

    // nav
    const prev = widget.querySelector('.prev-month');
    const next = widget.querySelector('.next-month');
    prev && prev.addEventListener('click', (e) => {
        e.preventDefault();
        month -= 1;
        if (month < 1) { month = 12; year -= 1; }
        fetchAndRender(year, month);
    });
    next && next.addEventListener('click', (e) => {
        e.preventDefault();
        month += 1;
        if (month > 12) { month = 1; year += 1; }
        fetchAndRender(year, month);
    });

    // initial
    fetchAndRender(year, month);
});
