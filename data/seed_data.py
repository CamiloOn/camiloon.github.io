"""
Database initialization and factual seed data for Cine Tiza Festival
(Festival Internacional de Cine y Artes Estudiantiles - Oncativo, Córdoba, Argentina)
Organizado por la comunidad educativa del Instituto Secundario Oncativo (ISO).
"""

import sqlite3
import os
import hashlib
import hmac
import json
import secrets

DB_PATH = os.path.join(os.path.dirname(__file__), "cinetiza.db")

def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        salt = secrets.token_hex(16)
    # PBKDF2 HMAC SHA-256 with 100,000 iterations
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Site Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    # 2. Editions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS editions (
        id INTEGER PRIMARY KEY,
        number INTEGER NOT NULL UNIQUE,
        year INTEGER NOT NULL UNIQUE,
        title TEXT NOT NULL,
        theme TEXT,
        description TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        poster_url TEXT,
        hero_image_url TEXT,
        films_count INTEGER DEFAULT 0,
        schools_count INTEGER DEFAULT 0,
        attendees_count INTEGER DEFAULT 0,
        featured INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Films
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edition_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        synopsis TEXT NOT NULL,
        year INTEGER NOT NULL,
        category TEXT NOT NULL,
        genre TEXT NOT NULL,
        duration TEXT NOT NULL,
        institution TEXT NOT NULL,
        city TEXT NOT NULL,
        province TEXT NOT NULL,
        country TEXT NOT NULL DEFAULT 'Argentina',
        director TEXT NOT NULL,
        cast_and_crew TEXT,
        teacher_guide TEXT,
        thumbnail_url TEXT,
        video_url TEXT,
        awards TEXT,
        featured INTEGER DEFAULT 0,
        status TEXT DEFAULT 'PUBLISHED',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (edition_id) REFERENCES editions (id)
    )
    """)

    # 4. Events (Agenda)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edition_id INTEGER NOT NULL,
        day_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        speaker_or_host TEXT,
        featured INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (edition_id) REFERENCES editions (id)
    )
    """)

    # 5. Awards
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS awards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edition_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        winner_film_title TEXT NOT NULL,
        institution TEXT NOT NULL,
        director TEXT NOT NULL,
        badge_url TEXT,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (edition_id) REFERENCES editions (id)
    )
    """)

    # 6. Submissions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        film_title TEXT NOT NULL,
        institution TEXT NOT NULL,
        city TEXT NOT NULL,
        province TEXT NOT NULL,
        country TEXT NOT NULL DEFAULT 'Argentina',
        category TEXT NOT NULL,
        genre TEXT NOT NULL,
        duration TEXT NOT NULL,
        director TEXT NOT NULL,
        participants TEXT NOT NULL,
        teacher TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        synopsis TEXT NOT NULL,
        video_url TEXT NOT NULL,
        thumbnail_url TEXT,
        status TEXT DEFAULT 'PENDIENTE',
        admin_notes TEXT,
        terms_accepted INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Gallery
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gallery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edition_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        media_type TEXT DEFAULT 'IMAGE',
        media_url TEXT NOT NULL,
        caption TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (edition_id) REFERENCES editions (id)
    )
    """)

    # 8. Contact Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Admin Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'ADMIN',
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed Default Data if empty
    seed_data(cursor, conn)
    conn.close()
    print("Database schema and seed data initialized successfully.")

