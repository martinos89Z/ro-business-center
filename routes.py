import os
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote
from flask import Blueprint, abort, flash, redirect, render_template, request, send_from_directory, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from models import Category, ContactMessage, Inscription, Product, ProductImage, Settings, User, get_db_connection, backup_database, _execute
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MAX_LOGIN_ATTEMPTS, LOGIN_ATTEMPT_WINDOW, WHATSAPP_PHONE
from seo import SEOMetadata, StructuredData

# Rate limiter for admin login
limiter = Limiter(key_func=get_remote_address)

def get_available_products(extra_filter=None, params=()):
    conn = get_db_connection()
    query = '''
        SELECT p.*, c.name AS category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE (p.availability IS NULL OR p.availability = '' OR p.availability = 'Disponible')
    '''
    query_params = list(params)
    if extra_filter:
        query += f' AND {extra_filter}'
    query += ' ORDER BY p.created_at DESC'
    rows = _execute(conn, query, query_params).fetchall()
    conn.close()
    return [
        {**dict(row), 'images': [img['filename'] for img in ProductImage.for_product(row['id'])]}
        for row in rows
    ]


def get_filter_for_route(key):
    filters = Settings.get_product_filters()
    keywords = filters.get(key, [key])
    conditions = ' OR '.join([f"LOWER(p.name) LIKE ?" for _ in keywords])
    params = [f'%{kw}%' for kw in keywords]
    return f'({conditions})', tuple(params)


main = Blueprint('main', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_file_if_exists(filename):
    if not filename:
        return
    path = UPLOAD_FOLDER / filename
    if path.exists():
        path.unlink()


@main.route('/')
def index():
    categories = Category.all()
    products = []
    conn = get_db_connection()
    rows = _execute(conn, '''
        SELECT p.*, c.name AS category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.availability IS NULL OR p.availability = '' OR p.availability = 'Disponible'
        ORDER BY p.created_at DESC
        LIMIT 6
    ''').fetchall()
    conn.close()
    
    products = [
        {**dict(row), 'images': [img['filename'] for img in ProductImage.for_product(row['id'])]}
        for row in rows
    ]
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('home')
    
    # Structured data
    local_business = StructuredData.get_local_business()
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/")
    ])
    
    return render_template('index.html', 
                          products=products, 
                          categories=categories,
                          seo_metadata=seo_metadata,
                          local_business=local_business,
                          breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata,
                          StructuredData=StructuredData)


@main.route('/boutique')
def boutique():
    categories = Category.all()
    selected = request.args.get('category')
    conn = get_db_connection()
    if selected:
        rows = _execute(conn, '''
            SELECT p.*, c.name AS category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE (p.availability IS NULL OR p.availability = '' OR p.availability = 'Disponible')
            AND p.category_id = ?
            ORDER BY p.created_at DESC
        ''', (selected,)).fetchall()
    else:
        rows = _execute(conn, '''
            SELECT p.*, c.name AS category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.availability IS NULL OR p.availability = '' OR p.availability = 'Disponible'
            ORDER BY p.created_at DESC
        ''').fetchall()
    conn.close()
    products = []
    for row in rows:
        images = ProductImage.for_product(row['id'])
        products.append({**dict(row), 'images': [img['filename'] for img in images]})
    return render_template('boutique.html', products=products, categories=categories, selected_category=selected)


@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    images = ProductImage.for_product(product_id)
    return render_template('product_detail.html', product=product, images=images)


