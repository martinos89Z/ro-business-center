import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory, Response
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import User, init_db
from routes import main
from config import SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH, WHATSAPP_PHONE
from seo import SEOMetadata, StructuredData, SitemapGenerator, RobotsTxt, WebManifest

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

app.register_blueprint(main)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.context_processor
def inject_seo_helpers():
    return {
        'SEOMetadata': SEOMetadata,
        'StructuredData': StructuredData,
        'WHATSAPP_PHONE': WHATSAPP_PHONE
    }


@app.before_request
def ensure_db():
    pass


@app.route('/health')
def health():
    return {'status': 'ok'}


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# SEO Routes
@app.route('/robots.txt')
def robots_txt():
    return Response(RobotsTxt.generate(), mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    return Response(SitemapGenerator.generate_sitemap(), mimetype='application/xml')


@app.route('/manifest.webmanifest')
def manifest():
    import json
    return Response(json.dumps(WebManifest.generate()), mimetype='application/manifest+json')


# Security Headers
@app.after_request
def set_security_headers(response):
    from flask import request
    
    # Content Security Policy - Temporarily disabled for development
    # csp_policy = (
    #     "default-src 'self'; "
    #     "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google-analytics.com https://www.googletagmanager.com; "
    #     "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://www.gstatic.com; "
    #     "font-src 'self' https://fonts.gstatic.com; "
    #     "img-src 'self' data: https:; "
    #     "connect-src 'self' https://www.google-analytics.com https://wa.me https://translate.googleapis.com; "
    #     "frame-ancestors 'self'; "
    #     "form-action 'self';"
    # )
    
    # CSP plus stricte pour les pages admin
    if request.path.startswith('/admin'):
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self';"
        )
        response.headers['Content-Security-Policy'] = csp_policy
    
    # X-Frame-Options
    if request.path.startswith('/admin'):
        response.headers['X-Frame-Options'] = 'DENY'
    else:
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # X-Content-Type-Options
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Referrer-Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions-Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=(), payment=()'
    
    # HSTS (only in production)
    if os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

