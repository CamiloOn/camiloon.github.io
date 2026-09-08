/**
 * Cine Tiza - Lógica de la Página Principal (Home)
 */

document.addEventListener('DOMContentLoaded', async () => {
  const settings = await CineTizaAPI.getSettings();
  initCountdown(settings.start_date || '2026-10-15T09:00:00');
  initAnimatedStats();
  loadFeaturedFilms();
  loadAgendaPreview();
  loadGalleryPreview();
});

/* ================= 1. Countdown Dinámico ================= */

function initCountdown(targetDateStr) {
  const targetDate = new Date(targetDateStr).getTime();
  const daysEl = document.getElementById('countDays');
  const hoursEl = document.getElementById('countHours');
  const minsEl = document.getElementById('countMins');
  const secsEl = document.getElementById('countSecs');
  const labelEl = document.getElementById('countdownLabel');

  if (!daysEl || !hoursEl || !minsEl || !secsEl) return;

  function update() {
    const now = Date.now();
    const diff = targetDate - now;

    if (diff <= 0) {
      if (labelEl) labelEl.textContent = '¡CINE TIZA ESTÁ EN MARCHA!';
      daysEl.textContent = '00';
      hoursEl.textContent = '00';
      minsEl.textContent = '00';
      secsEl.textContent = '00';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    daysEl.textContent = days.toString().padStart(2, '0');
    hoursEl.textContent = hours.toString().padStart(2, '0');
    minsEl.textContent = mins.toString().padStart(2, '0');
    secsEl.textContent = secs.toString().padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}

/* ================= 2. Contador de Números Animados ================= */

function initAnimatedStats() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (!statNumbers.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateValue(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  statNumbers.forEach(el => observer.observe(el));
}

function animateValue(element) {
  const targetStr = element.getAttribute('data-target') || element.textContent;
  const isPlus = targetStr.includes('+');
  const target = parseInt(targetStr.replace(/\D/g, ''), 10) || 0;
  let start = 0;
  const duration = 1600;
  const stepTime = 25;
  const steps = duration / stepTime;
  const increment = target / steps;

  const timer = setInterval(() => {
    start += increment;
    if (start >= target) {
      element.textContent = target + (isPlus ? '+' : '');
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(start) + (isPlus ? '+' : '');
    }
  }, stepTime);
}

/* ================= 3. Carga de Cortometrajes Destacados ================= */

async function loadFeaturedFilms() {
  const container = document.getElementById('featuredFilmsGrid');
  if (!container) return;

  const films = await CineTizaAPI.getFilms({ featured: true });
  const displayFilms = films.slice(0, 6);

  if (!displayFilms.length) {
    container.innerHTML = `<p class="text-muted" style="text-align: center; grid-column: 1/-1;">No hay cortometrajes destacados por el momento.</p>`;
    return;
  }

  container.innerHTML = displayFilms.map(film => renderFilmCard(film)).join('');

  // Attach click events
  container.querySelectorAll('.film-card').forEach((card, idx) => {
    card.addEventListener('click', () => {
      openFilmModal(displayFilms[idx]);
    });
  });
}

function renderFilmCard(film) {
  const awardsHtml = Array.isArray(film.awards) && film.awards.length
    ? `<div class="film-awards-preview">${film.awards.slice(0, 2).map(a => `<span class="award-tag">🏆 ${a}</span>`).join('')}</div>`
    : '';

  return `
    <article class="film-card reveal-fade-up" data-cursor="play" tabindex="0" role="button" aria-label="Ver cortometraje ${film.title}">
      <div class="film-thumbnail-wrapper">
        <img src="${film.thumbnail_url || 'images/Logo_CineTiza.png'}" alt="Afiche de ${film.title}" class="film-thumbnail" loading="lazy">
        <span class="film-badge-category">${(film.category || 'FICCION').replace('_', ' ')}</span>
        <span class="film-duration">⏱ ${film.duration || '10:00'}</span>
        <div class="film-play-overlay">
          <div class="play-circle">▶</div>
        </div>
      </div>
      <div class="film-body">
        <h3 class="film-title">${film.title}</h3>
        <div class="film-institution">${film.institution}</div>
        <div class="film-location">📍 ${film.city || 'Oncativo'}, ${film.province || 'Córdoba'} · ${film.year}</div>
        ${awardsHtml}
      </div>
    </article>
  `;
}

/* ================= 4. Carga de Highlights de la Agenda ================= */

async function loadAgendaPreview() {
  const container = document.getElementById('agendaPreviewList');
  if (!container) return;

  const events = await CineTizaAPI.getEvents();
  const highlighted = events.filter(e => e.featured).slice(0, 4);

  if (!highlighted.length) return;

  container.innerHTML = highlighted.map(ev => {
    const typeClass = `type-${(ev.type || 'proyeccion').toLowerCase()}`;
    return `
      <div class="timeline-item reveal-fade-up">
        <div class="event-time">
          <div>${ev.start_time} — ${ev.end_time}</div>
          <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: normal;">${ev.day_date.split('-').slice(1).reverse().join('/')}</span>
        </div>
        <div>
          <h4 class="event-title">${ev.title}</h4>
          <p class="event-desc">${ev.description}</p>
          <div class="event-location">🏛️ ${ev.location} ${ev.speaker_or_host ? `· 👤 ${ev.speaker_or_host}` : ''}</div>
        </div>
        <div>
          <span class="event-badge-type ${typeClass}">${ev.type}</span>
        </div>
      </div>
    `;
  }).join('');
}

/* ================= 5. Carga de Vista Previa de Galería ================= */

async function loadGalleryPreview() {
  const container = document.getElementById('galleryPreviewGrid');
  if (!container) return;

  const gallery = await CineTizaAPI.getGallery();
  const preview = gallery.slice(0, 8);

  container.innerHTML = preview.map(item => `
    <div class="gallery-item reveal-fade-up" data-cursor="view" onclick="openLightbox('${item.media_url}', '${item.caption || item.title}')">
      <img src="${item.media_url}" alt="${item.title}" class="gallery-img" loading="lazy">
      <div class="gallery-overlay">
        <span class="gallery-cat">${item.category}</span>
        <div class="gallery-caption">${item.title}</div>
      </div>
    </div>
  `).join('');
}