def seed_data(cursor, conn):
    # Check if admin user exists
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    if cursor.fetchone()[0] == 0:
        admin_hash = hash_password("cinetiza2026")
        editor_hash = hash_password("editor2026")
        cursor.execute("""
        INSERT INTO admin_users (username, password_hash, role, full_name, email)
        VALUES 
        ('admin', ?, 'ADMIN', 'Comisión Organizadora Cine Tiza', 'festivalcinetiza@gmail.com'),
        ('editor', ?, 'EDITOR', 'Equipo Editorial ISO', 'prensa@cinetiza.com.ar')
        """, (admin_hash, editor_hash))

    # Site Settings
    cursor.execute("SELECT COUNT(*) FROM site_settings")
    if cursor.fetchone()[0] == 0:
        settings = {
            "festival_name": "Cine Tiza",
            "full_title": "Festival Internacional de Cine y Artes Estudiantiles",
            "edition_number": "18",
            "edition_year": "2026",
            "start_date": "2026-10-15T09:00:00",
            "end_date": "2026-10-17T22:00:00",
            "submissions_open": "true",
            "submissions_start": "2026-03-16",
            "submissions_deadline": "2026-08-28",
            "location_city": "Oncativo",
            "location_province": "Córdoba",
            "location_country": "Argentina",
            "main_venue": "Centro Cultural Gral. San Martín & Sala Teatro Victoria",
            "organizer": "Instituto Secundario Oncativo (ISO)",
            "collaborators": "Grupo ABC Cine, Escuela ProA Oncativo, Polo Audiovisual Córdoba, Municipalidad de Oncativo",
            "contact_email": "festivalcinetiza@gmail.com",
            "instagram_url": "https://www.instagram.com/cinetiza/",
            "youtube_url": "https://www.youtube.com/@FestivalCineTiza",
            "facebook_url": "https://www.facebook.com/festivalcinetiza",
            "hero_badge": "18ª EDICIÓN · 15 — 17 OCTUBRE 2026",
            "hero_tagline": "UNA PANTALLA PARA LAS NUEVAS VOCES",
            "stat_years": "18",
            "stat_schools": "100+",
            "stat_films": "260+",
            "stat_days": "3"
        }
        for k, v in settings.items():
            cursor.execute("INSERT OR REPLACE INTO site_settings (key, value) VALUES (?, ?)", (k, v))

    # Editions (1st in 2009 to 18th in 2026)
    cursor.execute("SELECT COUNT(*) FROM editions")
    if cursor.fetchone()[0] == 0:
        editions_data = [
            (18, 2026, "18ª Edición Cine Tiza", "Historias que Transforman", 
             "La 18ª edición del Festival Internacional de Cine y Artes Estudiantiles reúne a realizadores de escuelas secundarias de todo el país y el exterior en Oncativo, Córdoba.",
             "2026-10-15", "2026-10-17", "images/Centro2026.jpeg", "images/Centro2026.jpeg", 35, 28, 1200, 1),
            (17, 2025, "17ª Edición Cine Tiza", "Voces en Movimiento",
             "Edición marcada por la consolidación del certamen internacional y talleres audiovisuales con profesionales del Polo Audiovisual.",
             "2025-10-16", "2025-10-18", "images/Carresel1.png", "images/Carresel1.png", 32, 24, 1100, 0),
            (16, 2024, "16ª Edición Cine Tiza", "Nuevas Miradas",
             "Celebración de los 15 años de trayectoria con récord de instituciones participantes y gran muestra federal.",
             "2024-10-17", "2024-10-19", "images/Carresel2.png", "images/Carresel2.png", 30, 22, 950, 0),
            (15, 2023, "15ª Edición Cine Tiza", "El Cine en las Aulas",
             "Encuentro que profundizó la capacitación pedagógica y técnica de estudiantes y docentes de nivel secundario.",
             "2023-10-12", "2023-10-14", "images/Carresel3.png", "images/Carresel3.png", 28, 20, 900, 0),
            (14, 2022, "14ª Edición Cine Tiza", "Reencuentro Audiovisual",
             "El regreso a las salas llenas en el Teatro Victoria de Oncativo tras las etapas virtuales.",
             "2022-10-13", "2022-10-15", "images/Carresel4.png", "images/Carresel4.png", 26, 18, 850, 0),
            (13, 2021, "13ª Edición Cine Tiza", "Pantallas Conectadas",
             "Edición híbrida con proyecciones federales y streaming en vivo para toda la comunidad latinoamericana.",
             "2021-10-14", "2021-10-16", "images/Carresel5.png", "images/Carresel5.png", 24, 16, 750, 0),
            (12, 2020, "12ª Edición Cine Tiza", "Crear en Tiempos de Cambio",
             "Adaptación virtual completa que unió a estudiantes a través de producciones audiovisuales desde sus hogares.",
             "2020-10-15", "2020-10-17", "images/Carresel6.png", "images/Carresel6.png", 22, 15, 600, 0),
            (1, 2009, "1ª Edición Cine Tiza", "El Nacimiento de un Sueño",
             "Nace Cine Tiza en el Instituto Secundario Oncativo (ISO) como una iniciativa de expresión e intercambio cultural para jóvenes.",
             "2009-10-10", "2009-10-11", "images/Logo_CineTiza.png", "images/Logo_CineTiza.png", 8, 4, 250, 0)
        ]
        for e in editions_data:
            cursor.execute("""
            INSERT INTO editions (number, year, title, theme, description, start_date, end_date, poster_url, hero_image_url, films_count, schools_count, attendees_count, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, e)

    # Films (Historical & Featured)
    cursor.execute("SELECT COUNT(*) FROM films")
    if cursor.fetchone()[0] == 0:
        films_data = [
            (18, "Turno Noche", "turno-noche", 
             "Un grupo de estudiantes descubre un misterio en los pasillos de su escuela secundaria durante una jornada extracurricular. Una atmósfera de suspenso construida con maestría lumínica y sonora.",
             2025, "FICCION", "Suspenso / Drama", "11:42", "Instituto Secundario Oncativo (ISO)", "Oncativo", "Córdoba", "Argentina",
             "Facundo Rossi & Equipo 6° Año", json.dumps(["Camila Díaz (Sonido)", "Mateo Luna (Fotografía)", "Lucía Gómez (Montaje)"]),
             "Prof. Laura Martínez", "images/Carresel11.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Cortometraje Ficción 2025", "Mejor Fotografía", "Mejor Sonido"]), 1, "PUBLISHED"),

            (18, "SmartBoy", "smartboy",
             "Sátira distópica sobre la hiperconexión digital en la juventud y los límites entre la identidad real y el algoritmo escolar.",
             2025, "FICCION", "Comedia / Ciencia Ficción", "09:15", "Instituto Secundario Oncativo (ISO)", "Oncativo", "Córdoba", "Argentina",
             "Valentina Pérez", json.dumps(["Joaquín Alvarez (Actuación)", "Sofía Benítez (Arte)"]),
             "Prof. Martín Almada", "images/Carresel12.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mención Especial Guión Original", "Premio del Público"]), 1, "PUBLISHED"),

            (18, "Las Puertas del Tiempo", "las-puertas-del-tiempo",
             "Un viaje documental que rescata la memoria ferroviaria y los relatos orales de los pioneros de la región pampeana cordobesa.",
             2024, "DOCUMENTAL", "Histórico / Social", "14:20", "IPEM 338 Dr. Salvador Mazza", "Córdoba", "Córdoba", "Argentina",
             "Tomás Navarro & Taller Audiovisual", json.dumps(["Estudiantes 5° Año IPEM 338"]),
             "Prof. Gabriel Fernández", "images/Carresel13.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Documental 16ª Edición", "Seleccionado para Cinedfest España"]), 1, "PUBLISHED"),

            (18, "Ecos de Tiza", "ecos-de-tiza",
             "Cortometraje de animación stop-motion con plastilina y papel que explora las emociones adolescentes y la presión del futuro.",
             2025, "ANIMACION", "Stop Motion / Experimental", "06:50", "Escuela ProA Oncativo", "Oncativo", "Córdoba", "Argentina",
             "Julieta Molina", json.dumps(["Nicolás Vega (Animación)", "Ana Clara Ríos (Música Original)"]),
             "Prof. Roberto Sánchez", "images/Carresel14.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Animación 17ª Edición"]), 1, "PUBLISHED"),

            (18, "Frecuencia Joven", "frecuencia-joven",
             "Videoclip rítmico y conceptual que acompaña la composición musical original de una banda estudiantil sobre la libertad de expresión.",
             2024, "VIDEOCLIP", "Musical / Urbano", "04:30", "Instituto Manuel Belgrano", "Oliva", "Córdoba", "Argentina",
             "Ignacio Ceballos", json.dumps(["Banda 'Sin Timbre'", "Equipo Técnico Belgrano"]),
             "Prof. Cecilia Morales", "images/Carresel15.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Videoclip"]), 0, "PUBLISHED"),

            (18, "Raíces del Valle", "raices-del-valle",
             "Muestra Federal que retrata las tradiciones comunitarias y la preservación del monte nativo contada por jóvenes serranos.",
             2025, "MUESTRA_FEDERAL", "Documental Territorial", "12:10", "IPEM 142 Joaquín V. González", "San Marcos Sierras", "Córdoba", "Argentina",
             "Lara Soria", json.dumps(["Comunidad Educativa IPEM 142"]),
             "Prof. Marcelo Castro", "images/Carresel17.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Destacado Muestra Federal"]), 0, "PUBLISHED"),

            (18, "Cartas sin Destino", "cartas-sin-destino",
             "Desde España, un relato conmovedor sobre la distancia, la inmigración juvenil y los lazos que persisten a través del tiempo.",
             2025, "INTERNACIONAL", "Drama", "10:05", "IES Gabriel Ferrater", "Reus", "Cataluña", "España",
             "Pau Martí", json.dumps(["Elena Soler", "Arnau Rovira"]),
             "Prof. Xavier Puig", "images/Carresel18.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Cortometraje Internacional"]), 1, "PUBLISHED")
        ]

        for f in films_data:
            cursor.execute("""
            INSERT INTO films (edition_id, title, slug, synopsis, year, category, genre, duration, institution, city, province, country, director, cast_and_crew, teacher_guide, thumbnail_url, video_url, awards, featured, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, f)

    # Events (18th Edition Agenda: 15, 16, 17 Octubre 2026)
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        events_data = [
            # Day 1: 15 Octubre 2026
            (18, "2026-10-15", "09:00", "10:30", "Apertura Oficial 18ª Edición & Alfombra Roja",
             "Recepción de delegaciones estudiantiles de todo el país, acto de apertura institucional y corte de cinta en el Centro Cultural San Martín.",
             "Centro Cultural Gral. San Martín", "OTRO", "Comisión Directiva ISO & Autoridades", 1),
            (18, "2026-10-15", "11:00", "13:00", "Bloque 1: Muestra Oficial de Ficción",
             "Primera sesión de proyecciones competitivas de cortometrajes de ficción realizados por escuelas secundarias.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado Oficial de Ficción", 1),
            (18, "2026-10-15", "15:00", "17:30", "Taller: De la Idea al Guión Cinematográfico",
             "Espacio formativo y práctico dictado por docentes del Polo Audiovisual Córdoba sobre estructura dramática para jóvenes realizadores.",
             "Auditorio Instituto Secundario Oncativo", "TALLER", "Polo Audiovisual Córdoba", 0),
            (18, "2026-10-15", "18:00", "20:30", "Bloque 2: Muestra Federal & Debate Abierto",
             "Proyección de producciones regionales que retratan identidades locales de diferentes provincias con ronda de preguntas entre directores.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Equipo Cine Tiza", 0),

            # Day 2: 16 Octubre 2026
            (18, "2026-10-16", "09:30", "12:00", "Bloque 3: Documentales & Animación",
             "Exhibición de cortometrajes documentales y animación stop-motion/digital.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado de Documental y Animación", 1),
            (18, "2026-10-16", "14:30", "16:30", "Taller: Sonido Directo y Banda Sonora",
             "Clínica intensiva sobre grabación de sonido en rodajes escolares, microfonía y diseño sonoro.",
             "Laboratorio Multimedia ProA", "TALLER", "Especialistas Invitados", 0),
            (18, "2026-10-16", "17:00", "18:30", "Charla Magistral: El Futuro del Cine Joven",
             "Encuentro y debate entre directores consagrados y realizadores estudiantiles sobre el salto al cine profesional.",
             "Centro Cultural San Martín", "CHARLA", "Realizadores Cordobeses Destacados", 0),
            (18, "2026-10-16", "19:30", "22:00", "Noche de Videoclips & Arte Urbano",
             "Proyecciones de videoclips musicales en pantalla gigante con intervenciones musicales en vivo de bandas escolares.",
             "Patio de las Artes ISO", "MUSICA", "Bandas y Realizadores Invitados", 1),

            # Day 3: 17 Octubre 2026
            (18, "2026-10-17", "10:00", "12:30", "Bloque 4: Certamen Internacional Cine Tiza",
             "Proyección de cortometrajes seleccionados de instituciones educativas de Iberoamérica.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado Internacional", 1),
            (18, "2026-10-17", "15:00", "17:00", "Foro de Intercambio y Red de Festivales",
             "Mesa de trabajo entre docentes y estudiantes para consolidar la red nacional de festivales escolares.",
             "Auditorio ISO", "ARTE", "Comunidad Docente y ABC Cine", 0),
            (18, "2026-10-17", "19:00", "22:00", "Gala de Clausura & Entrega de Premios 2026",
             "Ceremonia oficial de premiación, entrega de estatuillas Tiza de Oro, menciones especiales y anuncio de clasificados internacionales.",
             "Sala Cine Teatro Victoria", "PREMIACION", "Comisión Cine Tiza & Jurado Oficial", 1)
        ]

        for ev in events_data:
            cursor.execute("""
            INSERT INTO events (edition_id, day_date, start_time, end_time, title, description, location, type, speaker_or_host, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ev)

    # Awards History
    cursor.execute("SELECT COUNT(*) FROM awards")
    if cursor.fetchone()[0] == 0:
        awards_data = [
            (18, 2025, "Mejor Cortometraje Ficción", "Turno Noche", "Instituto Secundario Oncativo", "Facundo Rossi", "images/Logo_CineTiza.png", "Ganador por unanimidad de jurado técnico"),
            (18, 2025, "Mejor Cortometraje Documental", "Voces del Telar", "IPEM 142 Joaquín V. González", "Clara Méndez", "images/Logo_CineTiza.png", "Reconocimiento a la preservación cultural"),
            (18, 2025, "Mejor Animación", "Ecos de Tiza", "Escuela ProA Oncativo", "Julieta Molina", "images/Logo_CineTiza.png", "Destacada técnica en stop motion"),
            (18, 2025, "Mejor Cortometraje Internacional", "Cartas sin Destino", "IES Gabriel Ferrater (España)", "Pau Martí", "images/Logo_CineTiza.png", "Clasificado para certamen iberoamericano"),
            (18, 2024, "Mejor Cortometraje Ficción", "Las Puertas del Tiempo", "IPEM 338 Dr. Salvador Mazza", "Tomás Navarro", "images/Logo_CineTiza.png", "Representante oficial en Cinedfest Tenerife"),
            (18, 2024, "Premio del Público", "SmartBoy", "Instituto Secundario Oncativo", "Valentina Pérez", "images/Logo_CineTiza.png", "Voto popular en sala llena")
        ]
        for aw in awards_data:
            cursor.execute("""
            INSERT INTO awards (edition_id, year, category_name, winner_film_title, institution, director, badge_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, aw)

    # Gallery (Curated with real assets)
    cursor.execute("SELECT COUNT(*) FROM gallery")
    if cursor.fetchone()[0] == 0:
        gallery_data = [
            (18, "Apertura Oficial en Sala Victoria", "FESTIVAL", "IMAGE", "images/Carresel1.png", "Recepción y sala colmada en Oncativo"),
            (18, "Taller de Animación y Cámara", "TALLERES", "IMAGE", "images/Carresel2.png", "Estudiantes explorando técnicas de filmación"),
            (18, "Proyección en Pantalla Gigante", "PROYECCIONES", "IMAGE", "images/Carresel3.png", "El público disfrutando de las producciones en competencia"),
            (18, "Entrega de Premios y Distinciones", "PREMIACION", "IMAGE", "images/Carresel4.png", "Momento emotivo de la entrega de trofeos Tiza"),
            (18, "Backstage de Rodaje Estudiantil", "BACKSTAGE", "IMAGE", "images/Carresel5.png", "Detrás de escena de los cortometrajes participantes"),
            (18, "Delegaciones de Todo el País", "PARTICIPANTES", "IMAGE", "images/Carresel6.png", "Jóvenes de diferentes provincias en Oncativo"),
            (18, "Comunidad ISO y Organizadores", "FESTIVAL", "IMAGE", "images/Carresel8.png", "El equipo docente y estudiantil del Instituto Secundario Oncativo"),
            (18, "Muestra de Cortos de Ficción", "PROYECCIONES", "IMAGE", "images/Carresel9.png", "Debate posterior a la proyección de ficción"),
            (18, "Jornada de Formación Audiovisual", "TALLERES", "IMAGE", "images/Carresel10.png", "Prácticas de sonido e iluminación"),
            (18, "Alfombra Roja y Registro de Medios", "BACKSTAGE", "IMAGE", "images/Carresel19.jpeg", "Entrevistas en vivo antes de la función de gala"),
            (18, "Celebración y Encuentro Joven", "PARTICIPANTES", "IMAGE", "images/Carresel20.jpeg", "Intercambio cultural entre realizadores adolescentes"),
            (18, "Cierre de la 17ª Edición", "PREMIACION", "IMAGE", "images/Carresel21.jpeg", "Foto grupal con todas las delegaciones participantes")
        ]
        for g in gallery_data:
            cursor.execute("""
            INSERT INTO gallery (edition_id, title, category, media_type, media_url, caption)
            VALUES (?, ?, ?, ?, ?, ?)
            """, g)

    # Submissions Seed (for admin management showcase)
    cursor.execute("SELECT COUNT(*) FROM submissions")
    if cursor.fetchone()[0] == 0:
        sub_data = [
            ("Memorias de Arcilla", "Instituto Secundario Oncativo", "Oncativo", "Córdoba", "Argentina", "FICCION", "Drama", "10:15",
             "Lucas Morales", "5 alumnos de 5to año", "Prof. Mariano Rossi", "inscripciones@isooncativo.edu.ar", "+54 3572 455000",
             "Un emotivo retrato sobre el legado artesanal de una familia y el desafío de las nuevas generaciones.",
             "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "images/Carresel12.jpeg", "APROBADO", "Aprobado para Muestra Oficial 2026.", 1),
            ("Horizonte Verde", "Colegio Nacional Villa María", "Villa María", "Córdoba", "Argentina", "DOCUMENTAL", "Ambiental", "13:40",
             "Candela Herrera", "Equipo de Comunicación 6to B", "Prof. Claudia Paz", "candela.herrera@email.com", "+54 353 4201122",
             "Investigación sobre la recuperación de flora autóctona en la llanura cordobesa.",
             "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "images/Carresel13.jpeg", "EN_REVISION", "Pendiente de confirmación de autorización de derechos de música.", 1),
            ("Sombras en el Recreo", "Escuela Técnica N° 1", "Rosario", "Santa Fe", "Argentina", "ANIMACION", "Stop Motion", "07:20",
             "Esteban D'Amico", "Grupo Taller Audiovisual", "Prof. Sergio Varela", "esteban.damico@rosario.edu.ar", "+54 341 4889900",
             "Una animación lúdica que cobra vida con elementos escolares cotidianos.",
             "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "images/Carresel14.jpeg", "FINALISTA", "Seleccionado como finalista en Certamen de Animación.", 1)
        ]
        for s in sub_data:
            cursor.execute("""
            INSERT INTO submissions (film_title, institution, city, province, country, category, genre, duration, director, participants, teacher, email, phone, synopsis, video_url, thumbnail_url, status, admin_notes, terms_accepted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, s)

    conn.commit()

if __name__ == "__main__":
    init_db()
