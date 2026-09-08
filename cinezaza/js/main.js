/**
 * Cine Tiza - Lógica Global y Efectos Cinematográficos
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCustomCursor();
  initCameraHUD();
  initCinemaIntro();
  initScrollReveal();
  initFilmModal();
  initLightbox();
});

/* ================= 1. Navbar con Blur & Mobile Toggle ================= */

function initNavbar() {
  const navbar = document.querySelector('.cinema-navbar');
  const toggleBtn = document.querySelector('.menu-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (navbar) {
    const handleScroll = () => {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  if (toggleBtn && mobileMenu) {
    toggleBtn.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('active');
      toggleBtn.setAttribute('aria-expanded', isOpen);
      toggleBtn.innerHTML = isOpen ? '✕' : '☰';
    });

    // Close on link click
    mobileMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        toggleBtn.innerHTML = '☰';
      });
    });
  }
}

/* ================= 2. Cursor Cinematográfico Inteligente ================= */

function initCustomCursor() {
  // Ignorar en pantallas táctiles
  if (window.matchMedia('(pointer: coarse)').matches) return;

  let cursor = document.querySelector('.cinema-cursor');
  if (!cursor) {
    cursor = document.createElement('div');
    cursor.className = 'cinema-cursor';
    document.body.appendChild(cursor);
  }

  let mouseX = -100;
  let mouseY = -100;
  let currentX = -100;
  let currentY = -100;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  }, { passive: true });

  function renderCursor() {
    currentX += (mouseX - currentX) * 0.35;
    currentY += (mouseY - currentY) * 0.35;
    cursor.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) translate(-50%, -50%)`;
    requestAnimationFrame(renderCursor);
  }
  renderCursor();

  // Delegación de eventos para estados del cursor
  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest('[data-cursor], .film-card, .gallery-item, a, button');
    if (!target) {
      cursor.className = 'cinema-cursor';
      cursor.textContent = '';
      return;
    }

    const type = target.getAttribute('data-cursor');
    if (type === 'play' || target.classList.contains('film-card')) {
      cursor.className = 'cinema-cursor cursor-play';
      cursor.textContent = 'PLAY';
    } else if (type === 'view' || target.classList.contains('gallery-item')) {
      cursor.className = 'cinema-cursor cursor-view';
      cursor.textContent = 'VER';
    } else if (type === 'open' || target.tagName === 'A' || target.tagName === 'BUTTON') {
      cursor.className = 'cinema-cursor cursor-open';
      cursor.textContent = '';
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (!e.relatedTarget) {
      cursor.className = 'cinema-cursor';
      cursor.textContent = '';
    }
  });
}

/* ================= 3. Camera HUD Timecode & Frame Counter ================= */

function initCameraHUD() {
  const timecodeEl = document.querySelector('.hud-timecode');
  const frameEl = document.querySelector('.hud-frame');

  if (!timecodeEl && !frameEl) return;

  let frameCount = 0;
  const startTime = Date.now();

  function updateHUD() {
    frameCount++;
    const elapsed = Date.now() - startTime;
    const hours = Math.floor(elapsed / 3600000).toString().padStart(2, '0');
    const minutes = Math.floor((elapsed % 3600000) / 60000).toString().padStart(2, '0');
    const seconds = Math.floor((elapsed % 60000) / 1000).toString().padStart(2, '0');
    const frames = Math.floor((elapsed % 1000) / (1000 / 24)).toString().padStart(2, '0');

    if (timecodeEl) {
      timecodeEl.textContent = `${hours}:${minutes}:${seconds}:${frames}`;
    }
    if (frameEl) {
      frameEl.textContent = `FRAME ${(frameCount % 9999).toString().padStart(4, '0')}`;
    }
    requestAnimationFrame(updateHUD);
  }

  requestAnimationFrame(updateHUD);
}

/* ================= 4. Intro Cinematográfica Opcional ================= */

function initCinemaIntro() {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const intro = document.querySelector('.cinema-intro-overlay');

  if (!intro) return;

  if (prefersReducedMotion || sessionStorage.getItem('cinetiza_intro_shown')) {
    intro.classList.add('dismissed');
    return;
  }

  // Desvanecer tras 1.4s
  setTimeout(() => {
    intro.classList.add('dismissed');
    sessionStorage.setItem('cinetiza_intro_shown', 'true');
  }, 1400);

  // Permitir saltar con click
  intro.addEventListener('click', () => {
    intro.classList.add('dismissed');
    sessionStorage.setItem('cinetiza_intro_shown', 'true');
  });
}

/* ================= 5. Scroll Reveal con IntersectionObserver ================= */

function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal-fade-up');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  elements.forEach(el => observer.observe(el));
}

/* ================= 6. Modal de Cortometraje y Reproductor ================= */

function initFilmModal() {
  let modal = document.querySelector('.film-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.className = 'film-modal';
    modal.innerHTML = `
      <div class="film-modal-dialog">
        <button class="lightbox-close" id="closeFilmModal" aria-label="Cerrar modal">&times;</button>
        <div class="film-modal-video" id="filmVideoContainer"></div>
        <div class="film-modal-body">
          <div class="film-modal-header">
            <div>
              <span class="scene-tag" id="filmModalCategory">FICCION</span>
              <h2 id="filmModalTitle" style="font-size: 2rem; margin-top: 0.5rem;">Título del Corto</h2>
              <div class="film-institution" id="filmModalInstitution" style="font-size: 1.1rem; margin-top: 0.25rem;">Escuela</div>
              <div class="film-location" id="filmModalLocation">Oncativo, Córdoba</div>
            </div>
            <div id="filmModalAwards" style="display: flex; flex-direction: column; gap: 0.35rem; align-items: flex-end;"></div>
          </div>
          <div class="film-modal-details-grid">
            <div>
              <div class="film-synopsis-title">Sinopsis</div>
              <p id="filmModalSynopsis" style="font-size: 1.05rem; line-height: 1.6; color: var(--text-secondary);"></p>
            </div>
            <div>
              <div class="film-credits-box">
                <div><strong>Dirección:</strong> <span id="filmModalDirector"></span></div>
                <div><strong>Docente Guía:</strong> <span id="filmModalTeacher"></span></div>
                <div><strong>Duración:</strong> <span id="filmModalDuration"></span></div>
                <div><strong>Año:</strong> <span id="filmModalYear"></span></div>
                <div id="filmModalCrew"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('#closeFilmModal').addEventListener('click', closeFilmModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeFilmModal();
    });
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) closeFilmModal();
    });
  }
}

