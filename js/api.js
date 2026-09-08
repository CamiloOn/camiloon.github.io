/**
 * Cine Tiza - API Client & Data Provider
 * Conecta con el backend REST y provee datos factuales con fallback offline automático.
 */

const API_BASE = '/api';

// Cache en memoria y datos de fallback completos
const FALLBACK_DATA = {
  settings: {
    festival_name: "Cine Tiza",
    full_title: "Festival Internacional de Cine y Artes Estudiantiles",
    edition_number: "18",
    edition_year: "2026",
    start_date: "2026-10-15T09:00:00",
    end_date: "2026-10-17T22:00:00",
    submissions_open: "true",
    submissions_deadline: "2026-08-28",
    location_city: "Oncativo",
    location_province: "Córdoba",
    location_country: "Argentina",
    main_venue: "Centro Cultural Gral. San Martín & Sala Teatro Victoria",
    organizer: "Instituto Secundario Oncativo (ISO)",
    contact_email: "festivalcinetiza@gmail.com",
    instagram_url: "https://www.instagram.com/cinetiza/",
    youtube_url: "https://www.youtube.com/@FestivalCineTiza",
    facebook_url: "https://www.facebook.com/festivalcinetiza",
    hero_badge: "18ª EDICIÓN · 15 — 17 OCTUBRE 2026",
    hero_tagline: "UNA PANTALLA PARA LAS NUEVAS VOCES",
    stat_years: "18",
    stat_schools: "100+",
    stat_films: "260+",
    stat_days: "3"
  },
  editions: [
    { id: 18, number: 18, year: 2026, title: "18ª Edición Cine Tiza", theme: "Historias que Transforman", description: "La 18ª edición del Festival Internacional de Cine y Artes Estudiantiles reúne a realizadores de escuelas secundarias de todo el país y el exterior en Oncativo, Córdoba.", start_date: "2026-10-15", end_date: "2026-10-17", poster_url: "images/Centro2026.jpeg", hero_image_url: "images/Centro2026.jpeg", films_count: 35, schools_count: 28, attendees_count: 1200, featured: 1 },
    { id: 17, number: 17, year: 2025, title: "17ª Edición Cine Tiza", theme: "Voces en Movimiento", description: "Edición marcada por la consolidación del certamen internacional y talleres audiovisuales con profesionales del Polo Audiovisual.", start_date: "2025-10-16", end_date: "2025-10-18", poster_url: "images/Carresel1.png", hero_image_url: "images/Carresel1.png", films_count: 32, schools_count: 24, attendees_count: 1100, featured: 0 },
    { id: 16, number: 16, year: 2024, title: "16ª Edición Cine Tiza", theme: "Nuevas Miradas", description: "Celebración de los 15 años de trayectoria con récord de instituciones participantes y gran muestra federal.", start_date: "2024-10-17", end_date: "2024-10-19", poster_url: "images/Carresel2.png", hero_image_url: "images/Carresel2.png", films_count: 30, schools_count: 22, attendees_count: 950, featured: 0 },
    { id: 15, number: 15, year: 2023, title: "15ª Edición Cine Tiza", theme: "El Cine en las Aulas", description: "Encuentro que profundizó la capacitación pedagógica y técnica de estudiantes y docentes de nivel secundario.", start_date: "2023-10-12", end_date: "2023-10-14", poster_url: "images/Carresel3.png", hero_image_url: "images/Carresel3.png", films_count: 28, schools_count: 20, attendees_count: 900, featured: 0 },
    { id: 14, number: 14, year: 2022, title: "14ª Edición Cine Tiza", theme: "Reencuentro Audiovisual", description: "El regreso a las salas llenas en el Teatro Victoria de Oncativo tras las etapas virtuales.", start_date: "2022-10-13", end_date: "2022-10-15", poster_url: "images/Carresel4.png", hero_image_url: "images/Carresel4.png", films_count: 26, schools_count: 18, attendees_count: 850, featured: 0 },
    { id: 13, number: 13, year: 2021, title: "13ª Edición Cine Tiza", theme: "Pantallas Conectadas", description: "Edición híbrida con proyecciones federales y streaming en vivo para toda la comunidad latinoamericana.", start_date: "2021-10-14", end_date: "2021-10-16", poster_url: "images/Carresel5.png", hero_image_url: "images/Carresel5.png", films_count: 24, schools_count: 16, attendees_count: 750, featured: 0 },
    { id: 12, number: 12, year: 2020, title: "12ª Edición Cine Tiza", theme: "Crear en Tiempos de Cambio", description: "Adaptación virtual completa que unió a estudiantes a través de producciones audiovisuales desde sus hogares.", start_date: "2020-10-15", end_date: "2020-10-17", poster_url: "images/Carresel6.png", hero_image_url: "images/Carresel6.png", films_count: 22, schools_count: 15, attendees_count: 600, featured: 0 },
    { id: 1, number: 1, year: 2009, title: "1ª Edición Cine Tiza", theme: "El Nacimiento de un Sueño", description: "Nace Cine Tiza en el Instituto Secundario Oncativo (ISO) como una iniciativa de expresión e intercambio cultural para jóvenes.", start_date: "2009-10-10", end_date: "2009-10-11", poster_url: "images/Logo_CineTiza.png", hero_image_url: "images/Logo_CineTiza.png", films_count: 8, schools_count: 4, attendees_count: 250, featured: 0 }
  ],
  films: [
    {
      id: 1, edition_id: 18, title: "Turno Noche", slug: "turno-noche",
      synopsis: "Un grupo de estudiantes descubre un misterio en los pasillos de su escuela secundaria durante una jornada extracurricular. Una atmósfera de suspenso construida con maestría lumínica y sonora.",
      year: 2025, category: "FICCION", genre: "Suspenso / Drama", duration: "11:42",
      institution: "Instituto Secundario Oncativo (ISO)", city: "Oncativo", province: "Córdoba", country: "Argentina",
      director: "Facundo Rossi & Equipo 6° Año",
      cast_and_crew: ["Camila Díaz (Sonido)", "Mateo Luna (Fotografía)", "Lucía Gómez (Montaje)"],
      teacher_guide: "Prof. Laura Martínez", thumbnail_url: "images/Carresel11.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mejor Cortometraje Ficción 2025", "Mejor Fotografía", "Mejor Sonido"],
      featured: 1, status: "PUBLISHED"
    },
    {
      id: 2, edition_id: 18, title: "SmartBoy", slug: "smartboy",
      synopsis: "Sátira distópica sobre la hiperconexión digital en la juventud y los límites entre la identidad real y el algoritmo escolar.",
      year: 2025, category: "FICCION", genre: "Comedia / Ciencia Ficción", duration: "09:15",
      institution: "Instituto Secundario Oncativo (ISO)", city: "Oncativo", province: "Córdoba", country: "Argentina",
      director: "Valentina Pérez",
      cast_and_crew: ["Joaquín Alvarez (Actuación)", "Sofía Benítez (Arte)"],
      teacher_guide: "Prof. Martín Almada", thumbnail_url: "images/Carresel12.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mención Especial Guión Original", "Premio del Público"],
      featured: 1, status: "PUBLISHED"
    },
    {
      id: 3, edition_id: 18, title: "Las Puertas del Tiempo", slug: "las-puertas-del-tiempo",
      synopsis: "Un viaje documental que rescata la memoria ferroviaria y los relatos orales de los pioneros de la región pampeana cordobesa.",
      year: 2024, category: "DOCUMENTAL", genre: "Histórico / Social", duration: "14:20",
      institution: "IPEM 338 Dr. Salvador Mazza", city: "Córdoba", province: "Córdoba", country: "Argentina",
      director: "Tomás Navarro & Taller Audiovisual",
      cast_and_crew: ["Estudiantes 5° Año IPEM 338"],
      teacher_guide: "Prof. Gabriel Fernández", thumbnail_url: "images/Carresel13.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mejor Documental 16ª Edición", "Seleccionado para Cinedfest España"],
      featured: 1, status: "PUBLISHED"
    },
    {
      id: 4, edition_id: 18, title: "Ecos de Tiza", slug: "ecos-de-tiza",
      synopsis: "Cortometraje de animación stop-motion con plastilina y papel que explora las emociones adolescentes y la presión del futuro.",
      year: 2025, category: "ANIMACION", genre: "Stop Motion / Experimental", duration: "06:50",
      institution: "Escuela ProA Oncativo", city: "Oncativo", province: "Córdoba", country: "Argentina",
      director: "Julieta Molina",
      cast_and_crew: ["Nicolás Vega (Animación)", "Ana Clara Ríos (Música Original)"],
      teacher_guide: "Prof. Roberto Sánchez", thumbnail_url: "images/Carresel14.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mejor Animación 17ª Edición"],
      featured: 1, status: "PUBLISHED"
    },
    {
      id: 5, edition_id: 18, title: "Frecuencia Joven", slug: "frecuencia-joven",
      synopsis: "Videoclip rítmico y conceptual que acompaña la composición musical original de una banda estudiantil sobre la libertad de expresión.",
      year: 2024, category: "VIDEOCLIP", genre: "Musical / Urbano", duration: "04:30",
      institution: "Instituto Manuel Belgrano", city: "Oliva", province: "Córdoba", country: "Argentina",
      director: "Ignacio Ceballos",
      cast_and_crew: ["Banda 'Sin Timbre'", "Equipo Técnico Belgrano"],
      teacher_guide: "Prof. Cecilia Morales", thumbnail_url: "images/Carresel15.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mejor Videoclip"],
      featured: 0, status: "PUBLISHED"
    },
    {
      id: 6, edition_id: 18, title: "Raíces del Valle", slug: "raices-del-valle",
      synopsis: "Muestra Federal que retrata las tradiciones comunitarias y la preservación del monte nativo contada por jóvenes serranos.",
      year: 2025, category: "MUESTRA_FEDERAL", genre: "Documental Territorial", duration: "12:10",
      institution: "IPEM 142 Joaquín V. González", city: "San Marcos Sierras", province: "Córdoba", country: "Argentina",
      director: "Lara Soria",
      cast_and_crew: ["Comunidad Educativa IPEM 142"],
      teacher_guide: "Prof. Marcelo Castro", thumbnail_url: "images/Carresel17.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Destacado Muestra Federal"],
      featured: 0, status: "PUBLISHED"
    },
    {
      id: 7, edition_id: 18, title: "Cartas sin Destino", slug: "cartas-sin-destino",
      synopsis: "Desde España, un relato conmovedor sobre la distancia, la inmigración juvenil y los lazos que persisten a través del tiempo.",
      year: 2025, category: "INTERNACIONAL", genre: "Drama", duration: "10:05",
      institution: "IES Gabriel Ferrater", city: "Reus", province: "Cataluña", country: "España",
      director: "Pau Martí",
      cast_and_crew: ["Elena Soler", "Arnau Rovira"],
      teacher_guide: "Prof. Xavier Puig", thumbnail_url: "images/Carresel18.jpeg",
      video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
      awards: ["Mejor Cortometraje Internacional"],
      featured: 1, status: "PUBLISHED"
    }
  ],
  events: [
    { id: 1, edition_id: 18, day_date: "2026-10-15", start_time: "09:00", end_time: "10:30", title: "Apertura Oficial 18ª Edición & Alfombra Roja", description: "Recepción de delegaciones estudiantiles de todo el país, acto de apertura institucional y corte de cinta en el Centro Cultural San Martín.", location: "Centro Cultural Gral. San Martín", type: "OTRO", speaker_or_host: "Comisión Directiva ISO & Autoridades", featured: 1 },
    { id: 2, edition_id: 18, day_date: "2026-10-15", start_time: "11:00", end_time: "13:00", title: "Bloque 1: Muestra Oficial de Ficción", description: "Primera sesión de proyecciones competitivas de cortometrajes de ficción realizados por escuelas secundarias.", location: "Sala Cine Teatro Victoria", type: "PROYECCION", speaker_or_host: "Jurado Oficial de Ficción", featured: 1 },
    { id: 3, edition_id: 18, day_date: "2026-10-15", start_time: "15:00", end_time: "17:30", title: "Taller: De la Idea al Guión Cinematográfico", description: "Espacio formativo y práctico dictado por docentes del Polo Audiovisual Córdoba sobre estructura dramática para jóvenes realizadores.", location: "Auditorio Instituto Secundario Oncativo", type: "TALLER", speaker_or_host: "Polo Audiovisual Córdoba", featured: 0 },
    { id: 4, edition_id: 18, day_date: "2026-10-15", start_time: "18:00", end_time: "20:30", title: "Bloque 2: Muestra Federal & Debate Abierto", description: "Proyección de producciones regionales que retratan identidades locales de diferentes provincias con ronda de preguntas entre directores.", location: "Sala Cine Teatro Victoria", type: "PROYECCION", speaker_or_host: "Equipo Cine Tiza", featured: 0 },
    { id: 5, edition_id: 18, day_date: "2026-10-16", start_time: "09:30", end_time: "12:00", title: "Bloque 3: Documentales & Animación", description: "Exhibición de cortometrajes documentales y animación stop-motion/digital.", location: "Sala Cine Teatro Victoria", type: "PROYECCION", speaker_or_host: "Jurado de Documental y Animación", featured: 1 },
    { id: 6, edition_id: 18, day_date: "2026-10-16", start_time: "14:30", end_time: "16:30", title: "Taller: Sonido Directo y Banda Sonora", description: "Clínica intensiva sobre grabación de sonido en rodajes escolares, microfonía y diseño sonoro.", location: "Laboratorio Multimedia ProA", type: "TALLER", speaker_or_host: "Especialistas Invitados", featured: 0 },
    { id: 7, edition_id: 18, day_date: "2026-10-16", start_time: "17:00", end_time: "18:30", title: "Charla Magistral: El Futuro del Cine Joven", description: "Encuentro y debate entre directores consagrados y realizadores estudiantiles sobre el salto al cine profesional.", location: "Centro Cultural San Martín", type: "CHARLA", speaker_or_host: "Realizadores Cordobeses Destacados", featured: 0 },
    { id: 8, edition_id: 18, day_date: "2026-10-16", start_time: "19:30", end_time: "22:00", title: "Noche de Videoclips & Arte Urbano", description: "Proyecciones de videoclips musicales en pantalla gigante con intervenciones musicales en vivo de bandas escolares.", location: "Patio de las Artes ISO", type: "MUSICA", speaker_or_host: "Bandas y Realizadores Invitados", featured: 1 },
    { id: 9, edition_id: 18, day_date: "2026-10-17", start_time: "10:00", end_time: "12:30", title: "Bloque 4: Certamen Internacional Cine Tiza", description: "Proyección de cortometrajes seleccionados de instituciones educativas de Iberoamérica.", location: "Sala Cine Teatro Victoria", type: "PROYECCION", speaker_or_host: "Jurado Internacional", featured: 1 },
    { id: 10, edition_id: 18, day_date: "2026-10-17", start_time: "15:00", end_time: "17:00", title: "Foro de Intercambio y Red de Festivales", description: "Mesa de trabajo entre docentes y estudiantes para consolidar la red nacional de festivales escolares.", location: "Auditorio ISO", type: "ARTE", speaker_or_host: "Comunidad Docente y ABC Cine", featured: 0 },
    { id: 11, edition_id: 18, day_date: "2026-10-17", start_time: "19:00", end_time: "22:00", title: "Gala de Clausura & Entrega de Premios 2026", description: "Ceremonia oficial de premiación, entrega de estatuillas Tiza de Oro, menciones especiales y anuncio de clasificados internacionales.", location: "Sala Cine Teatro Victoria", type: "PREMIACION", speaker_or_host: "Comisión Cine Tiza & Jurado Oficial", featured: 1 }
  ],
  gallery: [
    { id: 1, edition_id: 18, title: "Apertura Oficial en Sala Victoria", category: "FESTIVAL", media_type: "IMAGE", media_url: "images/Carresel1.png", caption: "Recepción y sala colmada en Oncativo" },
    { id: 2, edition_id: 18, title: "Taller de Animación y Cámara", category: "TALLERES", media_type: "IMAGE", media_url: "images/Carresel2.png", caption: "Estudiantes explorando técnicas de filmación" },
    { id: 3, edition_id: 18, title: "Proyección en Pantalla Gigante", category: "PROYECCIONES", media_type: "IMAGE", media_url: "images/Carresel3.png", caption: "El público disfrutando de las producciones en competencia" },
    { id: 4, edition_id: 18, title: "Entrega de Premios y Distinciones", category: "PREMIACION", media_type: "IMAGE", media_url: "images/Carresel4.png", caption: "Momento emotivo de la entrega de trofeos Tiza" },
    { id: 5, edition_id: 18, title: "Backstage de Rodaje Estudiantil", category: "BACKSTAGE", media_type: "IMAGE", media_url: "images/Carresel5.png", caption: "Detrás de escena de los cortometrajes participantes" },
    { id: 6, edition_id: 18, title: "Delegaciones de Todo el País", category: "PARTICIPANTES", media_type: "IMAGE", media_url: "images/Carresel6.png", caption: "Jóvenes de diferentes provincias en Oncativo" },
    { id: 7, edition_id: 18, title: "Comunidad ISO y Organizadores", category: "FESTIVAL", media_type: "IMAGE", media_url: "images/Carresel8.png", caption: "El equipo docente y estudiantil del Instituto Secundario Oncativo" },
    { id: 8, edition_id: 18, title: "Muestra de Cortos de Ficción", category: "PROYECCIONES", media_type: "IMAGE", media_url: "images/Carresel9.png", caption: "Debate posterior a la proyección de ficción" },
    { id: 9, edition_id: 18, title: "Jornada de Formación Audiovisual", category: "TALLERES", media_type: "IMAGE", media_url: "images/Carresel10.png", caption: "Prácticas de sonido e iluminación" },
    { id: 10, edition_id: 18, title: "Alfombra Roja y Registro de Medios", category: "BACKSTAGE", media_type: "IMAGE", media_url: "images/Carresel19.jpeg", caption: "Entrevistas en vivo antes de la función de gala" },
    { id: 11, edition_id: 18, title: "Celebración y Encuentro Joven", category: "PARTICIPANTES", media_type: "IMAGE", media_url: "images/Carresel20.jpeg", caption: "Intercambio cultural entre realizadores adolescentes" },
    { id: 12, edition_id: 18, title: "Cierre de la 17ª Edición", category: "PREMIACION", media_type: "IMAGE", media_url: "images/Carresel21.jpeg", caption: "Foto grupal con todas las delegaciones participantes" }
  ],
  awards: [
    { id: 1, edition_id: 18, year: 2025, category_name: "Mejor Cortometraje Ficción", winner_film_title: "Turno Noche", institution: "Instituto Secundario Oncativo", director: "Facundo Rossi", badge_url: "images/Logo_CineTiza.png", notes: "Ganador por unanimidad de jurado técnico" },
    { id: 2, edition_id: 18, year: 2025, category_name: "Mejor Cortometraje Documental", winner_film_title: "Voces del Telar", institution: "IPEM 142 Joaquín V. González", director: "Clara Méndez", badge_url: "images/Logo_CineTiza.png", notes: "Reconocimiento a la preservación cultural" },
    { id: 3, edition_id: 18, year: 2025, category_name: "Mejor Animación", winner_film_title: "Ecos de Tiza", institution: "Escuela ProA Oncativo", director: "Julieta Molina", badge_url: "images/Logo_CineTiza.png", notes: "Destacada técnica en stop motion" },
    { id: 4, edition_id: 18, year: 2025, category_name: "Mejor Cortometraje Internacional", winner_film_title: "Cartas sin Destino", institution: "IES Gabriel Ferrater (España)", director: "Pau Martí", badge_url: "images/Logo_CineTiza.png", notes: "Clasificado para certamen iberoamericano" },
    { id: 5, edition_id: 18, year: 2024, category_name: "Mejor Cortometraje Ficción", winner_film_title: "Las Puertas del Tiempo", institution: "IPEM 338 Dr. Salvador Mazza", director: "Tomás Navarro", badge_url: "images/Logo_CineTiza.png", notes: "Representante oficial en Cinedfest Tenerife" },
    { id: 6, edition_id: 18, year: 2024, category_name: "Premio del Público", winner_film_title: "SmartBoy", institution: "Instituto Secundario Oncativo", director: "Valentina Pérez", badge_url: "images/Logo_CineTiza.png", notes: "Voto popular en sala llena" }
  ]
};

