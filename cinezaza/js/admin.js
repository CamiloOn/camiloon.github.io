/**
 * Cine Tiza - Panel de Administración (CMS)
 */

document.addEventListener('DOMContentLoaded', async () => {
  const token = CineTizaAPI.getAuthToken();
  const isLoginPage = window.location.pathname.includes('login.html');

  if (!token && !isLoginPage) {
    window.location.href = '/admin/login.html';
    return;
  }

  if (isLoginPage) {
    initAdminLogin();
    return;
  }

  // Load user data
  const user = CineTizaAPI.getCurrentUser();
  if (user) {
    const nameEl = document.getElementById('adminUserName');
    const roleEl = document.getElementById('adminUserRole');
    if (nameEl) nameEl.textContent = user.full_name || user.username;
    if (roleEl) roleEl.textContent = user.role;
  }

  // Logout button
  const logoutBtn = document.getElementById('adminLogoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => CineTizaAPI.logout());
  }

  // Mobile sidebar toggle
  const sidebarToggle = document.getElementById('adminSidebarToggle');
  const sidebar = document.querySelector('.admin-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
  }

  initNavTabs();
  loadDashboard();
});

/* ================= 1. Login de Administración ================= */

function initAdminLogin() {
  const form = document.getElementById('adminLoginForm');
  const errorMsg = document.getElementById('loginError');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = document.getElementById('loginUser').value.trim();
      const p = document.getElementById('loginPassword').value;

      try {
        const res = await CineTizaAPI.login(u, p);
        if (res.success && res.token) {
          window.location.href = '/admin/index.html';
        } else {
          if (errorMsg) {
            errorMsg.textContent = res.error || 'Credenciales inválidas';
            errorMsg.style.display = 'block';
          }
        }
      } catch (err) {
        if (errorMsg) {
          errorMsg.textContent = err.message || 'Error al iniciar sesión';
          errorMsg.style.display = 'block';
        }
      }
    });
  }
}

/* ================= 2. Pestañas de Navegación ================= */

function initNavTabs() {
  const navItems = document.querySelectorAll('.admin-nav-item[data-tab]');
  const sections = document.querySelectorAll('.admin-tab-section');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const tab = item.getAttribute('data-tab');

      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      sections.forEach(s => {
        s.style.display = s.id === `tab-${tab}` ? 'block' : 'none';
      });

      // Close mobile sidebar if open
      const sidebar = document.querySelector('.admin-sidebar');
      if (sidebar) sidebar.classList.remove('mobile-open');

      // Load tab content
      if (tab === 'dashboard') loadDashboard();
      if (tab === 'submissions') loadAdminSubmissions();
      if (tab === 'films') loadAdminFilms();
      if (tab === 'events') loadAdminEvents();
      if (tab === 'editions') loadAdminEditions();
      if (tab === 'awards') loadAdminAwards();
      if (tab === 'gallery') loadAdminGallery();
      if (tab === 'messages') loadAdminMessages();
      if (tab === 'settings') loadAdminSettings();
    });
  });
}

/* ================= 3. Dashboard ================= */

