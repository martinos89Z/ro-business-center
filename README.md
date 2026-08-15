# RO Business Center - Site Web

Site web complet pour Ro Business Center avec gestion de produits, inscriptions aux formations, et panneau d'administration.

## 📋 Fonctionnalités

### Site Public
- **Page d'accueil** avec présentation des services et formations
- **Boutique en ligne** avec catégories de produits (PC, RAM, Chargeurs, Claviers, Souris, Accessoires)
- **Recherche de produits** en temps réel
- **Modal produit** avec caractéristiques détaillées
- **Commande via WhatsApp** avec toutes les caractéristiques du produit
- **Options de paiement** : Total, 2x, 3x, 4x sans frais
- **Inscription aux formations** avec formulaire
- **Formulaire de contact**
- **Navigation responsive** avec menu mobile

### Panneau d'Administration
- **Dashboard** avec statistiques détaillées
- **Gestion des produits** (ajout, modification, suppression)
- **Gestion des catégories**
- **Gestion des images**
- **Messages** (contacts et inscriptions)
- **Paramètres** du site
- **Changement de mot de passe** admin
- **Backup automatique** de la base de données

## � Sécurité

### Mesures de sécurité implémentées
- **SECRET_KEY** stockée dans variable d'environnement (jamais dans le code)
- **Rate limiting** pour limiter les attaques par force brute (5 tentatives de connexion en 5 minutes)
- **Validation des données** de tous les formulaires (longueur, type, format)
- **Limitation des fichiers uploadés** (max 5MB, types autorisés: png, jpg, jpeg, webp)
- **Support PostgreSQL** pour la production (plus robuste que SQLite)
- **HTTPS** activé en production (fourni gratuitement par Render/Heroku)
- **.gitignore** pour protéger les secrets et fichiers sensibles
- **Rate limiting global** (200 requêtes par jour, 50 par heure)

### Variables d'environnement requises
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/ro_business
WHATSAPP_PHONE=22892888759
FLASK_ENV=production

# Google Analytics 4
GA_MEASUREMENT_ID=G-8TYFQTVB0X
```

## �🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd "c:\Users\marti\Desktop\SIte RO"
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env et ajouter vos valeurs
   python -c "import secrets; print(secrets.token_hex(32))"  # Générer SECRET_KEY
   ```

Ajoutez également votre ID Google Analytics (GA4) dans `.env` si vous souhaitez activer le suivi:

```bash
GA_MEASUREMENT_ID=G-8TYFQTVB0X
```

5. **Lancer l'application**
   ```bash
   python app.py
   ```

6. **Accéder au site**
   - Site public : `http://127.0.0.1:5000`
   - Admin : `http://127.0.0.1:5000/admin/login`

## 🔐 Identifiants Admin par défaut

- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin123`

⚠️ **Important** : Changez le mot de passe après la première connexion via les paramètres.

## 📁 Structure du Projet

```
SIte RO/
├── app.py                  # Application Flask principale
├── config.py               # Configuration de l'application
├── models.py               # Modèles de la base de données
├── routes.py               # Routes Flask
├── script.js               # JavaScript pour le frontend
├── style.css               # Styles CSS
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
├── .env.example           # Exemple de variables d'environnement
├── .gitignore             # Fichiers ignorés par Git
├── Procfile               # Configuration pour déploiement (Heroku/Render)
├── runtime.txt            # Version Python pour déploiement
├── gunicorn_config.py     # Configuration Gunicorn
├── instance/
│   └── ro_business.db     # Base de données SQLite (développement)
├── templates/             # Templates HTML
│   ├── index.html         # Page d'accueil
│   ├── pc.html            # Page PC
│   ├── ram.html           # Page RAM
│   ├── chargeurs.html     # Page Chargeurs
│   ├── claviers.html      # Page Claviers
│   ├── souris.html        # Page Souris
│   ├── accessoires.html   # Page Accessoires
│   ├── product_detail.html # Détails produit
│   └── admin/             # Templates admin
│       ├── dashboard.html
│       ├── products.html
│       ├── add_product.html
│       ├── edit_product.html
│       ├── categories.html
│       ├── galerie.html
│       ├── messages.html
│       └── settings.html
├── static/                # Fichiers statiques
│   ├── style.css
│   ├── script.js
│   └── images/           # Images du site
├── uploads/              # Images uploadées par les produits
└── backups/              # Backups automatiques de la base de données
```

## 🌐 Déploiement

### Option 1 : Déploiement Local (Développement)

1. Suivre les étapes d'installation ci-dessus
2. Le site est accessible sur `http://127.0.0.1:5000`

### Option 2 : Déploiement sur Render (Recommandé)

Render fournit gratuitement :
- **HTTPS** automatique
- **PostgreSQL** gratuit
- **Déploiement continu** depuis GitHub
- **SSL/TLS** automatique

#### Étapes :

