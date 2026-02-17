#!/usr/bin/env python
"""
Vérification de l'envoi d'email et de la création du contact
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globaltit_site.settings')
django.setup()

def verifier_email_et_contact():
    """Vérifie que l'email a été envoyé et le contact créé"""
    from main.models import Contact
    from django.core.mail import send_mail
    from django.conf import settings
    
    # Vérifier les derniers contacts
    derniers_contacts = Contact.objects.all().order_by('-date_creation')[:5]
    print("📋 Derniers contacts créés:")
    for contact in derniers_contacts:
        print(f"  - {contact.nom} ({contact.email}) - {contact.sujet}")
    
    # Vérifier la configuration email
    print(f"\n📧 Configuration email:")
    print(f"  - DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  - CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    print(f"  - EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    
    # Test d'envoi d'email simple
    try:
        result = send_mail(
            'Test de vérification',
            'Ceci est un test de vérification du système email.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        print(f"\n✅ Email de test envoyé avec succès (résultat: {result})")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'envoi de l'email de test: {e}")
    
    print("\n✅ Vérification terminée!")

if __name__ == '__main__':
    verifier_email_et_contact()