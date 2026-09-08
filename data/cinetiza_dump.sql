-- ========================================================
-- Cine Tiza 18ª Edición (2026) - MySQL / MariaDB Dump
-- Festival Internacional de Cine y Artes Estudiantiles
-- Instituto Secundario Oncativo (ISO), Córdoba, Argentina
-- ========================================================

SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE IF NOT EXISTS `cinetiza_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `cinetiza_db`;

DROP TABLE IF EXISTS `site_settings`;
CREATE TABLE `site_settings` (
  `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `site_settings` (`key`, `value`) VALUES
('collaborators', 'Grupo ABC Cine, Escuela ProA Oncativo, Polo Audiovisual Córdoba, Municipalidad de Oncativo'),
('contact_email', 'festivalcinetiza@gmail.com'),
('edition_number', '18'),
('edition_year', '2026'),
('end_date', '2026-10-17T22:00:00'),
('facebook_url', 'https://www.facebook.com/festivalcinetiza'),
('festival_name', 'Cine Tiza'),
('full_title', 'Festival Internacional de Cine y Artes Estudiantiles'),
('hero_badge', '18ª EDICIÓN · 15 — 17 OCTUBRE 2026'),
('hero_tagline', 'UNA PANTALLA PARA LAS NUEVAS VOCES'),
('instagram_url', 'https://www.instagram.com/cinetiza/'),
('location_city', 'Oncativo'),
('location_country', 'Argentina'),
('location_province', 'Córdoba'),
('main_venue', 'Centro Cultural Gral. San Martín & Sala Teatro Victoria'),
('organizer', 'Instituto Secundario Oncativo (ISO)'),
('start_date', '2026-10-15T09:00:00'),
('stat_days', '3'),
('stat_films', '260+'),
('stat_schools', '100+'),
('stat_years', '18'),
('submissions_deadline', '2026-08-28'),
('submissions_open', 'true'),
('submissions_start', '2026-03-16'),
('youtube_url', 'https://www.youtube.com/@FestivalCineTiza');

DROP TABLE IF EXISTS `editions`;
CREATE TABLE `editions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `theme` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_date` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `poster_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hero_image_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `films_count` int(11) DEFAULT 0,
  `schools_count` int(11) DEFAULT 0,
  `attendees_count` int(11) DEFAULT 0,
  `featured` tinyint(4) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  UNIQUE KEY `year` (`year`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `editions` (`id`, `number`, `year`, `title`, `theme`, `description`, `start_date`, `end_date`, `poster_url`, `hero_image_url`, `films_count`, `schools_count`, `attendees_count`, `featured`, `created_at`) VALUES
(1, 18, 2026, '18ª Edición Cine Tiza', 'Historias que Transforman', 'La 18ª edición del Festival Internacional de Cine y Artes Estudiantiles reúne a realizadores de escuelas secundarias de todo el país y el exterior en Oncativo, Córdoba.', '2026-10-15', '2026-10-17', 'images/Centro2026.jpeg', 'images/Centro2026.jpeg', 35, 28, 1200, 1, '2026-09-08 08:03:42'),
(2, 17, 2025, '17ª Edición Cine Tiza', 'Voces en Movimiento', 'Edición marcada por la consolidación del certamen internacional y talleres audiovisuales con profesionales del Polo Audiovisual.', '2025-10-16', '2025-10-18', 'images/Carresel1.png', 'images/Carresel1.png', 32, 24, 1100, 0, '2026-09-08 08:03:42'),
(3, 16, 2024, '16ª Edición Cine Tiza', 'Nuevas Miradas', 'Celebración de los 15 años de trayectoria con récord de instituciones participantes y gran muestra federal.', '2024-10-17', '2024-10-19', 'images/Carresel2.png', 'images/Carresel2.png', 30, 22, 950, 0, '2026-09-08 08:03:42'),
(4, 15, 2023, '15ª Edición Cine Tiza', 'El Cine en las Aulas', 'Encuentro que profundizó la capacitación pedagógica y técnica de estudiantes y docentes de nivel secundario.', '2023-10-12', '2023-10-14', 'images/Carresel3.png', 'images/Carresel3.png', 28, 20, 900, 0, '2026-09-08 08:03:42'),
(5, 14, 2022, '14ª Edición Cine Tiza', 'Reencuentro Audiovisual', 'El regreso a las salas llenas en el Teatro Victoria de Oncativo tras las etapas virtuales.', '2022-10-13', '2022-10-15', 'images/Carresel4.png', 'images/Carresel4.png', 26, 18, 850, 0, '2026-09-08 08:03:42'),
(6, 13, 2021, '13ª Edición Cine Tiza', 'Pantallas Conectadas', 'Edición híbrida con proyecciones federales y streaming en vivo para toda la comunidad latinoamericana.', '2021-10-14', '2021-10-16', 'images/Carresel5.png', 'images/Carresel5.png', 24, 16, 750, 0, '2026-09-08 08:03:42'),
(7, 12, 2020, '12ª Edición Cine Tiza', 'Crear en Tiempos de Cambio', 'Adaptación virtual completa que unió a estudiantes a través de producciones audiovisuales desde sus hogares.', '2020-10-15', '2020-10-17', 'images/Carresel6.png', 'images/Carresel6.png', 22, 15, 600, 0, '2026-09-08 08:03:42'),
(8, 1, 2009, '1ª Edición Cine Tiza', 'El Nacimiento de un Sueño', 'Nace Cine Tiza en el Instituto Secundario Oncativo (ISO) como una iniciativa de expresión e intercambio cultural para jóvenes.', '2009-10-10', '2009-10-11', 'images/Logo_CineTiza.png', 'images/Logo_CineTiza.png', 8, 4, 250, 0, '2026-09-08 08:03:42');

DROP TABLE IF EXISTS `films`;
CREATE TABLE `films` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edition_id` int(11) NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `synopsis` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int(11) NOT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `genre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `province` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Argentina',
  `director` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cast_and_crew` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `teacher_guide` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `thumbnail_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `video_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awards` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `featured` tinyint(4) DEFAULT 0,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'PUBLISHED',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `edition_id` (`edition_id`),
  CONSTRAINT `films_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `films` (`id`, `edition_id`, `title`, `slug`, `synopsis`, `year`, `category`, `genre`, `duration`, `institution`, `city`, `province`, `country`, `director`, `cast_and_crew`, `teacher_guide`, `thumbnail_url`, `video_url`, `awards`, `featured`, `status`, `created_at`) VALUES
