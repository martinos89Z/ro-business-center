"""
Module SEO pour RO Business Center
Optimisation du référencement naturel selon les recommandations de Google
"""

import os
from flask import url_for, request
from urllib.parse import quote


class SEOMetadata:
    """Génération des métadonnées SEO pour chaque page"""
    
    # Informations de l'entreprise
    BUSINESS_NAME = "RO BUSINESS CENTER"
    BUSINESS_DESCRIPTION = (
        "RO BUSINESS CENTER - Votre partenaire informatique à Lomé, Togo. "
        "Vente d'ordinateurs, accessoires informatiques, maintenance, réparation, "
        "réseaux informatiques, formations en informatique et développement web."
    )
    BUSINESS_KEYWORDS = [
        "RO BUSINESS CENTER",
        "vente d'ordinateurs Lomé",
        "vente de PC Togo",
        "accessoires informatiques",
        "maintenance informatique",
        "réparation ordinateurs",
        "réseaux informatiques",
        "formations informatique",
        "développement web",
        "Lomé",
        "Togo"
    ]
    
    # Coordonnées
    ADDRESS = "Bè Kpota, Nétadi, fin pavé, 200 m du Bar BASE 1, Lomé, Togo"
    PHONE = "+228 92 88 87 59"
    EMAIL = "guinnoukoami@gmail.com"
    WHATSAPP = "22892888759"
    
    # Localisation (SEO local)
    CITY = "Lomé"
    REGION = "Maritime"
    COUNTRY = "Togo"
    LATITUDE = 6.1283  # Coordonnées approximatives de Lomé
    LONGITUDE = 1.2253
    
    # Réseaux sociaux (à configurer)
    SOCIAL_MEDIA = {
        "facebook": "https://facebook.com/robusinesscenter",
        "instagram": "https://instagram.com/robusinesscenter",
        "linkedin": "https://linkedin.com/company/robusinesscenter",
        "twitter": "https://twitter.com/robusinesscenter"
    }
    
    # URL du site (à configurer en production)
    BASE_URL = "https://robusinesscenter.onrender.com"  # À remplacer par l'URL réelle
    
    @staticmethod
    def get_page_metadata(page_name, additional_info=None):
        """
        Génère les métadonnées SEO pour une page spécifique
        
        Args:
            page_name: Nom de la page (home, pc, ram, etc.)
            additional_info: Informations supplémentaires (produit, catégorie, etc.)
        
        Returns:
            Dictionnaire contenant toutes les métadonnées SEO
        """
        metadata = {
            "title": "",
            "description": "",
            "keywords": "",
            "canonical": "",
            "og_title": "",
            "og_description": "",
            "og_image": "",
            "og_type": "website",
            "twitter_card": "summary_large_image"
        }
        
        page_info = additional_info or {}
        
        # Métadonnées spécifiques par page
        if page_name == "home":
            metadata["title"] = f"{SEOMetadata.BUSINESS_NAME} | Vente d'ordinateurs & Services Informatiques à Lomé"
            metadata["description"] = (
                f"{SEOMetadata.BUSINESS_DESCRIPTION} "
                f"Trouvez les meilleurs PC, accessoires et services informatiques au Togo. "
                f"Situation : {SEOMetadata.ADDRESS}. Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = ", ".join(SEOMetadata.BUSINESS_KEYWORDS)
            metadata["og_type"] = "website"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-home.jpg"
            
        elif page_name == "pc":
            metadata["title"] = "Vente d'Ordinateurs PC à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Achetez des ordinateurs PC de qualité à Lomé, Togo. "
                "RO BUSINESS CENTER vous propose une large gamme de PC portables et de bureau. "
                f"Contactez-nous : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "vente ordinateurs Lomé, vente PC Togo, PC portables, PC bureau, ordinateurs pas cher"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-pc.jpg"
            
        elif page_name == "ram":
            metadata["title"] = "Vente de Mémoire RAM à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Mémoire RAM de haute performance pour vos ordinateurs à Lomé, Togo. "
                "RO BUSINESS CENTER - Amélioration et mise à niveau de PC. "
                f"Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "vente RAM Lomé, mémoire RAM Togo, upgrade RAM, DDR4, DDR3, mémoire ordinateur"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-ram.jpg"
            
        elif page_name == "chargeurs":
            metadata["title"] = "Vente de Chargeurs Ordinateur à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Chargeurs d'ordinateur universels et originaux à Lomé, Togo. "
                "RO BUSINESS CENTER - Tous types de chargeurs pour PC et laptops. "
                f"Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "vente chargeurs Lomé, chargeur ordinateur Togo, chargeur laptop, adaptateur secteur"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-chargeurs.jpg"
            
        elif page_name == "claviers":
            metadata["title"] = "Vente de Claviers à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Claviers d'ordinateur mécaniques et standard à Lomé, Togo. "
                "RO BUSINESS CENTER - Large choix de claviers pour tous les usages. "
                f"Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "vente claviers Lomé, clavier ordinateur Togo, clavier mécanique, clavier gaming"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-claviers.jpg"
            
        elif page_name == "souris":
            metadata["title"] = "Vente de Souris à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Souris d'ordinateur filaires et sans fil à Lomé, Togo. "
                "RO BUSINESS CENTER - Souris ergonomiques et gaming. "
                f"Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "vente souris Lomé, souris ordinateur Togo, souris sans fil, souris gaming"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-souris.jpg"
            
        elif page_name == "accessoires":
            metadata["title"] = "Accessoires Informatiques à Lomé | RO BUSINESS CENTER"
            metadata["description"] = (
                "Tous les accessoires informatiques à Lomé, Togo. "
                "RO BUSINESS CENTER - Câbles, hubs, écrans, et plus encore. "
                f"Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = "accessoires informatiques Lomé, périphériques PC Togo, matériel informatique"
            metadata["og_type"] = "product"
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-accessoires.jpg"
            
        elif page_name == "product" and page_info.get("product_name"):
            product_name = page_info["product_name"]
            metadata["title"] = f"{product_name} | RO BUSINESS CENTER Lomé"
            metadata["description"] = (
                f"Achetez {product_name} à Lomé, Togo. "
                f"{page_info.get('description', '')[:150]}... "
                f"RO BUSINESS CENTER - Qualité garantie. Contact : {SEOMetadata.PHONE}"
            )
            metadata["keywords"] = f"{product_name}, vente {product_name} Lomé, {product_name} Togo"
            metadata["og_type"] = "product"
            metadata["og_image"] = page_info.get("image", f"{SEOMetadata.BASE_URL}/static/images/og-product.jpg")
            
        else:
            # Page par défaut
            metadata["title"] = f"{SEOMetadata.BUSINESS_NAME} | Services Informatiques à Lomé, Togo"
            metadata["description"] = SEOMetadata.BUSINESS_DESCRIPTION
            metadata["keywords"] = ", ".join(SEOMetadata.BUSINESS_KEYWORDS)
            metadata["og_image"] = f"{SEOMetadata.BASE_URL}/static/images/og-default.jpg"
        
        # Open Graph (même que title/description par défaut)
        metadata["og_title"] = metadata["title"]
        metadata["og_description"] = metadata["description"]
        
        # URL canonique relative ; full URL ajouté lors du rendu
        metadata["canonical"] = request.path
        
        return metadata
    
    @staticmethod
    def render_meta_tags(metadata):
        """Génère les balises meta HTML"""
        base_url = os.getenv('BASE_URL', 'https://robusinesscenter.onrender.com')
        tags = []
        
        # Meta tags de base
        tags.append(f'<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        tags.append(f'<title>{metadata["title"]}</title>')
        tags.append(f'<meta name="description" content="{metadata["description"]}">')
        tags.append(f'<meta name="keywords" content="{metadata["keywords"]}">')
        tags.append(f'<meta name="author" content="RO BUSINESS CENTER">')
        
        # Canonical URL
        tags.append(f'<link rel="canonical" href="{base_url}{metadata["canonical"]}">')
        
        # Favicon (utilise le logo existant avec chemin relatif pour éviter les dépendances DNS)
        tags.append('<link rel="icon" href="/static/images/logo.jpeg" type="image/jpeg">')
        tags.append('<link rel="shortcut icon" href="/static/images/logo.jpeg" type="image/jpeg">')
        
        # Theme color (couleur de marque RO BUSINESS CENTER)
        tags.append(f'<meta name="theme-color" content="#2563eb">')
        tags.append(f'<meta name="msapplication-TileColor" content="#2563eb">')
        
        # Open Graph
        tags.append(f'<meta property="og:title" content="{metadata["og_title"]}">')
        tags.append(f'<meta property="og:description" content="{metadata["og_description"]}">')
        tags.append(f'<meta property="og:type" content="{metadata["og_type"]}">')
        tags.append(f'<meta property="og:url" content="{base_url}{metadata["canonical"]}">')
        tags.append(f'<meta property="og:image" content="{metadata["og_image"]}">')
        tags.append(f'<meta property="og:site_name" content="RO BUSINESS CENTER">')
        tags.append(f'<meta property="og:locale" content="fr_TG">')
        
        # Twitter Card
        tags.append(f'<meta name="twitter:card" content="{metadata["twitter_card"]}">')
        tags.append(f'<meta name="twitter:title" content="{metadata["title"]}">')
        tags.append(f'<meta name="twitter:description" content="{metadata["description"]}">')
        tags.append(f'<meta name="twitter:image" content="{metadata["og_image"]}">')
        
        # Robots
        tags.append(f'<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">')
        
        # Language
        tags.append(f'<meta http-equiv="content-language" content="fr">')
        
        # Web manifest
        tags.append(f'<link rel="manifest" href="/manifest.webmanifest">')
        
        return '\n    '.join(tags)


class StructuredData:
    """Génération des données structurées JSON-LD (Schema.org)"""
    
    @staticmethod
    def get_local_business():
        """
        Génère les données structurées pour LocalBusiness
        
        Returns:
            Dictionnaire JSON-LD Schema.org
        """
        return {
            "@context": "https://schema.org",
            "@type": "ComputerStore",
            "name": SEOMetadata.BUSINESS_NAME,
            "description": SEOMetadata.BUSINESS_DESCRIPTION,
            "url": SEOMetadata.BASE_URL,
            "telephone": SEOMetadata.PHONE,
            "email": SEOMetadata.EMAIL,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Bè Kpota, Nétadi, fin pavé, 200 m du Bar BASE 1",
                "addressLocality": SEOMetadata.CITY,
                "addressRegion": SEOMetadata.REGION,
                "addressCountry": SEOMetadata.COUNTRY
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": SEOMetadata.LATITUDE,
                "longitude": SEOMetadata.LONGITUDE
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday"
                ],
                "opens": "08:00",
                "closes": "18:00"
            },
            "priceRange": "$$",
            "image": f"{SEOMetadata.BASE_URL}/static/images/logo.jpg",
            "logo": f"{SEOMetadata.BASE_URL}/static/images/logo.jpg",
            "sameAs": list(SEOMetadata.SOCIAL_MEDIA.values()),
            "areaServed": {
                "@type": "GeoCircle",
                "geoMidpoint": {
                    "@type": "GeoCoordinates",
                    "latitude": SEOMetadata.LATITUDE,
                    "longitude": SEOMetadata.LONGITUDE
                },
                "geoRadius": "50000"
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Produits et Services Informatiques",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Product",
                            "name": "Ordinateurs PC"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Product",
                            "name": "Accessoires Informatiques"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Maintenance Informatique"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Formation Informatique"
                        }
                    }
                ]
            }
        }
    
    @staticmethod
    def get_breadcrumb_list(items):
        """
        Génère les données structurées pour BreadcrumbList
        
        Args:
            items: Liste de tuples (nom, url)
        
        Returns:
            Dictionnaire JSON-LD Schema.org
        """
        breadcrumb_items = []
        for i, (name, url) in enumerate(items, 1):
            breadcrumb_items.append({
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": f"{SEOMetadata.BASE_URL}{url}"
            })
        
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items
        }
    
    @staticmethod
    def get_product(product_data):
        """
        Génère les données structurées pour un produit
        
        Args:
            product_data: Dictionnaire avec les données du produit
        
        Returns:
            Dictionnaire JSON-LD Schema.org
        """
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product_data.get("name", ""),
            "description": product_data.get("description", ""),
            "image": product_data.get("images", []),
            "brand": {
                "@type": "Brand",
                "name": product_data.get("brand", "RO BUSINESS CENTER")
            },
            "offers": {
                "@type": "Offer",
                "price": str(product_data.get("price", 0)),
                "priceCurrency": "XOF",
                "availability": "https://schema.org/InStock" if product_data.get("availability") == "Disponible" else "https://schema.org/OutOfStock",
                "seller": {
                    "@type": "Organization",
                    "name": SEOMetadata.BUSINESS_NAME
                }
            }
        }
    
    @staticmethod
    def render_json_ld(data):
        """
        Génère le HTML script pour les données structurées
        
        Args:
            data: Dictionnaire JSON-LD
        
        Returns:
            String HTML du script
        """
        import json
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


