import os
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import DATABASE_URL, USE_POSTGRES, UPLOAD_FOLDER

# PostgreSQL support
if USE_POSTGRES:
    import psycopg2
    from psycopg2 import sql

def _execute(conn, query, params=()):
    if USE_POSTGRES:
        query = query.replace('?', '%s')
    return conn.execute(query, params)


def _last_insert_id(conn, cursor):
    if USE_POSTGRES:
        cursor.execute('SELECT LASTVAL()')
        row = cursor.fetchone()
        return row[0] if row else None
    return cursor.lastrowid


def get_db_connection():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        return conn
    else:
        db_path = DATABASE_URL.replace('sqlite:///', '')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    conn = get_db_connection()
    
    # SQL syntax differs between SQLite and PostgreSQL
    if USE_POSTGRES:
        # PostgreSQL syntax
        init_script = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            brand TEXT,
            processor TEXT,
            ram TEXT,
            storage TEXT,
            state TEXT,
            availability TEXT,
            category_id INTEGER REFERENCES categories(id),
            price REAL DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS product_images (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            filename TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'En attente',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS inscriptions (
            id SERIAL PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT,
            formation TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'En attente',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        '''
        cursor = conn.cursor()
        cursor.execute(init_script)
        conn.commit()
        cursor.close()
    else:
        # SQLite syntax
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            brand TEXT,
            processor TEXT,
            ram TEXT,
            storage TEXT,
            state TEXT,
            availability TEXT,
            category_id INTEGER REFERENCES categories(id),
            price REAL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'En attente',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT,
            formation TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'En attente',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        ''')
    
    conn.close()

    ensure_admin_user()
    Settings.seed_defaults()
    ensure_default_categories()


def ensure_admin_user():
    conn = get_db_connection()
    user = _execute(conn, 'SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not user:
        _execute(conn, 'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                 ('admin', generate_password_hash('admin123')))
        conn.commit()
    conn.close()


def ensure_default_categories():
    default_categories = ['PC', 'RAM', 'Chargeurs', 'Claviers', 'Souris', 'Accessoires']
    conn = get_db_connection()
    for category_name in default_categories:
        existing = _execute(conn, 'SELECT id FROM categories WHERE name = ?', (category_name,)).fetchone()
        if not existing:
            _execute(conn, 'INSERT INTO categories (name) VALUES (?)', (category_name,))
    conn.commit()
    conn.close()


def backup_database():
    """Create a backup of the database with timestamp"""
    try:
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if USE_POSTGRES:
            import subprocess
            backup_file = backup_dir / f'backup_{timestamp}.sql'
            try:
                subprocess.run(['pg_dump', '-d', DATABASE_URL, '-f', str(backup_file)], check=True)
            except Exception:
                print("Warning: pg_dump not available. Skipping PostgreSQL backup.")
                return None
        else:
            db_path = DATABASE_URL.replace('sqlite:///', '')
            backup_file = backup_dir / f'backup_{timestamp}.db'
            shutil.copy2(db_path, backup_file)
        
        backups = sorted(backup_dir.glob('backup_*'))
        if len(backups) > 7:
            for old_backup in backups[:-7]:
                old_backup.unlink()
        
        return str(backup_file)
    except Exception as e:
        print(f"Backup failed: {e}")
        return None


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT id, username FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if row:
            return User(row['id'], row['username'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT id, username FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if row:
            return User(row['id'], row['username'])
        return None

    @staticmethod
    def verify_password(user_obj, password):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT password_hash FROM users WHERE id = ?', (user_obj.id,)).fetchone()
        conn.close()
        if row:
            return check_password_hash(row['password_hash'], password)
        return False


class Category:
    @staticmethod
    def all():
        conn = get_db_connection()
        rows = _execute(conn, 'SELECT * FROM categories ORDER BY name ASC').fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def create(name):
        conn = get_db_connection()
        if USE_POSTGRES:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (name) VALUES (%s) RETURNING id', (name,))
            category_id = cursor.fetchone()[0]
            cursor.close()
        else:
            cursor = _execute(conn, 'INSERT INTO categories (name) VALUES (?)', (name,))
            category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return category_id

    @staticmethod
    def update(category_id, name):
        conn = get_db_connection()
        _execute(conn, 'UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(category_id):
        conn = get_db_connection()
        _execute(conn, 'DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()


class Product:
    @staticmethod
    def all():
        conn = get_db_connection()
        rows = _execute(conn, '''
            SELECT p.*, c.name AS category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.created_at DESC
        ''').fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        row = _execute(conn, '''
            SELECT p.*, c.name AS category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
        ''', (product_id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def create(data):
        conn = get_db_connection()
        if USE_POSTGRES:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, description, brand, processor, ram, storage, state, availability, category_id, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            ''', (
                data['name'], data['description'], data['brand'], data['processor'], data['ram'], data['storage'],
                data['state'], data['availability'], data.get('category_id'), data.get('price', 0)
            ))
            product_id = cursor.fetchone()[0]
            cursor.close()
        else:
            cursor = _execute(conn, '''
                INSERT INTO products (name, description, brand, processor, ram, storage, state, availability, category_id, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'], data['description'], data['brand'], data['processor'], data['ram'], data['storage'],
                data['state'], data['availability'], data.get('category_id'), data.get('price', 0)
            ))
            product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id

    @staticmethod
    def update(product_id, data):
        conn = get_db_connection()
        _execute(conn, '''
            UPDATE products
            SET name = ?, description = ?, brand = ?, processor = ?, ram = ?, storage = ?, state = ?, availability = ?, category_id = ?, price = ?
            WHERE id = ?
        ''', (
            data['name'], data['description'], data['brand'], data['processor'], data['ram'], data['storage'],
            data['state'], data['availability'], data.get('category_id'), data.get('price', 0), product_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        # First, delete all associated image files
        images = ProductImage.for_product(product_id)
        for img in images:
            file_path = UPLOAD_FOLDER / img['filename']
            if file_path.exists():
                file_path.unlink(missing_ok=True)
        
        # Then delete from database
        conn = get_db_connection()
        _execute(conn, 'DELETE FROM product_images WHERE product_id = ?', (product_id,))
        _execute(conn, 'DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def count():
        conn = get_db_connection()
        row = _execute(conn, 'SELECT COUNT(*) AS c FROM products').fetchone()
        conn.close()
        return row['c'] if row else 0


class ProductImage:
    @staticmethod
    def add(product_id, filename):
        conn = get_db_connection()
        _execute(conn, 'INSERT INTO product_images (product_id, filename) VALUES (?, ?)', (product_id, filename))
        conn.commit()
        conn.close()

    @staticmethod
    def for_product(product_id):
        conn = get_db_connection()
        rows = _execute(conn, 'SELECT * FROM product_images WHERE product_id = ? ORDER BY id ASC', (product_id,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete(image_id):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT filename FROM product_images WHERE id = ?', (image_id,)).fetchone()
        if row:
            file_path = UPLOAD_FOLDER / row['filename']
            if file_path.exists():
                file_path.unlink(missing_ok=True)
            _execute(conn, 'DELETE FROM product_images WHERE id = ?', (image_id,))
            conn.commit()
        conn.close()

    @staticmethod
    def count():
        conn = get_db_connection()
        row = _execute(conn, 'SELECT COUNT(*) AS c FROM product_images').fetchone()
        conn.close()
        return row['c'] if row else 0


class ContactMessage:
    @staticmethod
    def create(data):
        conn = get_db_connection()
        contact = data.get('contact', '') or ''
        subject = data.get('subject', '') or ''
        email = contact if '@' in contact else None
        phone = contact if not email else None
        _execute(conn, 'INSERT INTO contacts (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)', (
            data.get('name'), email, phone, subject, data.get('message')
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_db_connection()
        rows = _execute(conn, 'SELECT * FROM contacts ORDER BY created_at DESC').fetchall()
        conn.close()
        return rows

    @staticmethod
    def mark_processed(message_id):
        conn = get_db_connection()
        _execute(conn, 'UPDATE contacts SET status = ? WHERE id = ?', ('processed', message_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(message_id):
        conn = get_db_connection()
        _execute(conn, 'DELETE FROM contacts WHERE id = ?', (message_id,))
        conn.commit()
        conn.close()


class Settings:
    DEFAULTS = {
        'site_name': 'Mon Site',
        'admin_email': '',
        'product_filters': 'pc,ordinateur,portable|ram,mémoire|chargeur,adaptateur|clavier|souris|accessoire',
        'items_per_page': '12',
        'allow_registration': 'true',
    }

    @staticmethod
    def get(key, default=None):
        conn = get_db_connection()
        row = _execute(conn, 'SELECT value FROM settings WHERE key = ?', (key,)).fetchone()
        conn.close()
        if row:
            return row['value']
        if default is not None:
            return default
        return Settings.DEFAULTS.get(key, '')

    @staticmethod
    def set(key, value):
        conn = get_db_connection()
        _execute(conn, 'INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value', (key, value))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_db_connection()
        rows = _execute(conn, 'SELECT * FROM settings').fetchall()
        conn.close()
        return {row['key']: row['value'] for row in rows}

    @staticmethod
    def get_product_filters():
        raw = Settings.get('product_filters', Settings.DEFAULTS['product_filters'])
        filters = {}
        for segment in raw.split('|'):
            if ':' in segment:
                key, words = segment.split(':', 1)
            else:
                parts = segment.split(',', 1)
                key = parts[0]
                words = parts[1] if len(parts) > 1 else key
            filters[key.strip()] = [w.strip() for w in words.split(',') if w.strip()]
        return filters

    @staticmethod
    def seed_defaults():
        conn = get_db_connection()
        for key, value in Settings.DEFAULTS.items():
            if USE_POSTGRES:
                _execute(conn, 'INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO NOTHING', (key, value))
            else:
                _execute(conn, 'INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()


class Inscription:
    @staticmethod
    def create(data):
        conn = get_db_connection()
        _execute(conn, 'INSERT INTO inscriptions (prenom, nom, tel, email, formation, message) VALUES (?, ?, ?, ?, ?, ?)', (
            data.get('prenom'), data.get('nom'), data.get('tel'), data.get('email'), data.get('formation'), data.get('message')
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_db_connection()
        rows = _execute(conn, 'SELECT * FROM inscriptions ORDER BY created_at DESC').fetchall()
        conn.close()
        return rows

    @staticmethod
    def mark_processed(inscription_id):
        conn = get_db_connection()
        _execute(conn, 'UPDATE inscriptions SET status = ? WHERE id = ?', ('processed', inscription_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(inscription_id):
        conn = get_db_connection()
        _execute(conn, 'DELETE FROM inscriptions WHERE id = ?', (inscription_id,))
        conn.commit()
        conn.close()