(1, 1, 'Turno Noche', 'turno-noche', 'Un grupo de estudiantes descubre un misterio en los pasillos de su escuela secundaria durante una jornada extracurricular. Una atmósfera de suspenso construida con maestría lumínica y sonora.', 2025, 'FICCION', 'Suspenso / Drama', '11:42', 'Instituto Secundario Oncativo (ISO)', 'Oncativo', 'Córdoba', 'Argentina', 'Facundo Rossi & Equipo 6° Año', '["Camila D\\u00edaz (Sonido)", "Mateo Luna (Fotograf\\u00eda)", "Luc\\u00eda G\\u00f3mez (Montaje)"]', 'Prof. Laura Martínez', 'images/Carresel11.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Mejor Cortometraje Ficci\\u00f3n 2025", "Mejor Fotograf\\u00eda", "Mejor Sonido"]', 1, 'PUBLISHED', '2026-09-08 08:03:42'),
(2, 1, 'SmartBoy', 'smartboy', 'Sátira distópica sobre la hiperconexión digital en la juventud y los límites entre la identidad real y el algoritmo escolar.', 2025, 'FICCION', 'Comedia / Ciencia Ficción', '09:15', 'Instituto Secundario Oncativo (ISO)', 'Oncativo', 'Córdoba', 'Argentina', 'Valentina Pérez', '["Joaqu\\u00edn Alvarez (Actuaci\\u00f3n)", "Sof\\u00eda Ben\\u00edtez (Arte)"]', 'Prof. Martín Almada', 'images/Carresel12.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Menci\\u00f3n Especial Gui\\u00f3n Original", "Premio del P\\u00fablico"]', 1, 'PUBLISHED', '2026-09-08 08:03:42'),
(3, 1, 'Las Puertas del Tiempo', 'las-puertas-del-tiempo', 'Un viaje documental que rescata la memoria ferroviaria y los relatos orales de los pioneros de la región pampeana cordobesa.', 2024, 'DOCUMENTAL', 'Histórico / Social', '14:20', 'IPEM 338 Dr. Salvador Mazza', 'Córdoba', 'Córdoba', 'Argentina', 'Tomás Navarro & Taller Audiovisual', '["Estudiantes 5\\u00b0 A\\u00f1o IPEM 338"]', 'Prof. Gabriel Fernández', 'images/Carresel13.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Mejor Documental 16\\u00aa Edici\\u00f3n", "Seleccionado para Cinedfest Espa\\u00f1a"]', 1, 'PUBLISHED', '2026-09-08 08:03:42'),
(4, 1, 'Ecos de Tiza', 'ecos-de-tiza', 'Cortometraje de animación stop-motion con plastilina y papel que explora las emociones adolescentes y la presión del futuro.', 2025, 'ANIMACION', 'Stop Motion / Experimental', '06:50', 'Escuela ProA Oncativo', 'Oncativo', 'Córdoba', 'Argentina', 'Julieta Molina', '["Nicol\\u00e1s Vega (Animaci\\u00f3n)", "Ana Clara R\\u00edos (M\\u00fasica Original)"]', 'Prof. Roberto Sánchez', 'images/Carresel14.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Mejor Animaci\\u00f3n 17\\u00aa Edici\\u00f3n"]', 1, 'PUBLISHED', '2026-09-08 08:03:42'),
(5, 1, 'Frecuencia Joven', 'frecuencia-joven', 'Videoclip rítmico y conceptual que acompaña la composición musical original de una banda estudiantil sobre la libertad de expresión.', 2024, 'VIDEOCLIP', 'Musical / Urbano', '04:30', 'Instituto Manuel Belgrano', 'Oliva', 'Córdoba', 'Argentina', 'Ignacio Ceballos', '["Banda \'Sin Timbre\'", "Equipo T\\u00e9cnico Belgrano"]', 'Prof. Cecilia Morales', 'images/Carresel15.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Mejor Videoclip"]', 0, 'PUBLISHED', '2026-09-08 08:03:42'),
(6, 1, 'Raíces del Valle', 'raices-del-valle', 'Muestra Federal que retrata las tradiciones comunitarias y la preservación del monte nativo contada por jóvenes serranos.', 2025, 'MUESTRA_FEDERAL', 'Documental Territorial', '12:10', 'IPEM 142 Joaquín V. González', 'San Marcos Sierras', 'Córdoba', 'Argentina', 'Lara Soria', '["Comunidad Educativa IPEM 142"]', 'Prof. Marcelo Castro', 'images/Carresel17.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Destacado Muestra Federal"]', 0, 'PUBLISHED', '2026-09-08 08:03:42'),
(7, 1, 'Cartas sin Destino', 'cartas-sin-destino', 'Desde España, un relato conmovedor sobre la distancia, la inmigración juvenil y los lazos que persisten a través del tiempo.', 2025, 'INTERNACIONAL', 'Drama', '10:05', 'IES Gabriel Ferrater', 'Reus', 'Cataluña', 'España', 'Pau Martí', '["Elena Soler", "Arnau Rovira"]', 'Prof. Xavier Puig', 'images/Carresel18.jpeg', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '["Mejor Cortometraje Internacional"]', 1, 'PUBLISHED', '2026-09-08 08:03:42');

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edition_id` int(11) NOT NULL,
  `day_date` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_time` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `speaker_or_host` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `featured` tinyint(4) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `edition_id` (`edition_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `events` (`id`, `edition_id`, `day_date`, `start_time`, `end_time`, `title`, `description`, `location`, `type`, `speaker_or_host`, `featured`, `created_at`) VALUES
(1, 1, '2026-10-15', '09:00', '10:30', 'Apertura Oficial 18ª Edición & Alfombra Roja', 'Recepción de delegaciones estudiantiles de todo el país, acto de apertura institucional y corte de cinta en el Centro Cultural San Martín.', 'Centro Cultural Gral. San Martín', 'OTRO', 'Comisión Directiva ISO & Autoridades', 1, '2026-09-08 08:03:42'),
(2, 1, '2026-10-15', '11:00', '13:00', 'Bloque 1: Muestra Oficial de Ficción', 'Primera sesión de proyecciones competitivas de cortometrajes de ficción realizados por escuelas secundarias.', 'Sala Cine Teatro Victoria', 'PROYECCION', 'Jurado Oficial de Ficción', 1, '2026-09-08 08:03:42'),
(3, 1, '2026-10-15', '15:00', '17:30', 'Taller: De la Idea al Guión Cinematográfico', 'Espacio formativo y práctico dictado por docentes del Polo Audiovisual Córdoba sobre estructura dramática para jóvenes realizadores.', 'Auditorio Instituto Secundario Oncativo', 'TALLER', 'Polo Audiovisual Córdoba', 0, '2026-09-08 08:03:42'),
(4, 1, '2026-10-15', '18:00', '20:30', 'Bloque 2: Muestra Federal & Debate Abierto', 'Proyección de producciones regionales que retratan identidades locales de diferentes provincias con ronda de preguntas entre directores.', 'Sala Cine Teatro Victoria', 'PROYECCION', 'Equipo Cine Tiza', 0, '2026-09-08 08:03:42'),
(5, 1, '2026-10-16', '09:30', '12:00', 'Bloque 3: Documentales & Animación', 'Exhibición de cortometrajes documentales y animación stop-motion/digital.', 'Sala Cine Teatro Victoria', 'PROYECCION', 'Jurado de Documental y Animación', 1, '2026-09-08 08:03:42'),
(6, 1, '2026-10-16', '14:30', '16:30', 'Taller: Sonido Directo y Banda Sonora', 'Clínica intensiva sobre grabación de sonido en rodajes escolares, microfonía y diseño sonoro.', 'Laboratorio Multimedia ProA', 'TALLER', 'Especialistas Invitados', 0, '2026-09-08 08:03:42'),
(7, 1, '2026-10-16', '17:00', '18:30', 'Charla Magistral: El Futuro del Cine Joven', 'Encuentro y debate entre directores consagrados y realizadores estudiantiles sobre el salto al cine profesional.', 'Centro Cultural San Martín', 'CHARLA', 'Realizadores Cordobeses Destacados', 0, '2026-09-08 08:03:42'),
(8, 1, '2026-10-16', '19:30', '22:00', 'Noche de Videoclips & Arte Urbano', 'Proyecciones de videoclips musicales en pantalla gigante con intervenciones musicales en vivo de bandas escolares.', 'Patio de las Artes ISO', 'MUSICA', 'Bandas y Realizadores Invitados', 1, '2026-09-08 08:03:42'),
(9, 1, '2026-10-17', '10:00', '12:30', 'Bloque 4: Certamen Internacional Cine Tiza', 'Proyección de cortometrajes seleccionados de instituciones educativas de Iberoamérica.', 'Sala Cine Teatro Victoria', 'PROYECCION', 'Jurado Internacional', 1, '2026-09-08 08:03:42'),
(10, 1, '2026-10-17', '15:00', '17:00', 'Foro de Intercambio y Red de Festivales', 'Mesa de trabajo entre docentes y estudiantes para consolidar la red nacional de festivales escolares.', 'Auditorio ISO', 'ARTE', 'Comunidad Docente y ABC Cine', 0, '2026-09-08 08:03:42'),
(11, 1, '2026-10-17', '19:00', '22:00', 'Gala de Clausura & Entrega de Premios 2026', 'Ceremonia oficial de premiación, entrega de estatuillas Tiza de Oro, menciones especiales y anuncio de clasificados internacionales.', 'Sala Cine Teatro Victoria', 'PREMIACION', 'Comisión Cine Tiza & Jurado Oficial', 1, '2026-09-08 08:03:42');

DROP TABLE IF EXISTS `awards`;
CREATE TABLE `awards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edition_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `category_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `winner_film_title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `director` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `badge_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `edition_id` (`edition_id`),
  CONSTRAINT `awards_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `awards` (`id`, `edition_id`, `year`, `category_name`, `winner_film_title`, `institution`, `director`, `badge_url`, `notes`, `created_at`) VALUES
(1, 1, 2025, 'Mejor Cortometraje Ficción', 'Turno Noche', 'Instituto Secundario Oncativo', 'Facundo Rossi', 'images/Logo_CineTiza.png', 'Ganador por unanimidad de jurado técnico', '2026-09-08 08:03:42'),
(2, 1, 2025, 'Mejor Cortometraje Documental', 'Voces del Telar', 'IPEM 142 Joaquín V. González', 'Clara Méndez', 'images/Logo_CineTiza.png', 'Reconocimiento a la preservación cultural', '2026-09-08 08:03:42'),
(3, 1, 2025, 'Mejor Animación', 'Ecos de Tiza', 'Escuela ProA Oncativo', 'Julieta Molina', 'images/Logo_CineTiza.png', 'Destacada técnica en stop motion', '2026-09-08 08:03:42'),
(4, 1, 2025, 'Mejor Cortometraje Internacional', 'Cartas sin Destino', 'IES Gabriel Ferrater (España)', 'Pau Martí', 'images/Logo_CineTiza.png', 'Clasificado para certamen iberoamericano', '2026-09-08 08:03:42'),
(5, 1, 2024, 'Mejor Cortometraje Ficción', 'Las Puertas del Tiempo', 'IPEM 338 Dr. Salvador Mazza', 'Tomás Navarro', 'images/Logo_CineTiza.png', 'Representante oficial en Cinedfest Tenerife', '2026-09-08 08:03:42'),
(6, 1, 2024, 'Premio del Público', 'SmartBoy', 'Instituto Secundario Oncativo', 'Valentina Pérez', 'images/Logo_CineTiza.png', 'Voto popular en sala llena', '2026-09-08 08:03:42');

DROP TABLE IF EXISTS `gallery`;
CREATE TABLE `gallery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edition_id` int(11) NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'IMAGE',
  `media_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `caption` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `edition_id` (`edition_id`),
  CONSTRAINT `gallery_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `gallery` (`id`, `edition_id`, `title`, `category`, `media_type`, `media_url`, `caption`, `created_at`) VALUES
(1, 1, 'Apertura Oficial en Sala Victoria', 'FESTIVAL', 'IMAGE', 'images/Carresel1.png', 'Recepción y sala colmada en Oncativo', '2026-09-08 08:03:42'),
(2, 1, 'Taller de Animación y Cámara', 'TALLERES', 'IMAGE', 'images/Carresel2.png', 'Estudiantes explorando técnicas de filmación', '2026-09-08 08:03:42'),
(3, 1, 'Proyección en Pantalla Gigante', 'PROYECCIONES', 'IMAGE', 'images/Carresel3.png', 'El público disfrutando de las producciones en competencia', '2026-09-08 08:03:42'),
(4, 1, 'Entrega de Premios y Distinciones', 'PREMIACION', 'IMAGE', 'images/Carresel4.png', 'Momento emotivo de la entrega de trofeos Tiza', '2026-09-08 08:03:42'),
(5, 1, 'Backstage de Rodaje Estudiantil', 'BACKSTAGE', 'IMAGE', 'images/Carresel5.png', 'Detrás de escena de los cortometrajes participantes', '2026-09-08 08:03:42'),
(6, 1, 'Delegaciones de Todo el País', 'PARTICIPANTES', 'IMAGE', 'images/Carresel6.png', 'Jóvenes de diferentes provincias en Oncativo', '2026-09-08 08:03:42'),
(7, 1, 'Comunidad ISO y Organizadores', 'FESTIVAL', 'IMAGE', 'images/Carresel8.png', 'El equipo docente y estudiantil del Instituto Secundario Oncativo', '2026-09-08 08:03:42'),
(8, 1, 'Muestra de Cortos de Ficción', 'PROYECCIONES', 'IMAGE', 'images/Carresel9.png', 'Debate posterior a la proyección de ficción', '2026-09-08 08:03:42'),
(9, 1, 'Jornada de Formación Audiovisual', 'TALLERES', 'IMAGE', 'images/Carresel10.png', 'Prácticas de sonido e iluminación', '2026-09-08 08:03:42'),
(10, 1, 'Alfombra Roja y Registro de Medios', 'BACKSTAGE', 'IMAGE', 'images/Carresel19.jpeg', 'Entrevistas en vivo antes de la función de gala', '2026-09-08 08:03:42'),
(11, 1, 'Celebración y Encuentro Joven', 'PARTICIPANTES', 'IMAGE', 'images/Carresel20.jpeg', 'Intercambio cultural entre realizadores adolescentes', '2026-09-08 08:03:42'),
(12, 1, 'Cierre de la 17ª Edición', 'PREMIACION', 'IMAGE', 'images/Carresel21.jpeg', 'Foto grupal con todas las delegaciones participantes', '2026-09-08 08:03:42');

DROP TABLE IF EXISTS `submissions`;
CREATE TABLE `submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `film_title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `province` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Argentina',
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `genre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `director` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `participants` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `teacher` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `synopsis` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `thumbnail_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'PENDIENTE',
  `admin_notes` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `terms_accepted` tinyint(4) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `submissions` (`id`, `film_title`, `institution`, `city`, `province`, `country`, `category`, `genre`, `duration`, `director`, `participants`, `teacher`, `email`, `phone`, `synopsis`, `video_url`, `thumbnail_url`, `status`, `admin_notes`, `terms_accepted`, `created_at`) VALUES
(1, 'Memorias de Arcilla', 'Instituto Secundario Oncativo', 'Oncativo', 'Córdoba', 'Argentina', 'FICCION', 'Drama', '10:15', 'Lucas Morales', '5 alumnos de 5to año', 'Prof. Mariano Rossi', 'inscripciones@isooncativo.edu.ar', '+54 3572 455000', 'Un emotivo retrato sobre el legado artesanal de una familia y el desafío de las nuevas generaciones.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'images/Carresel12.jpeg', 'APROBADO', 'Aprobado para Muestra Oficial 2026.', 1, '2026-09-08 08:03:42'),
(2, 'Horizonte Verde', 'Colegio Nacional Villa María', 'Villa María', 'Córdoba', 'Argentina', 'DOCUMENTAL', 'Ambiental', '13:40', 'Candela Herrera', 'Equipo de Comunicación 6to B', 'Prof. Claudia Paz', 'candela.herrera@email.com', '+54 353 4201122', 'Investigación sobre la recuperación de flora autóctona en la llanura cordobesa.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'images/Carresel13.jpeg', 'EN_REVISION', 'Pendiente de confirmación de autorización de derechos de música.', 1, '2026-09-08 08:03:42'),
(3, 'Sombras en el Recreo', 'Escuela Técnica N° 1', 'Rosario', 'Santa Fe', 'Argentina', 'ANIMACION', 'Stop Motion', '07:20', 'Esteban D\'Amico', 'Grupo Taller Audiovisual', 'Prof. Sergio Varela', 'esteban.damico@rosario.edu.ar', '+54 341 4889900', 'Una animación lúdica que cobra vida con elementos escolares cotidianos.', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'images/Carresel14.jpeg', 'FINALISTA', 'Seleccionado como finalista en Certamen de Animación.', 1, '2026-09-08 08:03:42'),
(4, 'Cortometraje Test MySQL', 'Instituto Oncativo', 'Oncativo', 'Córdoba', 'Argentina', 'FICCION', 'General', '10:00', 'Tester Alumno', '', '', 'alumno@test.com', '', '', 'https://youtube.com/watch?v=12345', 'images/Logo_CineTiza.png', 'APROBADO', 'Aprobado vía MySQL test', 1, '2026-09-08 08:15:02');

DROP TABLE IF EXISTS `contact_messages`;
CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(4) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `contact_messages` (`id`, `name`, `email`, `subject`, `message`, `is_read`, `created_at`) VALUES
(2, 'Profesor Consulta', 'profe@escuela.edu.ar', 'Consulta Inscripciones 2026', 'Hola, queremos saber si podemos inscribir 2 cortos.', 0, '2026-09-08 08:15:04'),
(3, 'Profesor Consulta', 'profe@escuela.edu.ar', 'Consulta Inscripciones 2026', 'Hola, queremos saber si podemos inscribir 2 cortos.', 0, '2026-09-08 08:20:18');

DROP TABLE IF EXISTS `admin_users`;
CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ADMIN',
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `admin_users` (`id`, `username`, `password_hash`, `role`, `full_name`, `email`, `created_at`) VALUES
(1, 'admin', '529de689ad6318be65fb1bde2eb99e64$fc0a126a8fc4fddaf1b3888220f52a58cbfa9f14550c4d55493dca72f328e7e4', 'ADMIN', 'Comisión Organizadora Cine Tiza', 'festivalcinetiza@gmail.com', '2026-09-08 08:03:42'),
(2, 'editor', '92345ac01cf85026bb9b5bd0bcc81e91$6e729058dbd44862f72953a657a955146bdfd5b0731739ac570f46a9703936c8', 'EDITOR', 'Equipo Editorial ISO', 'prensa@cinetiza.com.ar', '2026-09-08 08:03:42');

SET FOREIGN_KEY_CHECKS = 1;