class SitemapGenerator:
    """Génération du sitemap.xml dynamique"""
    
    @staticmethod
    def generate_sitemap():
        """
        Génère le sitemap.xml avec toutes les pages du site
        
        Returns:
            String XML du sitemap
        """
        from datetime import datetime
        from models import Product, Category
        
        base_url = SEOMetadata.BASE_URL
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Pages statiques
        static_pages = [
            ("", "daily", "1.0"),
            ("/pc", "weekly", "0.8"),
            ("/ram", "weekly", "0.8"),
            ("/chargeurs", "weekly", "0.8"),
            ("/claviers", "weekly", "0.8"),
            ("/souris", "weekly", "0.8"),
            ("/accessoires", "weekly", "0.8"),
        ]
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Pages statiques
        for path, changefreq, priority in static_pages:
            xml += f'  <url>\n'
            xml += f'    <loc>{base_url}{path}</loc>\n'
            xml += f'    <lastmod>{current_date}</lastmod>\n'
            xml += f'    <changefreq>{changefreq}</changefreq>\n'
            xml += f'    <priority>{priority}</priority>\n'
            xml += f'  </url>\n'
        
        # Pages de produits (si disponibles)
        try:
            products = Product.all()
            for product in products:
                xml += f'  <url>\n'
                xml += f'    <loc>{base_url}/product/{product["id"]}</loc>\n'
                xml += f'    <lastmod>{current_date}</lastmod>\n'
                xml += f'    <changefreq>weekly</changefreq>\n'
                xml += f'    <priority>0.6</priority>\n'
                xml += f'  </url>\n'
        except:
            pass
        
        xml += '</urlset>'
        return xml


