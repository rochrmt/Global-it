# GlobalTit Site Vitrine

Site vitrine professionnel pour GlobalTit - Services informatiques et formations.

## 🚀 Fonctionnalités

- **Gestion des services** : Présentation des services informatiques
- **Gestion des formations** : Catalogue de formations avec détails
- **Système de dashboard** : Interface d'administration intuitive
- **Gestion des images** : Système de gestion d'images avec synchronisation
- **Partenaires** : Présentation des partenaires
- **Témoignages clients** : Avis et retours d'expérience
- **Responsive design** : Compatible mobile et tablette

## 📋 Prérequis

- Python 3.8+
- Django 4.2+
- pip (gestionnaire de paquets Python)

## 🔧 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/globaltit-site.git
cd globaltit-site
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

Copier le fichier d'exemple et le configurer :

```bash
cp .env.example .env
```

Modifier le fichier `.env` avec vos configurations :

```env
# Générer une clé secrète sécurisée
SECRET_KEY=votre-clé-secrète-générée

# Mode production
DEBUG=False

# Votre domaine
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com

# Configuration email
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
```

### 5. Préparer la base de données

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

## 🗄️ Configuration de la base de données

### SQLite (développement)

Par défaut, le projet utilise SQLite. Aucune configuration supplémentaire n'est nécessaire.

### PostgreSQL (production recommandée)

```bash
pip install psycopg2-binary
```

Modifier le fichier `.env` :

```env
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

Et mettre à jour `settings.py` pour utiliser cette variable.

## 📧 Configuration Email

Pour Gmail :
1. Activer l'authentification à 2 facteurs
2. Créer un mot de passe d'application
3. Utiliser ce mot de passe dans `EMAIL_HOST_PASSWORD`

## 🔒 Sécurité en production

### HTTPS

Activer les paramètres de sécurité dans `.env` :

```env
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
```

### Autres recommandations

- Utiliser un serveur WSGI comme Gunicorn
- Configurer Nginx comme proxy inverse
- Activer le firewall
- Utiliser SSL/TLS
- Mettre à jour régulièrement les dépendances

## 🚀 Déploiement

### Avec Gunicorn

```bash
pip install gunicorn
gunicorn globaltit_site.wsgi:application --bind 0.0.0.0:8000
```

### Avec Docker (recommandé)

Créer un `Dockerfile` et un `docker-compose.yml` (fichiers non inclus dans ce repo).

### Plateformes de déploiement

- **Heroku** : Support natif des applications Django
- **DigitalOcean** : VPS avec Docker
- **AWS** : EC2 ou Elastic Beanstalk
- **PythonAnywhere** : Hébergement Python spécialisé

## 📁 Structure du projet

```
globaltit-site/
├── dashboard/          # Application dashboard
├── main/               # Application principale
├── globaltit_site/     # Configuration Django
├── media/              # Fichiers média
├── static/             # Fichiers statiques
├── templates/          # Templates HTML
├── requirements.txt    # Dépendances Python
└── manage.py          # Script de gestion Django
```

## 🛠️ Maintenance

### Sauvegardes

- Base de données : `python manage.py dumpdata > backup.json`
- Fichiers média : Copier le dossier `media/`

### Mises à jour

```bash
pip install --upgrade -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🐛 Support

Pour les problèmes ou questions :
- Créer une issue sur GitHub
- Consulter la documentation Django
- Vérifier les logs d'erreur

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.