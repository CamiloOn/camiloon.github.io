"""
MySQL Database Connector and Layer for Cine Tiza Platform
Connects to XAMPP MySQL (host: 127.0.0.1:3306, user: root, database: cinetiza_db)
Provides SQLite-compatible Row objects (supports both r['col'] and r[0], dict(r), etc.)
"""

import os
import pymysql
import pymysql.cursors
import json
import hashlib
import secrets

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DB = os.environ.get("MYSQL_DB", "cinetiza_db")

def hash_password(password: str, salt: str = None) -> str:
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"

import datetime

class MySQLRow(dict):
    """
    SQLite-like Row object for MySQL results.
    Allows accessing columns by name: row['title']
    Allows accessing columns by index: row[0]
    Allows converting to dict: dict(row)
    Automatically converts datetime objects to ISO strings.
    """
    def __init__(self, data_dict, field_names=None):
        clean_dict = {}
        if data_dict:
            for k, v in data_dict.items():
                if isinstance(v, (datetime.datetime, datetime.date)):
                    clean_dict[k] = v.isoformat()
                elif isinstance(v, bytes):
                    clean_dict[k] = v.decode('utf-8', errors='replace')
                else:
                    clean_dict[k] = v
        super().__init__(clean_dict)
        self._fields = field_names or list(clean_dict.keys())
        self._values = list(clean_dict.values())

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._values[item]
        return super().__getitem__(item)

    def keys(self):
        return super().keys()

    def values(self):
        return super().values()

    def items(self):
        return super().items()

def get_server_connection():
    """Connect to MySQL server without selecting a specific database."""
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        charset='utf8mb4',
        autocommit=False
    )

def ensure_database_exists():
    """Ensure that the cinetiza_db database exists on XAMPP MySQL."""
    conn = get_server_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
    finally:
        conn.close()

import re

class MySQLCursorWrapper:
    """Cursor wrapper that returns MySQLRow instances."""
    def __init__(self, raw_cursor, wrapper_conn):
        self.cursor = raw_cursor
        self.wrapper_conn = wrapper_conn

    def _convert_sql(self, sql: str) -> str:
        sql_converted = sql.replace("?", "%s")
        sql_converted = sql_converted.replace("INSERT OR REPLACE INTO", "REPLACE INTO")
        # Escape MySQL reserved word 'key' if unescaped
        sql_converted = re.sub(r'(?<!`)\bkey\b(?!`)', '`key`', sql_converted)
        return sql_converted

    def execute(self, sql: str, params=None):
        converted_sql = self._convert_sql(sql)
        self.cursor.execute(converted_sql, params or ())
        return self

    def fetchone(self):
        row = self.cursor.fetchone()
        if row is None:
            return None
        return MySQLRow(row)

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [MySQLRow(r) for r in rows]

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()

class MySQLWrapper:
    """Wrapper around PyMySQL connection providing SQLite/Python DB-API compatibility."""
    def __init__(self, raw_conn):
        self.conn = raw_conn

    def cursor(self):
        raw_cur = self.conn.cursor(pymysql.cursors.DictCursor)
        return MySQLCursorWrapper(raw_cur, self)

    def execute(self, sql: str, params=None):
        cur = self.cursor()
        cur.execute(sql, params or ())
        return cur

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

def get_db():
    """Return a wrapped connection to the XAMPP MySQL database."""
    try:
        raw_conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return MySQLWrapper(raw_conn)
    except Exception as e:
        # If DB not found, ensure it exists and retry
        ensure_database_exists()
        raw_conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return MySQLWrapper(raw_conn)