1. **Préparer le dépôt Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Créer un compte sur [Render](https://render.com)**

3. **Créer une nouvelle Web Service**
   - Connecter votre compte GitHub
   - Sélectionner ce dépôt
   - Configuration :
     - **Build Command** : `pip install -r requirements.txt`
     - **Start Command** : `gunicorn app:app --workers 4 --threads 2 --bind 0.0.0.0:$PORT --timeout 120`
     - **Runtime** : Python 3.11.7

4. **Configurer les variables d'environnement**
   - `SECRET_KEY` : Générer avec `python -c "import secrets; print(secrets.token_hex(32))"`
   - `DATABASE_URL` : Render fournit automatiquement l'URL PostgreSQL
   - `WHATSAPP_PHONE` : `22892888759`
   - `FLASK_ENV` : `production`
 - `GA_MEASUREMENT_ID` : `G-8TYFQTVB0X` (optionnel — Google Analytics 4)

5. **Déployer**
   - Render déploiera automatiquement à chaque push sur GitHub

### Option 3 : Déploiement sur Heroku

1. **Installer Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Se connecter**
   ```bash
   heroku login
   ```

3. **Créer l'application**
   ```bash
   heroku create votre-app-name
   ```

4. **Ajouter PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Configurer les variables d'environnement**
   ```bash
   heroku config:set SECRET_KEY=votre-secret-key
   heroku config:set WHATSAPP_PHONE=22892888759
   heroku config:set FLASK_ENV=production
   heroku config:set GA_MEASUREMENT_ID=G-8TYFQTVB0X
   ```

6. **Déployer**
   ```bash
   git push heroku main
   ```

### Option 4 : Déploiement sur VPS (Ubuntu/Debian)

1. **Installer les dépendances système**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx postgresql
   ```

2. **Créer un environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Configurer PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE ro_business;
   CREATE USER ro_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ro_business TO ro_user;
   \q
   ```

5. **Configurer Gunicorn avec systemd**
   ```bash
   sudo nano /etc/systemd/system/ro_business.service
   ```
   Contenu :
   ```ini
   [Unit]
   Description=RO Business Center Gunicorn
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/SIte RO
   Environment="PATH=/path/to/SIte RO/venv/bin"
   ExecStart=/path/to/SIte RO/venv/bin/gunicorn --config gunicorn_config.py app:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Démarrer le service**
   ```bash
   sudo systemctl start ro_business
   sudo systemctl enable ro_business
   ```

7. **Configurer Nginx**
   ```nginx
   server {
       listen 80;
       server_name votre-domaine.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /uploads {
           alias /path/to/SIte RO/static/uploads;
       }

       location /static {
           alias /path/to/SIte RO/static;
       }
   }
   ```

8. **Activer HTTPS avec Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d votre-domaine.com
   ```

## 💾 Sauvegardes

### Sauvegardes automatiques
Les sauvegardes automatiques de la base de données sont créées dans le dossier `backups/` :
- Après chaque ajout/modification/suppression de produit
- Les 7 derniers backups sont conservés
- Format : `backup_YYYYMMDD_HHMMSS.db` (SQLite) ou `.sql` (PostgreSQL)

### Sauvegardes externes (Production)
Pour la production, utilisez les services de backup de votre hébergeur :
- **Render** : Backups automatiques PostgreSQL inclus
- **Heroku** : Backups automatiques avec pg:backups
- **AWS RDS** : Backups automatiques configurables
- **VPS** : Configurez pg_dump avec cron pour des backups externes

**Ne jamais** utiliser GitHub comme stockage de sauvegarde de données.

## 📝 Configuration

### Modifier le numéro WhatsApp
Dans `script.js`, modifier la fonction `openWhatsApp` :
```javascript
function openWhatsApp(message) {
  const phoneNumber = '22892888759'; // Modifier ce numéro
  const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
  window.open(url, '_blank');
}
```

### Modifier les catégories par défaut
Dans `models.py`, modifier la fonction `ensure_default_categories` :
```python
def ensure_default_categories():
    default_categories = ['PC', 'RAM', 'Chargeurs', 'Claviers', 'Souris', 'Accessoires']
    # Ajouter ou modifier les catégories ici
```

## 🔧 Maintenance

### Mettre à jour les dépendances
```bash
pip install --upgrade -r requirements.txt
```

### Vider le cache
```bash
rm -rf __pycache__
rm -rf instance/__pycache__
```

### Réinitialiser la base de données
```bash
rm instance/ro_business.db
rm instance/ro_business.db # La base sera recréée automatiquement
```

### Vérifier les logs de production
```bash
# Render/Heroku
heroku logs --tail

# VPS avec systemd
sudo journalctl -u ro_business -f

# VPS avec Gunicorn direct
tail -f /var/log/ro_business/error.log
```

## 🛡️ Bonnes pratiques de sécurité

1. **Jamais** commiter les fichiers `.env` ou `.env.local`
2. **Toujours** utiliser des variables d'environnement pour les secrets
3. **Mettre à jour** régulièrement les dépendances Python
4. **Utiliser** HTTPS en production
5. **Limiter** les tentatives de connexion
6. **Valider** toutes les données entrantes
7. **Limiter** la taille des fichiers uploadés
8. **Faire des backups** réguliers sur un stockage externe
9. **Surveiller** les logs pour les activités suspectes
10. **Changer** les mots de passe par défaut

## 📞 Support

Pour toute question ou problème, contactez :
- **Email** : [guinnoukoami@gmail.com](mailto:guinnoukoami@gmail.com)
- **WhatsApp** : +228 92 88 87 59
- **Adresse** : Bè Kpota, Nétadi fin pavé, 200m du Bar BASE 1 – Lomé, Togo

## 📄 Licence

Ce projet est la propriété de Ro Business Center.

---

**Développé par Martinos avec ❤️ pour Ro Business Center**