async function loadDashboard() {
  try {
    const data = await CineTizaAPI.getAdminDashboard();
    if (!data) return;

    document.getElementById('metricSubmissions').textContent = data.counts.submissions || 0;
    document.getElementById('metricPending').textContent = data.counts.submissions_pending || 0;
    document.getElementById('metricFilms').textContent = data.counts.films || 0;
    document.getElementById('metricMessages').textContent = data.counts.messages_unread || 0;

    // Recent Submissions Table
    const tbody = document.getElementById('recentSubmissionsTable');
    if (tbody && data.recent_submissions) {
      tbody.innerHTML = data.recent_submissions.map(s => `
        <tr>
          <td><strong>${s.film_title}</strong></td>
          <td>${s.institution}</td>
          <td>${s.director}</td>
          <td><span class="status-badge badge-${s.status.toLowerCase()}">${s.status}</span></td>
          <td>${s.created_at ? s.created_at.split(' ')[0] : 'Reciente'}</td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.error('Error loading dashboard:', err);
  }
}

/* ================= 4. Gestión de Inscripciones ================= */

async function loadAdminSubmissions() {
  const container = document.getElementById('adminSubmissionsTable');
  if (!container) return;

  try {
    const res = await CineTizaAPI.request('/admin/submissions');
    const submissions = res.data || [];

    if (!submissions.length) {
      container.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No hay inscripciones recibidas aún.</td></tr>`;
      return;
    }

    container.innerHTML = submissions.map(s => `
      <tr>
        <td>#${s.id}</td>
        <td><strong>${s.film_title}</strong></td>
        <td>${s.institution}<br><small class="text-muted">${s.city}, ${s.province}</small></td>
        <td>${s.director}<br><small class="text-muted">${s.email}</small></td>
        <td>
          <select class="form-control" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" onchange="updateSubmissionStatus(${s.id}, this.value)">
            <option value="PENDIENTE" ${s.status === 'PENDIENTE' ? 'selected' : ''}>PENDIENTE</option>
            <option value="EN_REVISION" ${s.status === 'EN_REVISION' ? 'selected' : ''}>EN REVISIÓN</option>
            <option value="APROBADO" ${s.status === 'APROBADO' ? 'selected' : ''}>APROBADO</option>
            <option value="FINALISTA" ${s.status === 'FINALISTA' ? 'selected' : ''}>FINALISTA</option>
            <option value="RECHAZADO" ${s.status === 'RECHAZADO' ? 'selected' : ''}>RECHAZADO</option>
          </select>
        </td>
        <td>
          <a href="${s.video_url}" target="_blank" class="btn-action">Ver Video ↗</a>
        </td>
        <td>
          <div class="action-buttons">
            <button class="btn-action delete" onclick="deleteSubmission(${s.id})">Eliminar</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

window.updateSubmissionStatus = async function (id, newStatus) {
  try {
    const res = await CineTizaAPI.request(`/admin/submissions/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status: newStatus })
    });
    if (res.success) {
      showToast(`Inscripción #${id} actualizada a ${newStatus}`, 'success');
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
};

