import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.db_mysql import get_db

def export_dump():
    conn = get_db()
    tables = ['site_settings', 'editions', 'films', 'events', 'awards', 'gallery', 'submissions', 'contact_messages', 'admin_users']
    out_path = os.path.join(os.path.dirname(__file__), "cinetiza_dump.sql")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('-- ========================================================\n')
        f.write('-- Cine Tiza 18ª Edición (2026) - MySQL / MariaDB Dump\n')
        f.write('-- Festival Internacional de Cine y Artes Estudiantiles\n')
        f.write('-- Instituto Secundario Oncativo (ISO), Córdoba, Argentina\n')
        f.write('-- ========================================================\n\n')
        f.write('SET FOREIGN_KEY_CHECKS = 0;\n')
        f.write('CREATE DATABASE IF NOT EXISTS `cinetiza_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n')
        f.write('USE `cinetiza_db`;\n\n')
        
        for t in tables:
            cur = conn.conn.cursor()
            cur.execute(f'SHOW CREATE TABLE `{t}`')
            create_stmt = cur.fetchone()['Create Table']
            f.write(f'DROP TABLE IF EXISTS `{t}`;\n')
            f.write(f'{create_stmt};\n\n')
            
            cur.execute(f'SELECT * FROM `{t}`')
            rows = cur.fetchall()
            if rows:
                cols = list(rows[0].keys())
                cols_str = ', '.join([f'`{c}`' for c in cols])
                f.write(f'INSERT INTO `{t}` ({cols_str}) VALUES\n')
                val_lines = []
                for r in rows:
                    vals = []
                    for c in cols:
                        v = r[c]
                        if v is None:
                            vals.append('NULL')
                        elif isinstance(v, (int, float)):
                            vals.append(str(v))
                        else:
                            s = str(v).replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
                            vals.append(f"'{s}'")
                    val_lines.append('(' + ', '.join(vals) + ')')
                f.write(',\n'.join(val_lines) + ';\n\n')
            cur.close()

        f.write('SET FOREIGN_KEY_CHECKS = 1;\n')

    conn.close()
    print(f"Dump generated successfully at {out_path}")

if __name__ == "__main__":
    export_dump()
