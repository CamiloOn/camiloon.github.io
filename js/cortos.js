/**
 * Cine Tiza - Catálogo Completo de Cortometrajes con Filtros Instantáneos
 */

document.addEventListener('DOMContentLoaded', async () => {
  let allFilms = await CineTizaAPI.getFilms();
  let currentCategory = '';
  let currentYear = '';
  let searchQuery = '';

  const gridContainer = document.getElementById('catalogFilmsGrid');
  const searchInput = document.getElementById('searchFilmInput');
  const categoryFilters = document.querySelectorAll('.filter-btn[data-category]');
  const yearSelect = document.getElementById('yearFilterSelect');
  const countLabel = document.getElementById('filmsCountLabel');

  function render() {
    let filtered = [...allFilms];

    if (currentCategory) {
      filtered = filtered.filter(f => f.category === currentCategory);
    }
    if (currentYear) {
      filtered = filtered.filter(f => f.year == currentYear);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(f =>
        (f.title && f.title.toLowerCase().includes(q)) ||
        (f.institution && f.institution.toLowerCase().includes(q)) ||
        (f.director && f.director.toLowerCase().includes(q)) ||
        (f.genre && f.genre.toLowerCase().includes(q)) ||
        (f.city && f.city.toLowerCase().includes(q))
      );
    }

    if (countLabel) {
      countLabel.textContent = `Mostrando ${filtered.length} cortometraje${filtered.length === 1 ? '' : 's'}`;
    }

    if (!filtered.length) {
      gridContainer.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem;">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
          <h3 style="margin-bottom: 0.5rem;">No se encontraron cortometrajes</h3>
          <p class="text-muted">Intenta ajustando los filtros o la búsqueda por título, escuela o director.</p>
        </div>
      `;
      return;
    }

    gridContainer.innerHTML = filtered.map(film => {
      const awardsHtml = Array.isArray(film.awards) && film.awards.length
        ? `<div class="film-awards-preview">${film.awards.slice(0, 2).map(a => `<span class="award-tag">🏆 ${a}</span>`).join('')}</div>`
        : '';

      return `
        <article class="film-card" data-cursor="play" tabindex="0" role="button" aria-label="Ver cortometraje ${film.title}">
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
    }).join('');

    // Attach click triggers
    gridContainer.querySelectorAll('.film-card').forEach((card, idx) => {
      card.addEventListener('click', () => {
        openFilmModal(filtered[idx]);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openFilmModal(filtered[idx]);
        }
      });
    });
  }

  // Category chip clicks
  categoryFilters.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryFilters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-category') || '';
      render();
    });
  });

  // Year select change
  if (yearSelect) {
    yearSelect.addEventListener('change', (e) => {
      currentYear = e.target.value;
      render();
    });
  }

  // Search input debounced
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchQuery = e.target.value;
        render();
      }, 250);
    });
  }

  // Check URL params for preselected category/search
  const urlParams = new URLSearchParams(window.location.search);
  const catParam = urlParams.get('categoria');
  if (catParam) {
    const matchingBtn = Array.from(categoryFilters).find(b => b.getAttribute('data-category') === catParam.toUpperCase());
    if (matchingBtn) {
      categoryFilters.forEach(b => b.classList.remove('active'));
      matchingBtn.classList.add('active');
      currentCategory = catParam.toUpperCase();
    }
  }

  render();
});