def init_mysql_db():
    """Create all tables and seed data in XAMPP MySQL."""
    ensure_database_exists()
    conn = get_db()
    
    with conn.conn.cursor() as cur:
        # 1. Site Settings
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `site_settings` (
            `key` VARCHAR(191) NOT NULL PRIMARY KEY,
            `value` LONGTEXT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 2. Editions
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `editions` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `number` INT NOT NULL UNIQUE,
            `year` INT NOT NULL UNIQUE,
            `title` VARCHAR(255) NOT NULL,
            `theme` VARCHAR(255) NULL,
            `description` TEXT NOT NULL,
            `start_date` VARCHAR(50) NOT NULL,
            `end_date` VARCHAR(50) NOT NULL,
            `poster_url` VARCHAR(500) NULL,
            `hero_image_url` VARCHAR(500) NULL,
            `films_count` INT DEFAULT 0,
            `schools_count` INT DEFAULT 0,
            `attendees_count` INT DEFAULT 0,
            `featured` TINYINT DEFAULT 0,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 3. Films
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `films` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `edition_id` INT NOT NULL,
            `title` VARCHAR(255) NOT NULL,
            `slug` VARCHAR(191) NOT NULL UNIQUE,
            `synopsis` TEXT NOT NULL,
            `year` INT NOT NULL,
            `category` VARCHAR(100) NOT NULL,
            `genre` VARCHAR(100) NOT NULL,
            `duration` VARCHAR(50) NOT NULL,
            `institution` VARCHAR(255) NOT NULL,
            `city` VARCHAR(100) NOT NULL,
            `province` VARCHAR(100) NOT NULL,
            `country` VARCHAR(100) NOT NULL DEFAULT 'Argentina',
            `director` VARCHAR(255) NOT NULL,
            `cast_and_crew` TEXT NULL,
            `teacher_guide` VARCHAR(255) NULL,
            `thumbnail_url` VARCHAR(500) NULL,
            `video_url` VARCHAR(500) NULL,
            `awards` TEXT NULL,
            `featured` TINYINT DEFAULT 0,
            `status` VARCHAR(50) DEFAULT 'PUBLISHED',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 4. Events (Agenda)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `events` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `edition_id` INT NOT NULL,
            `day_date` VARCHAR(50) NOT NULL,
            `start_time` VARCHAR(50) NOT NULL,
            `end_time` VARCHAR(50) NOT NULL,
            `title` VARCHAR(255) NOT NULL,
            `description` TEXT NOT NULL,
            `location` VARCHAR(255) NOT NULL,
            `type` VARCHAR(100) NOT NULL,
            `speaker_or_host` VARCHAR(255) NULL,
            `featured` TINYINT DEFAULT 0,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 5. Awards
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `awards` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `edition_id` INT NOT NULL,
            `year` INT NOT NULL,
            `category_name` VARCHAR(255) NOT NULL,
            `winner_film_title` VARCHAR(255) NOT NULL,
            `institution` VARCHAR(255) NOT NULL,
            `director` VARCHAR(255) NOT NULL,
            `badge_url` VARCHAR(500) NULL,
            `notes` TEXT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 6. Submissions
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `submissions` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `film_title` VARCHAR(255) NOT NULL,
            `institution` VARCHAR(255) NOT NULL,
            `city` VARCHAR(100) NOT NULL,
            `province` VARCHAR(100) NOT NULL,
            `country` VARCHAR(100) NOT NULL DEFAULT 'Argentina',
            `category` VARCHAR(100) NOT NULL,
            `genre` VARCHAR(100) NOT NULL,
            `duration` VARCHAR(50) NOT NULL,
            `director` VARCHAR(255) NOT NULL,
            `participants` TEXT NOT NULL,
            `teacher` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `phone` VARCHAR(100) NOT NULL,
            `synopsis` TEXT NOT NULL,
            `video_url` VARCHAR(500) NOT NULL,
            `thumbnail_url` VARCHAR(500) NULL,
            `status` VARCHAR(50) DEFAULT 'PENDIENTE',
            `admin_notes` TEXT NULL,
            `terms_accepted` TINYINT DEFAULT 1,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 7. Gallery
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `gallery` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `edition_id` INT NOT NULL,
            `title` VARCHAR(255) NOT NULL,
            `category` VARCHAR(100) NOT NULL,
            `media_type` VARCHAR(50) DEFAULT 'IMAGE',
            `media_url` VARCHAR(500) NOT NULL,
            `caption` TEXT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`edition_id`) REFERENCES `editions` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 8. Contact Messages
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `contact_messages` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `subject` VARCHAR(255) NOT NULL,
            `message` TEXT NOT NULL,
            `is_read` TINYINT DEFAULT 0,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 9. Admin Users
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `admin_users` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `username` VARCHAR(100) NOT NULL UNIQUE,
            `password_hash` VARCHAR(255) NOT NULL,
            `role` VARCHAR(50) NOT NULL DEFAULT 'ADMIN',
            `full_name` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 10. Game Scores — Director's Cut
        cur.execute("""
        CREATE TABLE IF NOT EXISTS `game_scores` (
            `id`         INT AUTO_INCREMENT PRIMARY KEY,
            `nickname`   VARCHAR(30)  NOT NULL,
            `score`      TINYINT UNSIGNED NOT NULL,
            `genre`      VARCHAR(30)  NOT NULL,
            `film_title` VARCHAR(100) NOT NULL,
            `character`  VARCHAR(30)  NOT NULL,
            `location`   VARCHAR(30)  NOT NULL DEFAULT '',
            `decisions`  VARCHAR(20)  NOT NULL,
            `ip_hash`    VARCHAR(64)  NOT NULL DEFAULT '',
            `created_at` DATETIME     DEFAULT CURRENT_TIMESTAMP,
            INDEX `idx_score` (`score` DESC),
            INDEX `idx_created` (`created_at`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

    conn.commit()
    seed_mysql_data(conn)
    conn.close()
    print("[Cine Tiza MySQL] Schema and seed data initialized successfully in XAMPP MySQL database 'cinetiza_db'.")

def seed_mysql_data(conn):
    # 1. Admin Users
    cur = conn.execute("SELECT COUNT(*) as cnt FROM admin_users")
    row = cur.fetchone()
    if row["cnt"] == 0:
        admin_hash = hash_password("cinetiza2026")
        editor_hash = hash_password("editor2026")
        conn.execute("""
        INSERT INTO admin_users (username, password_hash, role, full_name, email)
        VALUES 
        ('admin', %s, 'ADMIN', 'Comisión Organizadora Cine Tiza', 'festivalcinetiza@gmail.com'),
        ('editor', %s, 'EDITOR', 'Equipo Editorial ISO', 'prensa@cinetiza.com.ar')
        """, (admin_hash, editor_hash))

    # 2. Site Settings
    cur = conn.execute("SELECT COUNT(*) as cnt FROM site_settings")
    row = cur.fetchone()
    if row["cnt"] == 0:
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
            conn.execute("REPLACE INTO site_settings (`key`, `value`) VALUES (%s, %s)", (k, v))

    # 3. Editions
    cur = conn.execute("SELECT COUNT(*) as cnt FROM editions")
    row = cur.fetchone()
    if row["cnt"] == 0:
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
            conn.execute("""
            INSERT INTO editions (number, year, title, theme, description, start_date, end_date, poster_url, hero_image_url, films_count, schools_count, attendees_count, featured)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, e)

    # 4. Films
    cur = conn.execute("SELECT COUNT(*) as cnt FROM films")
    row = cur.fetchone()
    if row["cnt"] == 0:
        cur18 = conn.execute("SELECT id FROM editions WHERE number = 18")
        row18 = cur18.fetchone()
        ed18_id = row18["id"] if row18 else 1

        films_data = [
            (ed18_id, "Turno Noche", "turno-noche", 
             "Un grupo de estudiantes descubre un misterio en los pasillos de su escuela secundaria durante una jornada extracurricular. Una atmósfera de suspenso construida con maestría lumínica y sonora.",
             2025, "FICCION", "Suspenso / Drama", "11:42", "Instituto Secundario Oncativo (ISO)", "Oncativo", "Córdoba", "Argentina",
             "Facundo Rossi & Equipo 6° Año", json.dumps(["Camila Díaz (Sonido)", "Mateo Luna (Fotografía)", "Lucía Gómez (Montaje)"]),
             "Prof. Laura Martínez", "images/Carresel11.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Cortometraje Ficción 2025", "Mejor Fotografía", "Mejor Sonido"]), 1, "PUBLISHED"),

            (ed18_id, "SmartBoy", "smartboy",
             "Sátira distópica sobre la hiperconexión digital en la juventud y los límites entre la identidad real y el algoritmo escolar.",
             2025, "FICCION", "Comedia / Ciencia Ficción", "09:15", "Instituto Secundario Oncativo (ISO)", "Oncativo", "Córdoba", "Argentina",
             "Valentina Pérez", json.dumps(["Joaquín Alvarez (Actuación)", "Sofía Benítez (Arte)"]),
             "Prof. Martín Almada", "images/Carresel12.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mención Especial Guión Original", "Premio del Público"]), 1, "PUBLISHED"),

            (ed18_id, "Las Puertas del Tiempo", "las-puertas-del-tiempo",
             "Un viaje documental que rescata la memoria ferroviaria y los relatos orales de los pioneros de la región pampeana cordobesa.",
             2024, "DOCUMENTAL", "Histórico / Social", "14:20", "IPEM 338 Dr. Salvador Mazza", "Córdoba", "Córdoba", "Argentina",
             "Tomás Navarro & Taller Audiovisual", json.dumps(["Estudiantes 5° Año IPEM 338"]),
             "Prof. Gabriel Fernández", "images/Carresel13.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Documental 16ª Edición", "Seleccionado para Cinedfest España"]), 1, "PUBLISHED"),

            (ed18_id, "Ecos de Tiza", "ecos-de-tiza",
             "Cortometraje de animación stop-motion con plastilina y papel que explora las emociones adolescentes y la presión del futuro.",
             2025, "ANIMACION", "Stop Motion / Experimental", "06:50", "Escuela ProA Oncativo", "Oncativo", "Córdoba", "Argentina",
             "Julieta Molina", json.dumps(["Nicolás Vega (Animación)", "Ana Clara Ríos (Música Original)"]),
             "Prof. Roberto Sánchez", "images/Carresel14.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Animación 17ª Edición"]), 1, "PUBLISHED"),

            (ed18_id, "Frecuencia Joven", "frecuencia-joven",
             "Videoclip rítmico y conceptual que acompaña la composición musical original de una banda estudiantil sobre la libertad de expresión.",
             2024, "VIDEOCLIP", "Musical / Urbano", "04:30", "Instituto Manuel Belgrano", "Oliva", "Córdoba", "Argentina",
             "Ignacio Ceballos", json.dumps(["Banda 'Sin Timbre'", "Equipo Técnico Belgrano"]),
             "Prof. Cecilia Morales", "images/Carresel15.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Videoclip"]), 0, "PUBLISHED"),

            (ed18_id, "Raíces del Valle", "raices-del-valle",
             "Muestra Federal que retrata las tradiciones comunitarias y la preservación del monte nativo contada por jóvenes serranos.",
             2025, "MUESTRA_FEDERAL", "Documental Territorial", "12:10", "IPEM 142 Joaquín V. González", "San Marcos Sierras", "Córdoba", "Argentina",
             "Lara Soria", json.dumps(["Comunidad Educativa IPEM 142"]),
             "Prof. Marcelo Castro", "images/Carresel17.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Destacado Muestra Federal"]), 0, "PUBLISHED"),

            (ed18_id, "Cartas sin Destino", "cartas-sin-destino",
             "Desde España, un relato conmovedor sobre la distancia, la inmigración juvenil y los lazos que persisten a través del tiempo.",
             2025, "INTERNACIONAL", "Drama", "10:05", "IES Gabriel Ferrater", "Reus", "Cataluña", "España",
             "Pau Martí", json.dumps(["Elena Soler", "Arnau Rovira"]),
             "Prof. Xavier Puig", "images/Carresel18.jpeg", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
             json.dumps(["Mejor Cortometraje Internacional"]), 1, "PUBLISHED")
        ]

        for f in films_data:
            conn.execute("""
            INSERT INTO films (edition_id, title, slug, synopsis, year, category, genre, duration, institution, city, province, country, director, cast_and_crew, teacher_guide, thumbnail_url, video_url, awards, featured, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, f)

    # 5. Events
    cur = conn.execute("SELECT COUNT(*) as cnt FROM events")
    row = cur.fetchone()
    if row["cnt"] == 0:
        cur18 = conn.execute("SELECT id FROM editions WHERE number = 18")
        row18 = cur18.fetchone()
        ed18_id = row18["id"] if row18 else 1

        events_data = [
            (ed18_id, "2026-10-15", "09:00", "10:30", "Apertura Oficial 18ª Edición & Alfombra Roja",
             "Recepción de delegaciones estudiantiles de todo el país, acto de apertura institucional y corte de cinta en el Centro Cultural San Martín.",
             "Centro Cultural Gral. San Martín", "OTRO", "Comisión Directiva ISO & Autoridades", 1),
            (ed18_id, "2026-10-15", "11:00", "13:00", "Bloque 1: Muestra Oficial de Ficción",
             "Primera sesión de proyecciones competitivas de cortometrajes de ficción realizados por escuelas secundarias.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado Oficial de Ficción", 1),
            (ed18_id, "2026-10-15", "15:00", "17:30", "Taller: De la Idea al Guión Cinematográfico",
             "Espacio formativo y práctico dictado por docentes del Polo Audiovisual Córdoba sobre estructura dramática para jóvenes realizadores.",
             "Auditorio Instituto Secundario Oncativo", "TALLER", "Polo Audiovisual Córdoba", 0),
            (ed18_id, "2026-10-15", "18:00", "20:30", "Bloque 2: Muestra Federal & Debate Abierto",
             "Proyección de producciones regionales que retratan identidades locales de diferentes provincias con ronda de preguntas entre directores.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Equipo Cine Tiza", 0),
            (ed18_id, "2026-10-16", "09:30", "12:00", "Bloque 3: Documentales & Animación",
             "Exhibición de cortometrajes documentales y animación stop-motion/digital.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado de Documental y Animación", 1),
            (ed18_id, "2026-10-16", "14:30", "16:30", "Taller: Sonido Directo y Banda Sonora",
             "Clínica intensiva sobre grabación de sonido en rodajes escolares, microfonía y diseño sonoro.",
             "Laboratorio Multimedia ProA", "TALLER", "Especialistas Invitados", 0),
            (ed18_id, "2026-10-16", "17:00", "18:30", "Charla Magistral: El Futuro del Cine Joven",
             "Encuentro y debate entre directores consagrados y realizadores estudiantiles sobre el salto al cine profesional.",
             "Centro Cultural San Martín", "CHARLA", "Realizadores Cordobeses Destacados", 0),
            (ed18_id, "2026-10-16", "19:30", "22:00", "Noche de Videoclips & Arte Urbano",
             "Proyecciones de videoclips musicales en pantalla gigante con intervenciones musicales en vivo de bandas escolares.",
             "Patio de las Artes ISO", "MUSICA", "Bandas y Realizadores Invitados", 1),
            (ed18_id, "2026-10-17", "10:00", "12:30", "Bloque 4: Certamen Internacional Cine Tiza",
             "Proyección de cortometrajes seleccionados de instituciones educativas de Iberoamérica.",
             "Sala Cine Teatro Victoria", "PROYECCION", "Jurado Internacional", 1),
            (ed18_id, "2026-10-17", "15:00", "17:00", "Foro de Intercambio y Red de Festivales",
             "Mesa de trabajo entre docentes y estudiantes para consolidar la red nacional de festivales escolares.",
             "Auditorio ISO", "ARTE", "Comunidad Docente y ABC Cine", 0),
            (ed18_id, "2026-10-17", "19:00", "22:00", "Gala de Clausura & Entrega de Premios 2026",
             "Ceremonia oficial de premiación, entrega de estatuillas Tiza de Oro, menciones especiales y anuncio de clasificados internacionales.",
             "Sala Cine Teatro Victoria", "PREMIACION", "Comisión Cine Tiza & Jurado Oficial", 1)
        ]

        for ev in events_data:
            conn.execute("""
            INSERT INTO events (edition_id, day_date, start_time, end_time, title, description, location, type, speaker_or_host, featured)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, ev)

    # 6. Awards
    cur = conn.execute("SELECT COUNT(*) as cnt FROM awards")
    row = cur.fetchone()
    if row["cnt"] == 0:
        cur18 = conn.execute("SELECT id FROM editions WHERE number = 18")
        row18 = cur18.fetchone()
        ed18_id = row18["id"] if row18 else 1

        awards_data = [
            (ed18_id, 2025, "Mejor Cortometraje Ficción", "Turno Noche", "Instituto Secundario Oncativo", "Facundo Rossi", "images/Logo_CineTiza.png", "Ganador por unanimidad de jurado técnico"),
            (ed18_id, 2025, "Mejor Cortometraje Documental", "Voces del Telar", "IPEM 142 Joaquín V. González", "Clara Méndez", "images/Logo_CineTiza.png", "Reconocimiento a la preservación cultural"),
            (ed18_id, 2025, "Mejor Animación", "Ecos de Tiza", "Escuela ProA Oncativo", "Julieta Molina", "images/Logo_CineTiza.png", "Destacada técnica en stop motion"),
            (ed18_id, 2025, "Mejor Cortometraje Internacional", "Cartas sin Destino", "IES Gabriel Ferrater (España)", "Pau Martí", "images/Logo_CineTiza.png", "Clasificado para certamen iberoamericano"),
            (ed18_id, 2024, "Mejor Cortometraje Ficción", "Las Puertas del Tiempo", "IPEM 338 Dr. Salvador Mazza", "Tomás Navarro", "images/Logo_CineTiza.png", "Representante oficial en Cinedfest Tenerife"),
            (ed18_id, 2024, "Premio del Público", "SmartBoy", "Instituto Secundario Oncativo", "Valentina Pérez", "images/Logo_CineTiza.png", "Voto popular en sala llena")
        ]
        for aw in awards_data:
            conn.execute("""
            INSERT INTO awards (edition_id, year, category_name, winner_film_title, institution, director, badge_url, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, aw)

    # 7. Gallery
    cur = conn.execute("SELECT COUNT(*) as cnt FROM gallery")
    row = cur.fetchone()
    if row["cnt"] == 0:
        cur18 = conn.execute("SELECT id FROM editions WHERE number = 18")
        row18 = cur18.fetchone()
        ed18_id = row18["id"] if row18 else 1

        gallery_data = [
            (ed18_id, "Apertura Oficial en Sala Victoria", "FESTIVAL", "IMAGE", "images/Carresel1.png", "Recepción y sala colmada en Oncativo"),
            (ed18_id, "Taller de Animación y Cámara", "TALLERES", "IMAGE", "images/Carresel2.png", "Estudiantes explorando técnicas de filmación"),
            (ed18_id, "Proyección en Pantalla Gigante", "PROYECCIONES", "IMAGE", "images/Carresel3.png", "El público disfrutando de las producciones en competencia"),
            (ed18_id, "Entrega de Premios y Distinciones", "PREMIACION", "IMAGE", "images/Carresel4.png", "Momento emotivo de la entrega de trofeos Tiza"),
            (ed18_id, "Backstage de Rodaje Estudiantil", "BACKSTAGE", "IMAGE", "images/Carresel5.png", "Detrás de escena de los cortometrajes participantes"),
            (ed18_id, "Delegaciones de Todo el País", "PARTICIPANTES", "IMAGE", "images/Carresel6.png", "Jóvenes de diferentes provincias en Oncativo"),
            (ed18_id, "Comunidad ISO y Organizadores", "FESTIVAL", "IMAGE", "images/Carresel8.png", "El equipo docente y estudiantil del Instituto Secundario Oncativo"),
            (ed18_id, "Muestra de Cortos de Ficción", "PROYECCIONES", "IMAGE", "images/Carresel9.png", "Debate posterior a la proyección de ficción"),
            (ed18_id, "Jornada de Formación Audiovisual", "TALLERES", "IMAGE", "images/Carresel10.png", "Prácticas de sonido e iluminación"),
            (ed18_id, "Alfombra Roja y Registro de Medios", "BACKSTAGE", "IMAGE", "images/Carresel19.jpeg", "Entrevistas en vivo antes de la función de gala"),
            (ed18_id, "Celebración y Encuentro Joven", "PARTICIPANTES", "IMAGE", "images/Carresel20.jpeg", "Intercambio cultural entre realizadores adolescentes"),
            (ed18_id, "Cierre de la 17ª Edición", "PREMIACION", "IMAGE", "images/Carresel21.jpeg", "Foto grupal con todas las delegaciones participantes")
        ]
        for g in gallery_data:
            conn.execute("""
            INSERT INTO gallery (edition_id, title, category, media_type, media_url, caption)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, g)

    # 8. Submissions
    cur = conn.execute("SELECT COUNT(*) as cnt FROM submissions")
    row = cur.fetchone()
    if row["cnt"] == 0:
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
            conn.execute("""
            INSERT INTO submissions (film_title, institution, city, province, country, category, genre, duration, director, participants, teacher, email, phone, synopsis, video_url, thumbnail_url, status, admin_notes, terms_accepted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, s)

    conn.commit()

if __name__ == "__main__":
    init_mysql_db()