window.openFilmModal = function(film) {
  const modal = document.querySelector('.film-modal');
  if (!modal) return;

  document.getElementById('filmModalTitle').textContent = film.title;
  document.getElementById('filmModalCategory').textContent = film.category.replace('_', ' ');
  document.getElementById('filmModalInstitution').textContent = film.institution;
  document.getElementById('filmModalLocation').textContent = `${film.city || 'Oncativo'}, ${film.province || 'Córdoba'}, ${film.country || 'Argentina'}`;
  document.getElementById('filmModalSynopsis').textContent = film.synopsis || "Sinopsis no disponible.";
  document.getElementById('filmModalDirector').textContent = film.director || "Estudiante realizador";
  document.getElementById('filmModalTeacher').textContent = film.teacher_guide || "Comunidad Educativa";
  document.getElementById('filmModalDuration').textContent = film.duration || "10 min";
  document.getElementById('filmModalYear').textContent = film.year || "2026";

  // Crew
  const crewContainer = document.getElementById('filmModalCrew');
  crewContainer.innerHTML = '';
  if (Array.isArray(film.cast_and_crew) && film.cast_and_crew.length) {
    crewContainer.innerHTML = `<strong>Equipo:</strong> ${film.cast_and_crew.join(', ')}`;
  }

  // Awards
  const awardsContainer = document.getElementById('filmModalAwards');
  awardsContainer.innerHTML = '';
  if (Array.isArray(film.awards)) {
    film.awards.forEach(aw => {
      const tag = document.createElement('span');
      tag.className = 'award-tag';
      tag.textContent = `🏆 ${aw}`;
      awardsContainer.appendChild(tag);
    });
  }

  // Video Embed URL
  const videoContainer = document.getElementById('filmVideoContainer');
  let embedUrl = film.video_url;
  if (embedUrl.includes('youtube.com/watch?v=')) {
    const vidId = embedUrl.split('watch?v=')[1].split('&')[0];
    embedUrl = `https://www.youtube.com/embed/${vidId}?autoplay=1`;
  } else if (embedUrl.includes('youtu.be/')) {
    const vidId = embedUrl.split('youtu.be/')[1].split('?')[0];
    embedUrl = `https://www.youtube.com/embed/${vidId}?autoplay=1`;
  }

  videoContainer.innerHTML = `<iframe src="${embedUrl}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
};

window.closeFilmModal = function() {
  const modal = document.querySelector('.film-modal');
  if (!modal) return;
  modal.classList.remove('active');
  document.getElementById('filmVideoContainer').innerHTML = '';
  document.body.style.overflow = '';
};

/* ================= 7. Lightbox de Galería ================= */

function initLightbox() {
  let lightbox = document.querySelector('.lightbox-modal');
  if (!lightbox) {
    lightbox = document.createElement('div');
    lightbox.className = 'lightbox-modal';
    lightbox.innerHTML = `
      <button class="lightbox-close" id="closeLightbox" aria-label="Cerrar visor">&times;</button>
      <div class="lightbox-content">
        <img src="" alt="" class="lightbox-img" id="lightboxImg">
        <div class="lightbox-caption" id="lightboxCaption"></div>
      </div>
    `;
    document.body.appendChild(lightbox);

    lightbox.querySelector('#closeLightbox').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) closeLightbox();
    });
  }
}

window.openLightbox = function(mediaUrl, caption) {
  const lb = document.querySelector('.lightbox-modal');
  if (!lb) return;
  document.getElementById('lightboxImg').src = mediaUrl;
  document.getElementById('lightboxCaption').textContent = caption || '';
  lb.classList.add('active');
  document.body.style.overflow = 'hidden';
};

window.closeLightbox = function() {
  const lb = document.querySelector('.lightbox-modal');
  if (!lb) return;
  lb.classList.remove('active');
  document.body.style.overflow = '';
};

/* ================= 8. Toast Feedback Helper ================= */

window.showToast = function(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = `
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      z-index: 99999;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    `;
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const bg = type === 'success' ? '#182E1E' : type === 'error' ? '#3B1818' : '#2B2714';
  const border = type === 'success' ? '#38B000' : type === 'error' ? '#D93636' : '#FFD447';
  const color = type === 'success' ? '#85E364' : type === 'error' ? '#FF8585' : '#FFD447';

  toast.style.cssText = `
    background: ${bg};
    border: 1px solid ${border};
    color: ${color};
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    font-family: var(--font-sans);
    font-size: 0.95rem;
    font-weight: 600;
    max-width: 380px;
    animation: fadeInUp 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  `;
  toast.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span> <div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s';
    setTimeout(() => toast.remove(), 400);
  }, 4000);
};