class RobotsTxt:
    """Génération du robots.txt"""
    
    @staticmethod
    def generate():
        """
        Génère le robots.txt
        
        Returns:
            String du robots.txt
        """
        base_url = SEOMetadata.BASE_URL
        
        return f"""# Robots.txt pour {SEOMetadata.BUSINESS_NAME}
# Permet aux robots d'explorer le site

User-agent: *
Allow: /

# Sitemap
Sitemap: {base_url}/sitemap.xml

# Interdire l'accès aux pages d'administration
Disallow: /admin/
Disallow: /uploads/

# Interdire l'accès aux fichiers de configuration
Disallow: /config.py
Disallow: /.env
Disallow: /requirements.txt

# Crawl-delay pour éviter la surcharge
Crawl-delay: 1
"""


class WebManifest:
    """Génération du manifest.webmanifest pour PWA"""
    
    @staticmethod
    def generate():
        """
        Génère le manifest.webmanifest
        
        Returns:
            Dictionnaire JSON du manifest
        """
        return {
            "name": SEOMetadata.BUSINESS_NAME,
            "short_name": "RO Business",
            "description": SEOMetadata.BUSINESS_DESCRIPTION,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#0066cc",
            "orientation": "portrait",
            "scope": "/",
            "icons": [
                {
                    "src": "/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "categories": ["business", "shopping"],
            "shortcuts": [
                {
                    "name": "PC",
                    "short_name": "PC",
                    "description": "Vente d'ordinateurs",
                    "url": "/pc",
                    "icons": [{"src": "/icon-96x96.png", "sizes": "96x96"}]
                },
                {
                    "name": "Accessoires",
                    "short_name": "Accessoires",
                    "description": "Accessoires informatiques",
                    "url": "/accessoires",
                    "icons": [{"src": "/icon-96x96.png", "sizes": "96x96"}]
                }
            ]
        }
