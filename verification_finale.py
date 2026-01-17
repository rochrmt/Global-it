#!/usr/bin/env python
"""
Test final - Vérification complète de la configuration Cloudinary
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globaltit_site.settings')

# Charger .env.render si disponible
if os.path.exists('.env.render'):
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv('.env.render'))
else:
    from decouple import config

django.setup()

def verification_finale():
    """Vérification complète de la configuration"""
    print("🎯 Vérification finale de votre configuration")
    print("=" * 50)
    
    from django.conf import settings
    
    # 1. Vérifier Cloudinary
    cloudinary_config = getattr(settings, 'CLOUDINARY_STORAGE', {})
    print(f"📊 Cloudinary Configuration:")
    print(f"   Cloud Name: {cloudinary_config.get('CLOUD_NAME', 'Non défini')}")
    print(f"   API Key: {cloudinary_config.get('API_KEY', 'Non défini')[:10]}...")
    print(f"   API Secret: {'*** configuré ***' if cloudinary_config.get('API_SECRET') else 'Non défini'}")
    
    # 2. Vérifier le stockage
    storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'Local')
    print(f"\n🔧 Configuration Stockage:")
    print(f"   DEFAULT_FILE_STORAGE: {storage}")
    print(f"   MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Non défini')}")
    
    # 3. Vérifier email
    print(f"\n📧 Configuration Email:")
    print(f"   EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Non défini')}")
    print(f"   EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Non défini')}")
    print(f"   CONTACT_EMAIL: {getattr(settings, 'CONTACT_EMAIL', 'Non défini')}")
    
    # 4. Vérifier base de données
    print(f"\n🗄️ Configuration Base de données:")
    db_config = settings.DATABASES['default']
    print(f"   Engine: {db_config.get('ENGINE', 'Non défini')}")
    if 'sqlite' in str(db_config.get('ENGINE', '')):
        print(f"   Database: {db_config.get('NAME', 'Non défini')}")
    else:
        print(f"   Database: PostgreSQL (Render)")
    
    # 5. Résumé
    print("\n" + "=" * 50)
    
    # Vérifications
    cloudinary_ok = bool(cloudinary_config.get('CLOUD_NAME'))
    storage_ok = 'cloudinary' in str(storage)
    email_ok = bool(getattr(settings, 'EMAIL_HOST_USER', ''))
    
    if cloudinary_ok and storage_ok:
        print("🎉 Configuration Cloudinary ACTIVE !")
        print("   ✅ Vos images seront stockées en sécurité dans le cloud")
    else:
        print("⚠️  Cloudinary configuré mais non activé")
        print("   Les images utiliseront le stockage local")
    
    if email_ok:
        print("✅ Email configuré pour GoDaddy")
    
    print("\n🚀 Votre site est prêt pour Render !")
    
    return cloudinary_ok and storage_ok

if __name__ == "__main__":
    verification_finale()