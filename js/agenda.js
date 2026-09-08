/**
 * Cine Tiza - Lógica de la Agenda y Cronograma Oficial
 */

document.addEventListener('DOMContentLoaded', async () => {
  const events = await CineTizaAPI.getEvents();
  let selectedDay = '2026-10-15';
  let selectedType = '';

  const dayTabs = document.querySelectorAll('.agenda-tab-btn[data-day]');
  const typeFilters = document.querySelectorAll('.filter-btn[data-type]');
  const listContainer = document.getElementById('fullAgendaList');

  function render() {
    let filtered = events.filter(e => e.day_date === selectedDay);

    if (selectedType) {
      filtered = filtered.filter(e => e.type === selectedType);
    }

    if (!filtered.length) {
      listContainer.innerHTML = `
        <div style="text-align: center; padding: 4rem 1rem;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📅</div>
          <p class="text-muted">No hay actividades programadas con los filtros seleccionados para este día.</p>
        </div>
      `;
      return;
    }

    listContainer.innerHTML = filtered.map(ev => {
      const typeClass = `type-${(ev.type || 'proyeccion').toLowerCase()}`;
      return `
        <div class="timeline-item reveal-fade-up visible">
          <div class="event-time">
            <div>${ev.start_time} — ${ev.end_time}</div>
            <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: normal;">${formatDateLabel(ev.day_date)}</span>
          </div>
          <div>
            <h3 class="event-title">${ev.title}</h3>
            <p class="event-desc">${ev.description}</p>
            <div class="event-location">
              <span>🏛️ ${ev.location}</span>
              ${ev.speaker_or_host ? `<span>· 👤 ${ev.speaker_or_host}</span>` : ''}
            </div>
          </div>
          <div>
            <span class="event-badge-type ${typeClass}">${ev.type}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  function formatDateLabel(dateStr) {
    const parts = dateStr.split('-');
    return `${parts[2]} de Octubre`;
  }

  dayTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      dayTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      selectedDay = tab.getAttribute('data-day');
      render();
    });
  });

  typeFilters.forEach(btn => {
    btn.addEventListener('click', () => {
      typeFilters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedType = btn.getAttribute('data-type') || '';
      render();
    });
  });

  render();
});