@main.route('/pc')
def pc_products():
    categories = Category.all()
    conn = get_db_connection()
    pc_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('PC',)).fetchone()
    conn.close()
    if pc_category:
        products = get_available_products('p.category_id = ?', (pc_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('pc'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('pc')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("PC", "/pc")
    ])
    
    return render_template('pc.html', products=products, categories=categories, 
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/ram')
def ram_products():
    categories = Category.all()
    conn = get_db_connection()
    ram_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('RAM',)).fetchone()
    conn.close()
    if ram_category:
        products = get_available_products('p.category_id = ?', (ram_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('ram'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('ram')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("RAM", "/ram")
    ])
    
    return render_template('ram.html', products=products, categories=categories,
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/chargeurs')
def chargeurs_products():
    categories = Category.all()
    conn = get_db_connection()
    chargeur_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('Chargeurs',)).fetchone()
    conn.close()
    if chargeur_category:
        products = get_available_products('p.category_id = ?', (chargeur_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('chargeur'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('chargeurs')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("Chargeurs", "/chargeurs")
    ])
    
    return render_template('chargeurs.html', products=products, categories=categories,
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/claviers')
def claviers_products():
    categories = Category.all()
    conn = get_db_connection()
    clavier_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('Claviers',)).fetchone()
    conn.close()
    if clavier_category:
        products = get_available_products('p.category_id = ?', (clavier_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('clavier'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('claviers')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("Claviers", "/claviers")
    ])
    
    return render_template('claviers.html', products=products, categories=categories,
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/souris')
def souris_products():
    categories = Category.all()
    conn = get_db_connection()
    souris_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('Souris',)).fetchone()
    conn.close()
    if souris_category:
        products = get_available_products('p.category_id = ?', (souris_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('souris'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('souris')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("Souris", "/souris")
    ])
    
    return render_template('souris.html', products=products, categories=categories,
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/accessoires')
def accessoires_products():
    categories = Category.all()
    conn = get_db_connection()
    accessoire_category = _execute(conn, 'SELECT id FROM categories WHERE name = ?', ('Accessoires',)).fetchone()
    conn.close()
    if accessoire_category:
        products = get_available_products('p.category_id = ?', (accessoire_category['id'],))
    else:
        products = get_available_products(*get_filter_for_route('accessoire'))
    
    # SEO metadata
    seo_metadata = SEOMetadata.get_page_metadata('accessoires')
    breadcrumb = StructuredData.get_breadcrumb_list([
        ("Accueil", "/"),
        ("Accessoires", "/accessoires")
    ])
    
    return render_template('accessoires.html', products=products, categories=categories,
                          seo_metadata=seo_metadata, breadcrumb=breadcrumb,
                          SEOMetadata=SEOMetadata, StructuredData=StructuredData)


@main.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Validate input
    if not data.get('nom') or not data.get('prenom') or not data.get('tel') or not data.get('formation'):
        return jsonify(status='error', message='Champs obligatoires manquants'), 400
    
    if len(data.get('nom', '')) > 100 or len(data.get('prenom', '')) > 100:
        return jsonify(status='error', message='Données invalides'), 400
    
    if len(data.get('tel', '')) > 20:
        return jsonify(status='error', message='Numéro de téléphone invalide'), 400
    
    if data.get('email') and len(data.get('email', '')) > 200:
        return jsonify(status='error', message='Email invalide'), 400
    
    Inscription.create(data)
    return jsonify(status='success', message='Inscription enregistrée')


@main.route('/contact', methods=['POST'])
def contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Validate input
    if not data.get('name') or not data.get('message'):
        return jsonify(status='error', message='Champs obligatoires manquants'), 400
    
    if len(data.get('name', '')) > 100 or len(data.get('message', '')) > 1000:
        return jsonify(status='error', message='Données invalides'), 400
    
    if data.get('email') and len(data.get('email', '')) > 200:
        return jsonify(status='error', message='Email invalide'), 400
    
    if data.get('phone') and len(data.get('phone', '')) > 20:
        return jsonify(status='error', message='Numéro de téléphone invalide'), 400
    
    ContactMessage.create(data)
    return jsonify(status='success', message='Message envoyé')


@main.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit(f"{MAX_LOGIN_ATTEMPTS} per {LOGIN_ATTEMPT_WINDOW} seconds")
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not username or not password:
            flash('Veuillez remplir tous les champs', 'danger')
            return render_template('admin/login.html')
        
        if len(username) > 50 or len(password) > 100:
            flash('Identifiants invalides', 'danger')
            return render_template('admin/login.html')
        
        user = User.get_by_username(username)
        if user and User.verify_password(user, password):
            login_user(user)
            return redirect(url_for('main.admin_dashboard'))
        flash('Identifiants invalides', 'danger')
    return render_template('admin/login.html')


@main.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Déconnecté', 'info')
    return redirect(url_for('main.admin_login'))


@main.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        Settings.set('site_name', request.form.get('site_name', '').strip())
        Settings.set('admin_email', request.form.get('admin_email', '').strip())
        Settings.set('product_filters', request.form.get('product_filters', '').strip())
        Settings.set('items_per_page', request.form.get('items_per_page', '12').strip())
        Settings.set('allow_registration', 'true' if request.form.get('allow_registration') else 'false')
        
        # Change password if provided
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password:
            if not current_password:
                flash('Mot de passe actuel requis pour le changement', 'danger')
            elif not User.verify_password(current_user, current_password):
                flash('Mot de passe actuel incorrect', 'danger')
            elif new_password != confirm_password:
                flash('Les nouveaux mots de passe ne correspondent pas', 'danger')
            elif len(new_password) < 6:
                flash('Le mot de passe doit contenir au moins 6 caractères', 'danger')
            else:
                conn = get_db_connection()
                from werkzeug.security import generate_password_hash
                _execute(conn, 'UPDATE users SET password_hash = ? WHERE id = ?', 
                            (generate_password_hash(new_password), current_user.id))
                conn.commit()
                conn.close()
                flash('Mot de passe changé avec succès', 'success')
        
        flash('Paramètres enregistrés', 'success')
        return redirect(url_for('main.admin_settings'))
    settings = Settings.all()
    return render_template('admin/settings.html', settings=settings)


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_products = Product.count()
    total_images = ProductImage.count()
    total_categories = len(Category.all())
    latest_products = Product.all()[:5]
    
    # Statistics by category
    products_by_category = {}
    categories = Category.all()
    for cat in categories:
        conn = get_db_connection()
        count = _execute(conn, 'SELECT COUNT(*) as c FROM products WHERE category_id = ?', (cat['id'],)).fetchone()
        conn.close()
        products_by_category[cat['name']] = count['c'] if count else 0
    
    # Recent activity stats
    conn = get_db_connection()
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    recent_contacts = _execute(conn, 'SELECT COUNT(*) as c FROM contacts WHERE created_at >= ?', (seven_days_ago,)).fetchone()
    recent_inscriptions = _execute(conn, 'SELECT COUNT(*) as c FROM inscriptions WHERE created_at >= ?', (seven_days_ago,)).fetchone()
    recent_products = _execute(conn, 'SELECT COUNT(*) as c FROM products WHERE created_at >= ?', (seven_days_ago,)).fetchone()
    conn.close()
    
    return render_template('admin/dashboard.html', 
                           total_products=total_products, 
                           total_images=total_images,
                           total_categories=total_categories, 
                           latest_products=latest_products,
                           products_by_category=products_by_category,
                           recent_contacts=recent_contacts['c'] if recent_contacts else 0,
                           recent_inscriptions=recent_inscriptions['c'] if recent_inscriptions else 0,
                           recent_products=recent_products['c'] if recent_products else 0)


@main.route('/admin/products')
@login_required
def admin_products():
    products = Product.all()
    categories = Category.all()
    return render_template('admin/products.html', products=products, categories=categories)


@main.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    categories = Category.all()
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'description': request.form.get('description', '').strip(),
            'brand': request.form.get('brand', '').strip(),
            'processor': request.form.get('processor', '').strip(),
            'ram': request.form.get('ram', '').strip(),
            'storage': request.form.get('storage', '').strip(),
            'state': request.form.get('state', '').strip(),
            'availability': request.form.get('availability', '').strip(),
            'category_id': request.form.get('category_id') or None,
            'price': float(request.form.get('price', 0) or 0),
        }
        
        # Validate input
        if not data['name']:
            flash('Le nom du produit est obligatoire', 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        if len(data['name']) > 200:
            flash('Le nom du produit est trop long (max 200 caractères)', 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        if len(data['description']) > 2000:
            flash('La description est trop longue (max 2000 caractères)', 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        if data['price'] < 0 or data['price'] > 1000000:
            flash('Le prix est invalide', 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        product_id = Product.create(data)
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = UPLOAD_FOLDER / filename
                counter = 1
                while path.exists():
                    stem = Path(filename).stem
                    suffix = Path(filename).suffix
                    filename = f'{stem}-{counter}{suffix}'
                    path = UPLOAD_FOLDER / filename
                    counter += 1
                file.save(path)
                ProductImage.add(product_id, filename)
        backup_database()  # Create backup after adding product
        flash('Produit ajouté avec succès', 'success')
        return redirect(url_for('main.admin_products'))
    return render_template('admin/add_product.html', categories=categories)


@main.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    categories = Category.all()
    images = ProductImage.for_product(product_id)
    if not product:
        abort(404)
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'description': request.form.get('description', '').strip(),
            'brand': request.form.get('brand', '').strip(),
            'processor': request.form.get('processor', '').strip(),
            'ram': request.form.get('ram', '').strip(),
            'storage': request.form.get('storage', '').strip(),
            'state': request.form.get('state', '').strip(),
            'availability': request.form.get('availability', '').strip(),
            'category_id': request.form.get('category_id') or None,
            'price': float(request.form.get('price', 0) or 0),
        }
        
        # Validate input
        if not data['name']:
            flash('Le nom du produit est obligatoire', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories, images=images)
        
        if len(data['name']) > 200:
            flash('Le nom du produit est trop long (max 200 caractères)', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories, images=images)
        
        if len(data['description']) > 2000:
            flash('La description est trop longue (max 2000 caractères)', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories, images=images)
        
        if data['price'] < 0 or data['price'] > 1000000:
            flash('Le prix est invalide', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories, images=images)
        
        Product.update(product_id, data)
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = UPLOAD_FOLDER / filename
                counter = 1
                while path.exists():
                    stem = Path(filename).stem
                    suffix = Path(filename).suffix
                    filename = f'{stem}-{counter}{suffix}'
                    path = UPLOAD_FOLDER / filename
                    counter += 1
                file.save(path)
                ProductImage.add(product_id, filename)
        backup_database()  # Create backup after editing product
        flash('Produit mis à jour', 'success')
        return redirect(url_for('main.admin_products'))
    return render_template('admin/edit_product.html', product=product, categories=categories, images=images)


@main.route('/admin/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    Product.delete(product_id)
    backup_database()  # Create backup after deleting product
    flash('Produit supprimé', 'success')
    return redirect(url_for('main.admin_products'))


@main.route('/admin/products/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_product_image(image_id):
    ProductImage.delete(image_id)
    flash('Image supprimée', 'success')
    return redirect(request.referrer or url_for('main.admin_products'))


@main.route('/admin/categories')
@login_required
def admin_categories():
    categories = Category.all()
    return render_template('admin/categories.html', categories=categories)


@main.route('/admin/categories/add', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name', '').strip()
    if name:
        Category.create(name)
    return redirect(url_for('main.admin_categories'))


@main.route('/admin/categories/<int:category_id>/edit', methods=['POST'])
@login_required
def edit_category(category_id):
    name = request.form.get('name', '').strip()
    if name:
        Category.update(category_id, name)
    return redirect(url_for('main.admin_categories'))


@main.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    Category.delete(category_id)
    return redirect(url_for('main.admin_categories'))


@main.route('/admin/galerie')
@login_required
def admin_galerie():
    products = Product.all()
    product_list = []
    for p in products:
        images = ProductImage.for_product(p['id'])
        product_list.append({**dict(p), 'images': [img['filename'] for img in images]})
    return render_template('admin/galerie.html', products=product_list)


@main.route('/admin/messages')
@login_required
def admin_messages():
    contacts = ContactMessage.all()
    inscriptions = Inscription.all()
    return render_template('admin/messages.html', contacts=contacts, inscriptions=inscriptions)


@main.route('/admin/messages/contact/<int:message_id>/process', methods=['POST'])
@login_required
def mark_contact_processed(message_id):
    ContactMessage.mark_processed(message_id)
    return redirect(url_for('main.admin_messages'))


@main.route('/admin/messages/contact/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_contact(message_id):
    ContactMessage.delete(message_id)
    return redirect(url_for('main.admin_messages'))


@main.route('/admin/messages/inscription/<int:inscription_id>/process', methods=['POST'])
@login_required
def mark_inscription_processed(inscription_id):
    Inscription.mark_processed(inscription_id)
    return redirect(url_for('main.admin_messages'))


@main.route('/admin/messages/inscription/<int:inscription_id>/delete', methods=['POST'])
@login_required
def delete_inscription(inscription_id):
    Inscription.delete(inscription_id)
    return redirect(url_for('main.admin_messages'))


@main.route('/api/whatsapp-order', methods=['POST'])
def api_whatsapp_order():
    data = request.get_json(silent=True) or {}
    product_name = data.get('product_name', 'Produit')
    quantity = data.get('quantity', 1)
    payment = data.get('payment', 'Comptant')
    client_name = data.get('client_name', '')
    phone = data.get('phone', '')
    notes = data.get('notes', '')
    image_url = data.get('image_url', '')

    message = 'Bonjour Ro Business Center, je souhaite commander :\n\n'
    message += f'Produit : {product_name}\n'
    message += f'Quantité : x{quantity}\n'
    message += f'Option de paiement : {payment}\n'
    if client_name:
        message += f'Nom : {client_name}\n'
    if phone:
        message += f'Téléphone : {phone}\n'
    if notes:
        message += f'Notes : {notes}\n'
    message += '\nMerci de me confirmer la disponibilité.'

    wa_url = f'https://wa.me/{WHATSAPP_PHONE}?text={quote(message)}'
    return jsonify(whatsapp_url=wa_url)
