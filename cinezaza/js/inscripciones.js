/**
 * Cine Tiza - Formulario de Inscripción y Envío de Cortometrajes
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('submissionForm');
  const fileInput = document.getElementById('subThumbnail');
  const previewImg = document.getElementById('thumbnailPreview');
  const submitBtn = document.getElementById('submitBtn');

  let thumbnailBase64 = '';

  // Handle Thumbnail / Poster Preview
  if (fileInput && previewImg) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;

      if (file.size > 8 * 1024 * 1024) {
        showToast('El archivo no debe superar los 8MB', 'error');
        fileInput.value = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        thumbnailBase64 = event.target.result;
        previewImg.src = thumbnailBase64;
        previewImg.style.display = 'block';
      };
      reader.readAsDataURL(file);
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const terms = document.getElementById('subTerms');
      if (terms && !terms.checked) {
        showToast('Debes aceptar las bases y condiciones del festival para inscribir tu corto.', 'error');
        return;
      }

      const payload = {
        filmTitle: document.getElementById('subTitle').value.trim(),
        institution: document.getElementById('subInstitution').value.trim(),
        city: document.getElementById('subCity').value.trim(),
        province: document.getElementById('subProvince').value.trim(),
        country: document.getElementById('subCountry').value.trim() || 'Argentina',
        category: document.getElementById('subCategory').value,
        genre: document.getElementById('subGenre').value.trim(),
        duration: document.getElementById('subDuration').value.trim(),
        director: document.getElementById('subDirector').value.trim(),
        participants: document.getElementById('subParticipants').value.trim(),
        teacher: document.getElementById('subTeacher').value.trim(),
        email: document.getElementById('subEmail').value.trim(),
        phone: document.getElementById('subPhone').value.trim(),
        synopsis: document.getElementById('subSynopsis').value.trim(),
        videoUrl: document.getElementById('subVideoUrl').value.trim(),
        thumbnailUrl: thumbnailBase64 || 'images/Logo_CineTiza.png',
        website_hp: document.getElementById('subHp') ? document.getElementById('subHp').value : ''
      };

      if (!payload.filmTitle || !payload.institution || !payload.email || !payload.videoUrl) {
        showToast('Por favor completa todos los campos requeridos marcados con (*)', 'error');
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Enviando postulación... ⏳';
      }

      try {
        const res = await CineTizaAPI.submitFilm(payload);
        if (res.success) {
          showToast(res.message || '¡Inscripción recibida con éxito!', 'success');
          form.reset();
          if (previewImg) previewImg.style.display = 'none';

          // Mostrar mensaje de éxito en pantalla
          const container = document.querySelector('.form-card');
          if (container) {
            container.innerHTML = `
              <div style="text-align: center; padding: 3rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🎉</div>
                <span class="scene-tag">INSCRIPCIÓN REGISTRADA</span>
                <h2 style="margin: 1rem 0;">¡Muchas gracias por sumarte a Cine Tiza!</h2>
                <p style="max-width: 600px; margin: 0 auto 2rem; color: var(--text-secondary);">
                  Tu cortometraje <strong>"${payload.filmTitle}"</strong> ha ingresado a la etapa de preselección de la 18ª Edición.
                  La comisión evaluadora del festival se pondrá en contacto con el docente y equipo al correo <strong>${payload.email}</strong>.
                </p>
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                  <a href="/index.html" class="btn btn-secondary">Volver al Inicio</a>
                  <a href="/cortos.html" class="btn btn-primary">Ver Cortometrajes</a>
                </div>
              </div>
            `;
          }
        } else {
          showToast(res.error || 'Hubo un error al enviar la inscripción', 'error');
        }
      } catch (err) {
        showToast(err.message || 'Error en el servidor', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = 'Enviar Inscripción de Cortometraje';
        }
      }
    });
  }
});