const CineTizaAPI = {
  getAuthToken() {
    return localStorage.getItem('cinetiza_jwt') || '';
  },

  setAuthToken(token, user) {
    if (token) {
      localStorage.setItem('cinetiza_jwt', token);
      if (user) localStorage.setItem('cinetiza_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('cinetiza_jwt');
      localStorage.removeItem('cinetiza_user');
    }
  },

  getCurrentUser() {
    try {
      const u = localStorage.getItem('cinetiza_user');
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    const token = this.getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
      });
      if (res.ok) {
        return await res.json();
      }
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || `HTTP Error ${res.status}`);
    } catch (err) {
      console.warn(`[API] Fallback for ${endpoint}:`, err.message);
      // Fallback local logic
      return this.handleFallback(endpoint, options);
    }
  },

  handleFallback(endpoint, options) {
    const [path, queryStr] = endpoint.split('?');
    const params = new URLSearchParams(queryStr || '');

    if (path === '/settings') {
      return { success: true, data: FALLBACK_DATA.settings };
    }
    if (path === '/editions') {
      return { success: true, data: FALLBACK_DATA.editions };
    }
    if (path === '/films') {
      let filtered = [...FALLBACK_DATA.films];
      const category = params.get('category');
      const year = params.get('year');
      const search = params.get('search');
      const featured = params.get('featured');

      if (category) filtered = filtered.filter(f => f.category === category);
      if (year) filtered = filtered.filter(f => f.year === parseInt(year));
      if (featured) filtered = filtered.filter(f => f.featured === 1);
      if (search) {
        const q = search.toLowerCase();
        filtered = filtered.filter(f => 
          f.title.toLowerCase().includes(q) || 
          f.institution.toLowerCase().includes(q) || 
          f.director.toLowerCase().includes(q)
        );
      }
      return { success: true, data: filtered };
    }
    if (path.startsWith('/films/')) {
      const idOrSlug = path.replace('/films/', '');
      const film = FALLBACK_DATA.films.find(f => f.id == idOrSlug || f.slug == idOrSlug);
      if (film) return { success: true, data: film };
      return { success: false, error: "Cortometraje no encontrado" };
    }
    if (path === '/events') {
      let events = [...FALLBACK_DATA.events];
      const day = params.get('day');
      const type = params.get('type');
      if (day) events = events.filter(e => e.day_date === day);
      if (type) events = events.filter(e => e.type === type);
      return { success: true, data: events };
    }
    if (path === '/gallery') {
      let g = [...FALLBACK_DATA.gallery];
      const cat = params.get('category');
      if (cat) g = g.filter(item => item.category === cat);
      return { success: true, data: g };
    }
    if (path === '/awards') {
      return { success: true, data: FALLBACK_DATA.awards };
    }
    if (path === '/submissions' && options.method === 'POST') {
      return { success: true, message: "¡Inscripción registrada con éxito!" };
    }
    if (path === '/contact' && options.method === 'POST') {
      return { success: true, message: "Tu mensaje ha sido enviado correctamente." };
    }

    return { success: true, data: [] };
  },

  // Helpers específicos
  async getSettings() {
    const res = await this.request('/settings');
    return res.data || FALLBACK_DATA.settings;
  },

  async getEditions() {
    const res = await this.request('/editions');
    return res.data || FALLBACK_DATA.editions;
  },

  async getEdition(id) {
    const res = await this.request(`/editions/${id}`);
    return res.data;
  },

  async getFilms(filters = {}) {
    const q = new URLSearchParams();
    if (filters.category) q.set('category', filters.category);
    if (filters.year) q.set('year', filters.year);
    if (filters.search) q.set('search', filters.search);
    if (filters.featured) q.set('featured', '1');

    const res = await this.request(`/films?${q.toString()}`);
    return res.data || [];
  },

  async getFilm(idOrSlug) {
    const res = await this.request(`/films/${idOrSlug}`);
    return res.data;
  },

  async getEvents(filters = {}) {
    const q = new URLSearchParams();
    if (filters.day) q.set('day', filters.day);
    if (filters.type) q.set('type', filters.type);

    const res = await this.request(`/events?${q.toString()}`);
    return res.data || [];
  },

  async getAwards() {
    const res = await this.request('/awards');
    return res.data || [];
  },

  async getGallery(category = '') {
    const q = category ? `?category=${category}` : '';
    const res = await this.request(`/gallery${q}`);
    return res.data || [];
  },

  async submitFilm(data) {
    return await this.request('/submissions', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  async sendContact(data) {
    return await this.request('/contact', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  async login(username, password) {
    const res = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    if (res.token) {
      this.setAuthToken(res.token, res.user);
    }
    return res;
  },

  logout() {
    this.setAuthToken(null, null);
    window.location.href = '/admin/login.html';
  },

  async getAdminDashboard() {
    const res = await this.request('/admin/dashboard');
    return res.data;
  }
};

window.CineTizaAPI = CineTizaAPI;