window.deleteSubmission = async function (id) {
  if (!confirm(`¿Estás seguro de eliminar la postulación #${id}?`)) return;
  try {
    const res = await CineTizaAPI.request(`/admin/submissions/${id}`, { method: 'DELETE' });
    if (res.success) {
      showToast('Inscripción eliminada', 'success');
      loadAdminSubmissions();
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
};

/* ================= 5. Gestión de Cortometrajes ================= */

async function loadAdminFilms() {
  const container = document.getElementById('adminFilmsTable');
  if (!container) return;

  try {
    const res = await CineTizaAPI.request('/admin/films');
    const films = res.data || [];

    container.innerHTML = films.map(f => `
      <tr>
        <td>
          <img src="${f.thumbnail_url || 'images/Logo_CineTiza.png'}" style="width: 50px; height: 35px; object-fit: cover; border-radius: 4px;">
        </td>
        <td><strong>${f.title}</strong></td>
        <td>${f.category}</td>
        <td>${f.year}</td>
        <td>${f.institution}</td>
        <td>${f.featured ? '⭐ Destacado' : 'Estándar'}</td>
        <td>
          <div class="action-buttons">
            <button class="btn-action delete" onclick="deleteFilm(${f.id})">Eliminar</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

window.deleteFilm = async function (id) {
  if (!confirm(`¿Eliminar cortometraje #${id}?`)) return;
  try {
    const res = await CineTizaAPI.request(`/admin/films/${id}`, { method: 'DELETE' });
    if (res.success) {
      showToast('Cortometraje eliminado', 'success');
      loadAdminFilms();
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
};

// Crear nuevo corto modal
window.openCreateFilmModal = function () {
  const modal = document.getElementById('createFilmModal');
  if (modal) modal.classList.add('active');
};

window.closeCreateFilmModal = function () {
  const modal = document.getElementById('createFilmModal');
  if (modal) modal.classList.remove('active');
};

window.submitCreateFilm = async function (e) {
  e.preventDefault();
  const payload = {
    title: document.getElementById('newFilmTitle').value.trim(),
    category: document.getElementById('newFilmCategory').value,
    year: parseInt(document.getElementById('newFilmYear').value, 10),
    duration: document.getElementById('newFilmDuration').value.trim(),
    institution: document.getElementById('newFilmInstitution').value.trim(),
    director: document.getElementById('newFilmDirector').value.trim(),
    videoUrl: document.getElementById('newFilmVideoUrl').value.trim(),
    synopsis: document.getElementById('newFilmSynopsis').value.trim(),
    featured: document.getElementById('newFilmFeatured').checked,
    thumbnailUrl: document.getElementById('newFilmThumbnail').value.trim() || 'images/Logo_CineTiza.png'
  };

  try {
    const res = await CineTizaAPI.request('/admin/films', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    if (res.success) {
      showToast('¡Cortometraje publicado exitosamente!', 'success');
      closeCreateFilmModal();
      document.getElementById('createFilmForm').reset();
      loadAdminFilms();
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
};

/* ================= 6. Gestión de Configuración del Festival ================= */

async function loadAdminSettings() {
  try {
    const settings = await CineTizaAPI.getSettings();
    document.getElementById('setFestName').value = settings.festival_name || '';
    document.getElementById('setEdNumber').value = settings.edition_number || '';
    document.getElementById('setEdYear').value = settings.edition_year || '';
    document.getElementById('setStartDate').value = settings.start_date ? settings.start_date.substring(0, 16) : '';
    document.getElementById('setEndDate').value = settings.end_date ? settings.end_date.substring(0, 16) : '';
    document.getElementById('setSubOpen').checked = settings.submissions_open === 'true';
    document.getElementById('setContactEmail').value = settings.contact_email || '';
    document.getElementById('setInstagram').value = settings.instagram_url || '';
    document.getElementById('setYoutube').value = settings.youtube_url || '';
    document.getElementById('setFacebook').value = settings.facebook_url || '';
  } catch (err) {
    showToast(err.message, 'error');
  }
}

window.saveSettings = async function (e) {
  e.preventDefault();
  const payload = {
    festival_name: document.getElementById('setFestName').value.trim(),
    edition_number: document.getElementById('setEdNumber').value.trim(),
    edition_year: document.getElementById('setEdYear').value.trim(),
    start_date: document.getElementById('setStartDate').value,
    end_date: document.getElementById('setEndDate').value,
    submissions_open: document.getElementById('setSubOpen').checked ? 'true' : 'false',
    contact_email: document.getElementById('setContactEmail').value.trim(),
    instagram_url: document.getElementById('setInstagram').value.trim(),
    youtube_url: document.getElementById('setYoutube').value.trim(),
    facebook_url: document.getElementById('setFacebook').value.trim()
  };

  try {
    const res = await CineTizaAPI.request('/admin/settings', {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    if (res.success) {
      showToast('Configuración del festival guardada correctamente', 'success');
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
};

/* ================= 7. Gestión de Mensajes de Contacto ================= */

async function loadAdminMessages() {
  const container = document.getElementById('adminMessagesTable');
  if (!container) return;

  try {
    const res = await CineTizaAPI.request('/admin/messages');
    const messages = res.data || [];

    if (!messages.length) {
      container.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No hay mensajes recibidos.</td></tr>`;
      return;
    }

    container.innerHTML = messages.map(m => `
      <tr style="${m.is_read ? 'opacity: 0.65;' : 'font-weight: 600;'}">
        <td><strong>${m.name}</strong><br><small class="text-muted">${m.email}</small></td>
        <td>${m.subject}</td>
        <td style="max-width: 320px;">${m.message}</td>
        <td>${m.created_at ? m.created_at.split(' ')[0] : ''}</td>
        <td>
          <div class="action-buttons">
            ${!m.is_read ? `<button class="btn-action" onclick="markMessageRead(${m.id})">Marcar leído</button>` : ''}
            <button class="btn-action delete" onclick="deleteMessage(${m.id})">Eliminar</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

window.markMessageRead = async function (id) {
  try {
    await CineTizaAPI.request(`/admin/messages/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ isRead: true })
    });
    loadAdminMessages();
  } catch (err) {
    showToast(err.message, 'error');
  }
};

window.deleteMessage = async function (id) {
  if (!confirm(`¿Eliminar mensaje #${id}?`)) return;
  try {
    await CineTizaAPI.request(`/admin/messages/${id}`, { method: 'DELETE' });
    loadAdminMessages();
  } catch (err) {
    showToast(err.message, 'error');
  }
};
