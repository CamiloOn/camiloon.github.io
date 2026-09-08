#!/usr/bin/env python3
"""
Cine Tiza Platform - Fullstack Server & REST API
Festival Internacional de Cine y Artes Estudiantiles
Oncativo, Córdoba, Argentina
"""

import http.server
import socketserver
import json
import os
import mimetypes
import urllib.parse
import hashlib
import hmac
import time
import secrets
import base64
import re

from data.db_mysql import get_db, init_mysql_db

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
SECRET_KEY = os.environ.get("CINETIZA_SECRET", "cinetiza_secret_token_key_2026_festival_iso")

os.makedirs(UPLOADS_DIR, exist_ok=True)

def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, expected_hash = stored_hash.split("$")
        computed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return hmac.compare_digest(computed, expected_hash)
    except Exception:
        return False

def generate_token(user_id: int, username: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": int(time.time()) + (24 * 3600)  # 24 hours
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    sig = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"

def verify_token(token: str):
    if not token:
        return None
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_b64, sig = parts
        padding = 4 - (len(payload_b64) % 4)
        if padding != 4:
            payload_b64_padded = payload_b64 + ("=" * padding)
        else:
            payload_b64_padded = payload_b64
        
        expected_sig = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        
        payload_json = base64.urlsafe_b64decode(payload_b64_padded).decode()
        payload = json.loads(payload_json)
        
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None

def resolve_edition_id(conn, input_id):
    try:
        val = int(input_id)
    except (ValueError, TypeError):
        val = 18
    row = conn.execute("SELECT id FROM editions WHERE id = ? OR number = ? LIMIT 1", (val, val)).fetchone()
    if row:
        return row["id"]
    first = conn.execute("SELECT id FROM editions ORDER BY number DESC LIMIT 1").fetchone()
    return first["id"] if first else 1

# Simple in-memory rate limiter for logins and submissions
RATE_LIMITS = {}

def is_rate_limited(ip: str, endpoint: str, max_requests: int = 20, window_secs: int = 60) -> bool:
    now = time.time()
    key = f"{ip}:{endpoint}"
    requests = RATE_LIMITS.get(key, [])
    # Filter within window
    requests = [t for t in requests if now - t < window_secs]
    if len(requests) >= max_requests:
        RATE_LIMITS[key] = requests
        return True
    requests.append(now)
    RATE_LIMITS[key] = requests
    return False

# ----------------- HTTP Request Handler -----------------

class CineTizaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def send_json(self, status_code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def get_auth_user(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            return verify_token(token)
        # Check cookie
        cookie_header = self.headers.get("Cookie", "")
        match = re.search(r'cinetiza_token=([^;]+)', cookie_header)
        if match:
            return verify_token(match.group(1))
        return None

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode("utf-8"))
        except Exception:
            return {}

    # ----------------- GET Handlers -----------------

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API Routes
        if path.startswith("/api/"):
            return self.handle_api_get(path, query)

        # Route rewrites / fallback for clean URLs
        clean_routes = {
            "/": "/index.html",
            "/cortos": "/cortos.html",
            "/agenda": "/agenda.html",
            "/ediciones": "/ediciones.html",
            "/bases": "/bases.html",
            "/inscripciones": "/inscripciones.html",
            "/premios": "/premios.html",
            "/galeria": "/galeria.html",
            "/contacto": "/contacto.html",
            "/juego": "/juego.html",
            "/admin": "/admin/index.html",
            "/admin/login": "/admin/login.html"
        }

        if path in clean_routes:
            self.path = clean_routes[path]
        elif path.startswith("/ediciones/"):
            self.path = "/ediciones.html"

        return super().do_GET()

    def handle_api_get(self, path: str, query: dict):
        client_ip = self.client_address[0]

        # 1. GET /api/settings
        if path == "/api/settings":
            conn = get_db()
            rows = conn.execute("SELECT key, value FROM site_settings").fetchall()
            conn.close()
            settings = {r["key"]: r["value"] for r in rows}
            return self.send_json(200, {"success": True, "data": settings})

        # 2. GET /api/editions
        if path == "/api/editions":
            conn = get_db()
            rows = conn.execute("SELECT * FROM editions ORDER BY number DESC").fetchall()
            conn.close()
            editions = [dict(r) for r in rows]
            return self.send_json(200, {"success": True, "data": editions})

        # 3. GET /api/editions/:id
        edition_match = re.match(r"^/api/editions/(\d+)$", path)
        if edition_match:
            edition_id = int(edition_match.group(1))
            conn = get_db()
            edition = conn.execute("SELECT * FROM editions WHERE number = ? OR id = ?", (edition_id, edition_id)).fetchone()
            if not edition:
                conn.close()
                return self.send_json(404, {"success": False, "error": "Edición no encontrada"})
            
            # Fetch films and awards for this edition
            films = conn.execute("SELECT * FROM films WHERE edition_id = ?", (edition["id"],)).fetchall()
            awards = conn.execute("SELECT * FROM awards WHERE edition_id = ?", (edition["id"],)).fetchall()
            events = conn.execute("SELECT * FROM events WHERE edition_id = ? ORDER BY day_date, start_time", (edition["id"],)).fetchall()
            conn.close()

            result = dict(edition)
            result["films"] = [dict(f) for f in films]
            result["awards"] = [dict(a) for a in awards]
            result["events"] = [dict(ev) for ev in events]
            return self.send_json(200, {"success": True, "data": result})

        # 4. GET /api/films
        if path == "/api/films":
            conn = get_db()
            sql = "SELECT * FROM films WHERE status = 'PUBLISHED'"
            params = []
            
            if "category" in query and query["category"][0]:
                sql += " AND category = ?"
                params.append(query["category"][0].upper())
            if "year" in query and query["year"][0]:
                sql += " AND year = ?"
                params.append(int(query["year"][0]))
            if "featured" in query and query["featured"][0]:
                sql += " AND featured = 1"
            if "search" in query and query["search"][0]:
                term = f"%{query['search'][0]}%"
                sql += " AND (title LIKE ? OR institution LIKE ? OR director LIKE ? OR genre LIKE ?)"
                params.extend([term, term, term, term])

            sql += " ORDER BY featured DESC, year DESC, id DESC"
            rows = conn.execute(sql, params).fetchall()
            conn.close()

            films = []
            for r in rows:
                f = dict(r)
                if f.get("cast_and_crew"):
                    try:
                        f["cast_and_crew"] = json.loads(f["cast_and_crew"])
                    except Exception:
                        f["cast_and_crew"] = []
                if f.get("awards"):
                    try:
                        f["awards"] = json.loads(f["awards"])
                    except Exception:
                        f["awards"] = []
                films.append(f)
            return self.send_json(200, {"success": True, "data": films})

        # 5. GET /api/films/:id_or_slug
        film_match = re.match(r"^/api/films/([a-zA-Z0-9_-]+)$", path)
        if film_match:
            ident = film_match.group(1)
            conn = get_db()
            if ident.isdigit():
                film = conn.execute("SELECT * FROM films WHERE id = ?", (int(ident),)).fetchone()
            else:
                film = conn.execute("SELECT * FROM films WHERE slug = ?", (ident,)).fetchone()
            conn.close()

            if not film:
                return self.send_json(404, {"success": False, "error": "Cortometraje no encontrado"})
            f = dict(film)
            if f.get("cast_and_crew"):
                try:
                    f["cast_and_crew"] = json.loads(f["cast_and_crew"])
                except Exception:
                    pass
            if f.get("awards"):
                try:
                    f["awards"] = json.loads(f["awards"])
                except Exception:
                    pass
            return self.send_json(200, {"success": True, "data": f})

        # 6. GET /api/events (Agenda)
        if path == "/api/events":
            conn = get_db()
            sql = "SELECT * FROM events WHERE 1=1"
            params = []
            if "day" in query and query["day"][0]:
                sql += " AND day_date = ?"
                params.append(query["day"][0])
            if "type" in query and query["type"][0]:
                sql += " AND type = ?"
                params.append(query["type"][0].upper())
            sql += " ORDER BY day_date ASC, start_time ASC"
            rows = conn.execute(sql, params).fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 7. GET /api/awards
        if path == "/api/awards":
            conn = get_db()
            sql = "SELECT * FROM awards ORDER BY year DESC, id ASC"
            rows = conn.execute(sql).fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 8. GET /api/gallery
        if path == "/api/gallery":
            conn = get_db()
            sql = "SELECT * FROM gallery"
            params = []
            if "category" in query and query["category"][0]:
                sql += " WHERE category = ?"
                params.append(query["category"][0].upper())
            sql += " ORDER BY id DESC"
            rows = conn.execute(sql, params).fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 9. GET /api/auth/me
        if path == "/api/auth/me":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})
            return self.send_json(200, {"success": True, "data": user})

        # 10. GET /api/admin/dashboard
        if path == "/api/admin/dashboard":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})
            
            conn = get_db()
            submissions_count = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
            submissions_pending = conn.execute("SELECT COUNT(*) FROM submissions WHERE status = 'PENDIENTE'").fetchone()[0]
            films_count = conn.execute("SELECT COUNT(*) FROM films").fetchone()[0]
            events_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            messages_unread = conn.execute("SELECT COUNT(*) FROM contact_messages WHERE is_read = 0").fetchone()[0]
            editions_count = conn.execute("SELECT COUNT(*) FROM editions").fetchone()[0]
            
            recent_submissions = conn.execute("SELECT * FROM submissions ORDER BY id DESC LIMIT 5").fetchall()
            recent_messages = conn.execute("SELECT * FROM contact_messages ORDER BY id DESC LIMIT 5").fetchall()
            conn.close()

            return self.send_json(200, {
                "success": True,
                "data": {
                    "counts": {
                        "submissions": submissions_count,
                        "submissions_pending": submissions_pending,
                        "films": films_count,
                        "events": events_count,
                        "messages_unread": messages_unread,
                        "editions": editions_count
                    },
                    "recent_submissions": [dict(s) for s in recent_submissions],
                    "recent_messages": [dict(m) for m in recent_messages]
                }
            })

        # 11. GET /api/admin/submissions (Admin only)
        if path == "/api/admin/submissions":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})
            conn = get_db()
            sql = "SELECT * FROM submissions ORDER BY id DESC"
            rows = conn.execute(sql).fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 12. GET /api/admin/messages (Admin only)
        if path == "/api/admin/messages":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})
            conn = get_db()
            rows = conn.execute("SELECT * FROM contact_messages ORDER BY id DESC").fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 13. GET /api/admin/films (All films including drafts)
        if path == "/api/admin/films":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})
            conn = get_db()
            rows = conn.execute("SELECT * FROM films ORDER BY id DESC").fetchall()
            conn.close()
            return self.send_json(200, {"success": True, "data": [dict(r) for r in rows]})

        # 14. GET /api/game/leaderboard
        if path == "/api/game/leaderboard":
            conn = get_db()
            rows = conn.execute("""
                SELECT nickname, score, genre, film_title, created_at
                FROM game_scores
                ORDER BY score DESC, created_at ASC
                LIMIT 20
            """).fetchall()
            conn.close()
            leaderboard = []
            for i, r in enumerate(rows):
                entry = dict(r)
                entry["rank"] = i + 1
                leaderboard.append(entry)
            return self.send_json(200, {"success": True, "data": leaderboard})

        return self.send_json(404, {"success": False, "error": "Endpoint no encontrado"})

    # ----------------- POST Handlers -----------------

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        client_ip = self.client_address[0]
        body = self.read_json_body()

        # 1. POST /api/auth/login
        if path == "/api/auth/login":
            if is_rate_limited(client_ip, "login", max_requests=10, window_secs=60):
                return self.send_json(429, {"success": False, "error": "Demasiados intentos. Aguarde un minuto."})
            
            username = body.get("username", "").strip()
            password = body.get("password", "")
            if not username or not password:
                return self.send_json(400, {"success": False, "error": "Usuario y contraseña requeridos"})

            conn = get_db()
            user = conn.execute("SELECT * FROM admin_users WHERE username = ?", (username,)).fetchone()
            conn.close()

            if not user or not verify_password(password, user["password_hash"]):
                return self.send_json(401, {"success": False, "error": "Credenciales inválidas"})

            token = generate_token(user["id"], user["username"], user["role"])
            return self.send_json(200, {
                "success": True,
                "token": token,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                    "full_name": user["full_name"],
                    "email": user["email"]
                }
            })

        # 2. POST /api/submissions (Inscripción pública)
        if path == "/api/submissions":
            if is_rate_limited(client_ip, "submissions", max_requests=5, window_secs=60):
                return self.send_json(429, {"success": False, "error": "Límite de envíos alcanzado. Intente más tarde."})

            # Check honeypot for spam
            if body.get("website_hp"):
                return self.send_json(200, {"success": True, "message": "Inscripción recibida correctamente."})

            film_title = body.get("filmTitle", "").strip()
            institution = body.get("institution", "").strip()
            email = body.get("email", "").strip()
            video_url = body.get("videoUrl", "").strip()

            if not film_title or not institution or not email or not video_url:
                return self.send_json(400, {"success": False, "error": "Campos obligatorios incompletos (Título, Institución, Email, Enlace de video)"})

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO submissions (
                film_title, institution, city, province, country, category, genre,
                duration, director, participants, teacher, email, phone, synopsis,
                video_url, thumbnail_url, status, terms_accepted
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDIENTE', 1)
            """, (
                film_title,
                institution,
                body.get("city", "Oncativo"),
                body.get("province", "Córdoba"),
                body.get("country", "Argentina"),
                body.get("category", "FICCION"),
                body.get("genre", "General"),
                body.get("duration", "10:00"),
                body.get("director", "Estudiante Director/a"),
                body.get("participants", ""),
                body.get("teacher", ""),
                email,
                body.get("phone", ""),
                body.get("synopsis", ""),
                video_url,
                body.get("thumbnailUrl", "images/Logo_CineTiza.png")
            ))
            sub_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return self.send_json(201, {
                "success": True,
                "message": "¡Inscripción registrada con éxito! La comisión evaluadora revisará tu cortometraje.",
                "id": sub_id
            })

        # 3. POST /api/contact (Mensaje de contacto)
        if path == "/api/contact":
            if is_rate_limited(client_ip, "contact", max_requests=5, window_secs=60):
                return self.send_json(429, {"success": False, "error": "Límite de mensajes alcanzado. Aguarde unos instantes."})

            name = body.get("name", "").strip()
            email = body.get("email", "").strip()
            subject = body.get("subject", "").strip()
            message = body.get("message", "").strip()

            if not name or not email or not message:
                return self.send_json(400, {"success": False, "error": "Por favor complete todos los campos requeridos."})

            conn = get_db()
            conn.execute("""
            INSERT INTO contact_messages (name, email, subject, message, is_read)
            VALUES (?, ?, ?, ?, 0)
            """, (name, email, subject or "Consulta Festival Cine Tiza", message))
            conn.commit()
            conn.close()

            return self.send_json(201, {
                "success": True,
                "message": "Tu mensaje ha sido enviado a la organización de Cine Tiza. Te responderemos a la brevedad."
            })

        # 4. POST /api/upload (File/Image Upload)
        if path == "/api/upload":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado para subir archivos"})

            file_data = body.get("data", "")  # Base64 string
            filename = body.get("name", "upload.jpg")
            
            if not file_data:
                return self.send_json(400, {"success": False, "error": "Datos de archivo no provistos"})

            try:
                # Parse base64 header if present (e.g. data:image/png;base64,...)
                if "," in file_data:
                    header, encoded = file_data.split(",", 1)
                else:
                    encoded = file_data
                
                raw_bytes = base64.b64decode(encoded)
                if len(raw_bytes) > 10 * 1024 * 1024:  # 10MB max
                    return self.send_json(400, {"success": False, "error": "El archivo excede el tamaño máximo de 10MB"})

                ext = os.path.splitext(filename)[1].lower() or ".jpg"
                safe_name = f"{int(time.time())}_{secrets.token_hex(6)}{ext}"
                target_path = os.path.join(UPLOADS_DIR, safe_name)
                
                with open(target_path, "wb") as f:
                    f.write(raw_bytes)

                relative_url = f"uploads/{safe_name}"
                return self.send_json(201, {"success": True, "url": relative_url, "filename": safe_name})
            except Exception as e:
                return self.send_json(500, {"success": False, "error": f"Error procesando archivo: {str(e)}"})

        # 5. POST /api/admin/films (Crear corto)
        if path == "/api/admin/films":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})

            title = body.get("title", "").strip()
            if not title:
                return self.send_json(400, {"success": False, "error": "El título del cortometraje es requerido"})

            slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-') + f"-{secrets.token_hex(3)}"
            conn = get_db()
            cursor = conn.cursor()
            ed_id = resolve_edition_id(conn, body.get("editionId", 18))
            cursor.execute("""
            INSERT INTO films (
                edition_id, title, slug, synopsis, year, category, genre, duration,
                institution, city, province, country, director, cast_and_crew, teacher_guide,
                thumbnail_url, video_url, awards, featured, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ed_id,
                title,
                slug,
                body.get("synopsis", ""),
                int(body.get("year", 2026)),
                body.get("category", "FICCION"),
                body.get("genre", "General"),
                body.get("duration", "10:00"),
                body.get("institution", "Instituto Secundario Oncativo"),
                body.get("city", "Oncativo"),
                body.get("province", "Córdoba"),
                body.get("country", "Argentina"),
                body.get("director", ""),
                json.dumps(body.get("castAndCrew", [])),
                body.get("teacherGuide", ""),
                body.get("thumbnailUrl", "images/Logo_CineTiza.png"),
                body.get("videoUrl", ""),
                json.dumps(body.get("awards", [])),
                1 if body.get("featured") else 0,
                body.get("status", "PUBLISHED")
            ))
            film_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json(201, {"success": True, "id": film_id, "slug": slug})

        # 6. POST /api/admin/events (Crear evento de agenda)
        if path == "/api/admin/events":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})

            title = body.get("title", "").strip()
            if not title:
                return self.send_json(400, {"success": False, "error": "Título requerido"})

            conn = get_db()
            cursor = conn.cursor()
            ed_id = resolve_edition_id(conn, body.get("editionId", 18))
            cursor.execute("""
            INSERT INTO events (
                edition_id, day_date, start_time, end_time, title, description,
                location, type, speaker_or_host, featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ed_id,
                body.get("dayDate", "2026-10-15"),
                body.get("startTime", "10:00"),
                body.get("endTime", "11:30"),
                title,
                body.get("description", ""),
                body.get("location", "Sala Cine Teatro Victoria"),
                body.get("type", "PROYECCION"),
                body.get("speakerOrHost", ""),
                1 if body.get("featured") else 0
            ))
            ev_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json(201, {"success": True, "id": ev_id})

        # 7. POST /api/admin/awards (Crear premio)
        if path == "/api/admin/awards":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})

            category_name = body.get("categoryName", "").strip()
            winner_film = body.get("winnerFilmTitle", "").strip()

            conn = get_db()
            cursor = conn.cursor()
            ed_id = resolve_edition_id(conn, body.get("editionId", 18))
            cursor.execute("""
            INSERT INTO awards (
                edition_id, year, category_name, winner_film_title, institution,
                director, badge_url, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ed_id,
                int(body.get("year", 2026)),
                category_name,
                winner_film,
                body.get("institution", ""),
                body.get("director", ""),
                body.get("badgeUrl", "images/Logo_CineTiza.png"),
                body.get("notes", "")
            ))
            award_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json(201, {"success": True, "id": award_id})

        # 8. POST /api/admin/gallery (Crear foto/video galería)
        if path == "/api/admin/gallery":
            user = self.get_auth_user()
            if not user:
                return self.send_json(401, {"success": False, "error": "No autorizado"})

            title = body.get("title", "").strip()
            media_url = body.get("mediaUrl", "").strip()
            if not title or not media_url:
                return self.send_json(400, {"success": False, "error": "Título y URL de medio requeridos"})

            conn = get_db()
            cursor = conn.cursor()
            ed_id = resolve_edition_id(conn, body.get("editionId", 18))
            cursor.execute("""
            INSERT INTO gallery (edition_id, title, category, media_type, media_url, caption)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ed_id,
                title,
                body.get("category", "FESTIVAL"),
                body.get("mediaType", "IMAGE"),
                media_url,
                body.get("caption", "")
            ))
            g_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self.send_json(201, {"success": True, "id": g_id})

        # 9. POST /api/game/scores — Guardar resultado Director's Cut
        if path == "/api/game/scores":
            if is_rate_limited(client_ip, "game_scores", max_requests=3, window_secs=300):
                return self.send_json(429, {"success": False, "error": "Demasiados envíos. Aguardá unos minutos."})

            nickname   = body.get("nickname", "").strip()
            genre      = body.get("genre", "").strip().upper()
            film_title = body.get("filmTitle", "").strip()
            character  = body.get("character", "").strip().upper()
            location   = body.get("location", "").strip().upper()
            decisions  = body.get("decisions", [])

            VALID_GENRES    = {"DRAMA", "COMEDIA", "TERROR", "CIENCIA_FICCION", "MISTERIO", "EXPERIMENTAL"}
            VALID_CHARS     = {"ESTUDIANTE", "DIRECTOR", "MISTERIOSO", "VISITANTE", "AMIGO"}
            VALID_LOCATIONS = {"ESCUELA", "PLAZA", "CIUDAD", "CASA", "ABANDONADO", "ESTUDIO"}
            VALID_CHOICES   = {"A", "B", "C", "D"}

            # --- Validaciones ---
            if not nickname or len(nickname) < 2 or len(nickname) > 30:
                return self.send_json(400, {"success": False, "error": "Nickname inválido (2–30 caracteres)"})
            if re.search(r'[<>"\'/;]', nickname):
                return self.send_json(400, {"success": False, "error": "Nickname contiene caracteres no permitidos"})
            if genre not in VALID_GENRES:
                return self.send_json(400, {"success": False, "error": "Género inválido"})
            if character not in VALID_CHARS:
                return self.send_json(400, {"success": False, "error": "Personaje inválido"})
            if location not in VALID_LOCATIONS:
                return self.send_json(400, {"success": False, "error": "Locación inválida"})
            if not isinstance(decisions, list) or len(decisions) != 7:
                return self.send_json(400, {"success": False, "error": "Se requieren exactamente 7 decisiones"})
            if any(d not in VALID_CHOICES for d in decisions):
                return self.send_json(400, {"success": False, "error": "Decisiones inválidas (A/B/C/D)"})
            if not film_title or len(film_title) < 1 or len(film_title) > 100:
                return self.send_json(400, {"success": False, "error": "Título de película inválido"})

            # --- Recálculo server-side del score ---
            # Tabla de efectos por escena y decisión (debe coincidir con game-data.js)
            SCENE_EFFECTS = [
                # Escena 1: Actor olvidó el guion
                {"A": {"acting":8,"story":-5,"creativity":6},    "B": {"acting":12,"story":8},               "C": {"story":6,"creativity":4},             "D": {"acting":-8,"cinematography":4}},
                # Escena 2: Ruido durante grabación
                {"A": {"sound":12,"resources":-5},               "B": {"sound":-10,"cinematography":2},      "C": {"resources":-8,"creativity":4},        "D": {"sound":6,"creativity":10,"story":4}},
                # Escena 3: Poca batería
                {"A": {"cinematography":10,"resources":-12},     "B": {"resources":-5},                     "C": {"cinematography":5,"resources":-3},    "D": {"creativity":8,"story":6,"resources":-8}},
                # Escena 4: Empieza a llover
                {"A": {"resources":-5,"acting":3},               "B": {"cinematography":12,"story":8,"creativity":6},"C": {"story":5,"creativity":3},    "D": {"acting":8,"cinematography":6,"resources":-10}},
                # Escena 5: Actor propone cambio
                {"A": {"acting":10,"story":8,"creativity":4},    "B": {"direction":8,"story":3},             "C": {"creativity":10,"direction":4,"resources":-5},"D": {"acting":6,"creativity":8,"story":4}},
                # Escena 6: Camarógrafo se enferma
                {"A": {"direction":10,"cinematography":8},       "B": {"resources":-10,"cinematography":12}, "C": {"cinematography":-5,"creativity":8},   "D": {"story":8,"creativity":10,"cinematography":-5}},
                # Escena 7: Disputa en el set
                {"A": {"direction":12,"acting":-5},              "B": {"acting":8,"direction":4,"creativity":4},"C": {"resources":-8,"acting":5,"direction":5},"D": {"creativity":12,"story":8,"acting":6}},
            ]
            CHAR_BONUSES = {
                "ESTUDIANTE": {"acting":5,"story":3},
                "DIRECTOR":   {"direction":5,"creativity":3},
                "MISTERIOSO": {"story":5,"cinematography":3},
                "VISITANTE":  {"creativity":5,"acting":3},
                "AMIGO":      {"acting":5,"direction":3},
            }
            stats = {"direction":50,"acting":50,"cinematography":50,"sound":50,"story":50,"creativity":50,"resources":50}
            for k, v in CHAR_BONUSES.get(character, {}).items():
                stats[k] = min(100, stats.get(k, 50) + v)
            for i, choice in enumerate(decisions):
                effects = SCENE_EFFECTS[i].get(choice, {})
                for k, v in effects.items():
                    stats[k] = max(0, min(100, stats.get(k, 50) + v))
            raw_score = (
                stats["direction"]       * 0.20 +
                stats["acting"]          * 0.15 +
                stats["cinematography"]  * 0.20 +
                stats["sound"]           * 0.10 +
                stats["story"]           * 0.20 +
                stats["creativity"]      * 0.15
            )
            resource_mult = 0.85 + (stats["resources"] / 100.0) * 0.25
            computed_score = int(min(100, round(raw_score * resource_mult)))

            # Hash de IP para privacidad
            ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()[:16]
            decisions_str = "".join(decisions)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO game_scores (nickname, score, genre, film_title, `character`, location, decisions, ip_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nickname, computed_score, genre, film_title, character, location, decisions_str, ip_hash))
            new_id = cursor.lastrowid
            conn.commit()

            # Calcular ranking position
            rank_row = conn.execute(
                "SELECT COUNT(*) as cnt FROM game_scores WHERE score > ?", (computed_score,)
            ).fetchone()
            conn.close()
            rank_pos = (rank_row["cnt"] if rank_row else 0) + 1

            return self.send_json(201, {
                "success": True,
                "id": new_id,
                "score": computed_score,
                "rank": rank_pos,
                "message": "¡Tu película fue guardada en el ranking de Director's Cut!"
            })

        return self.send_json(404, {"success": False, "error": "Endpoint no encontrado"})

    # ----------------- PUT Handlers -----------------

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.read_json_body()
        user = self.get_auth_user()

        if not user:
            return self.send_json(401, {"success": False, "error": "No autorizado"})

        # 1. PUT /api/settings
        if path == "/api/settings" or path == "/api/admin/settings":
            conn = get_db()
            for k, v in body.items():
                conn.execute("INSERT OR REPLACE INTO site_settings (key, value) VALUES (?, ?)", (str(k), str(v)))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Configuración actualizada correctamente."})

        # 2. PUT /api/admin/submissions/:id (Change status / notes)
        sub_match = re.match(r"^/api/admin/submissions/(\d+)$", path)
        if sub_match:
            sub_id = int(sub_match.group(1))
            status = body.get("status", "PENDIENTE")
            admin_notes = body.get("adminNotes", "")

            conn = get_db()
            conn.execute("UPDATE submissions SET status = ?, admin_notes = ? WHERE id = ?", (status, admin_notes, sub_id))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": f"Inscripción #{sub_id} actualizada a estado {status}"})

        # 3. PUT /api/admin/films/:id
        film_match = re.match(r"^/api/admin/films/(\d+)$", path)
        if film_match:
            film_id = int(film_match.group(1))
            conn = get_db()
            conn.execute("""
            UPDATE films SET
                title = COALESCE(?, title),
                synopsis = COALESCE(?, synopsis),
                category = COALESCE(?, category),
                genre = COALESCE(?, genre),
                duration = COALESCE(?, duration),
                institution = COALESCE(?, institution),
                director = COALESCE(?, director),
                thumbnail_url = COALESCE(?, thumbnail_url),
                video_url = COALESCE(?, video_url),
                featured = COALESCE(?, featured),
                status = COALESCE(?, status)
            WHERE id = ?
            """, (
                body.get("title"),
                body.get("synopsis"),
                body.get("category"),
                body.get("genre"),
                body.get("duration"),
                body.get("institution"),
                body.get("director"),
                body.get("thumbnailUrl"),
                body.get("videoUrl"),
                1 if body.get("featured") else 0 if "featured" in body else None,
                body.get("status"),
                film_id
            ))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Cortometraje actualizado"})

        # 4. PUT /api/admin/messages/:id (Mark read)
        msg_match = re.match(r"^/api/admin/messages/(\d+)$", path)
        if msg_match:
            msg_id = int(msg_match.group(1))
            is_read = 1 if body.get("isRead", True) else 0
            conn = get_db()
            conn.execute("UPDATE contact_messages SET is_read = ? WHERE id = ?", (is_read, msg_id))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Mensaje actualizado"})

        return self.send_json(404, {"success": False, "error": "Endpoint no encontrado"})

    # ----------------- DELETE Handlers -----------------

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        user = self.get_auth_user()

        if not user:
            return self.send_json(401, {"success": False, "error": "No autorizado"})

        # Delete Film
        m = re.match(r"^/api/admin/films/(\d+)$", path)
        if m:
            film_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM films WHERE id = ?", (film_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Cortometraje eliminado"})

        # Delete Event
        m = re.match(r"^/api/admin/events/(\d+)$", path)
        if m:
            ev_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM events WHERE id = ?", (ev_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Evento eliminado"})

        # Delete Award
        m = re.match(r"^/api/admin/awards/(\d+)$", path)
        if m:
            award_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM awards WHERE id = ?", (award_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Premio eliminado"})

        # Delete Gallery item
        m = re.match(r"^/api/admin/gallery/(\d+)$", path)
        if m:
            g_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM gallery WHERE id = ?", (g_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Elemento de galería eliminado"})

        # Delete Submission
        m = re.match(r"^/api/admin/submissions/(\d+)$", path)
        if m:
            s_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM submissions WHERE id = ?", (s_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Inscripción eliminada"})

        # Delete Message
        m = re.match(r"^/api/admin/messages/(\d+)$", path)
        if m:
            msg_id = int(m.group(1))
            conn = get_db()
            conn.execute("DELETE FROM contact_messages WHERE id = ?", (msg_id,))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True, "message": "Mensaje eliminado"})

        return self.send_json(404, {"success": False, "error": "Endpoint no encontrado"})

def run_server(port=PORT):
    # Ensure MySQL DB exists and is initialized
    init_mysql_db()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CineTizaHandler) as httpd:
        print(f"[Cine Tiza] Server running at http://localhost:{port}")
        print(f"[Cine Tiza] Database: XAMPP MySQL (cinetiza_db on port 3306)")
        print(f"[Cine Tiza] Root: {BASE_DIR}")
        print("[Cine Tiza] Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
