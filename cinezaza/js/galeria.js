/**
 * Cine Tiza - Lógica de Galería Fotográfica y Videoteca
 */

document.addEventListener('DOMContentLoaded', async () => {
  const galleryItems = await CineTizaAPI.getGallery();
  let currentCategory = '';

  const gridContainer = document.getElementById('fullGalleryGrid');
  const filterBtns = document.querySelectorAll('.filter-btn[data-category]');

  function render() {
    let filtered = [...galleryItems];
    if (currentCategory) {
      filtered = filtered.filter(item => item.category === currentCategory);
    }

    if (!filtered.length) {
      gridContainer.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📸</div>
          <p class="text-muted">No hay fotografías o videos en esta categoría.</p>
        </div>
      `;
      return;
    }

    gridContainer.innerHTML = filtered.map(item => `
      <div class="gallery-item reveal-fade-up visible" data-cursor="view" onclick="openLightbox('${item.media_url}', '${item.caption || item.title}')">
        <img src="${item.media_url}" alt="${item.title}" class="gallery-img" loading="lazy">
        <div class="gallery-overlay">
          <span class="gallery-cat">${item.category}</span>
          <div class="gallery-caption">${item.title}</div>
        </div>
      </div>
    `).join('');
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-category') || '';
      render();
    });
  });

  render();
});
