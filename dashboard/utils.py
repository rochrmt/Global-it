"""
Utilitaires pour la synchronisation entre le dashboard et le site principal
"""
from django.core.files import File
from django.core.files.storage import default_storage
from django.conf import settings
import os
import shutil
from .models import StaticImage
from main.models import Service, Formation, SiteConfiguration, CarouselImage, AboutImage


def sync_dashboard_image_to_service(dashboard_image, service_id):
    """
    Synchronise une image du dashboard vers un service
    """
    try:
        service = Service.objects.get(id=service_id)
        
        # Copier le fichier vers le répertoire des services
        if dashboard_image.file:
            # Créer le répertoire de destination s'il n'existe pas
            service_dir = os.path.join(settings.MEDIA_ROOT, 'services')
            os.makedirs(service_dir, exist_ok=True)
            
            # Copier le fichier
            filename = os.path.basename(dashboard_image.file.name)
            dest_path = os.path.join('services', filename)
            full_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
            
            # Copier le fichier physique
            shutil.copy(dashboard_image.file.path, full_dest_path)
            
            # Mettre à jour le service
            service.image = dest_path
            service.save()
            
            return True, "Image synchronisée avec succès"
    except Service.DoesNotExist:
        return False, "Service non trouvé"
    except Exception as e:
        return False, f"Erreur lors de la synchronisation: {str(e)}"


def sync_dashboard_image_to_about(dashboard_image, about_id):
    """
    Synchronise une image du dashboard vers la section about
    """
    try:
        about_image = AboutImage.objects.get(id=about_id)
        
        if dashboard_image.file:
            # Créer le répertoire de destination
            about_dir = os.path.join(settings.MEDIA_ROOT, 'about')
            os.makedirs(about_dir, exist_ok=True)
            
            # Copier le fichier
            filename = os.path.basename(dashboard_image.file.name)
            dest_path = os.path.join('about', filename)
            full_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
            
            # Copier le fichier physique
            shutil.copy(dashboard_image.file.path, full_dest_path)
            
            # Mettre à jour l'image about
            about_image.image = dest_path
            about_image.save()
            
            return True, "Image synchronisée avec succès"
    except AboutImage.DoesNotExist:
        return False, "Image about non trouvée"
    except Exception as e:
        return False, f"Erreur lors de la synchronisation: {str(e)}"


def sync_dashboard_image_to_formation(dashboard_image, formation_id):
    """
    Synchronise une image du dashboard vers une formation
    """
    try:
        formation = Formation.objects.get(id=formation_id)
        
        print(f"DEBUG: Formation trouvée: {formation.titre}")
        print(f"DEBUG: Dashboard image file: {dashboard_image.file}")
        print(f"DEBUG: Dashboard image file path: {dashboard_image.file.path if dashboard_image.file else 'No file'}")
        
        if dashboard_image.file:
            # Créer le répertoire de destination
            formation_dir = os.path.join(settings.MEDIA_ROOT, 'formations')
            os.makedirs(formation_dir, exist_ok=True)
            
            # Copier le fichier
            filename = os.path.basename(dashboard_image.file.name)
            dest_path = os.path.join('formations', filename)
            full_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
            
            print(f"DEBUG: Copying file from {dashboard_image.file.path} to {full_dest_path}")
            
            # Copier le fichier physique
            shutil.copy(dashboard_image.file.path, full_dest_path)
            
            # Mettre à jour la formation
            formation.image = dest_path
            formation.save()
            
            print(f"DEBUG: Formation image updated to {dest_path}")
            
            return True, "Image synchronisée avec succès"
        else:
            print(f"DEBUG: No file found in dashboard_image")
            return False, "Aucun fichier image trouvé"
            
    except Formation.DoesNotExist:
        print(f"DEBUG: Formation non trouvée avec ID {formation_id}")
        return False, "Formation non trouvée"
    except Exception as e:
        print(f"DEBUG: Exception lors de la synchronisation: {str(e)}")
        return False, f"Erreur lors de la synchronisation: {str(e)}"


def sync_dashboard_image_to_site_config(dashboard_image, config_field):
    """
    Synchronise une image du dashboard vers la configuration du site
    """
    try:
        config = SiteConfiguration.get_config()
        
        if dashboard_image.file:
            # Créer le répertoire de destination
            config_dir = os.path.join(settings.MEDIA_ROOT, 'config')
            os.makedirs(config_dir, exist_ok=True)
            
            # Copier le fichier
            filename = os.path.basename(dashboard_image.file.name)
            dest_path = os.path.join('config', filename)
            full_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
            
            # Copier le fichier physique
            shutil.copy(dashboard_image.file.path, full_dest_path)
            
            # Mettre à jour la configuration
            if config_field == 'hero_image':
                config.hero_image = dest_path
            elif config_field == 'about_image':
                config.about_image = dest_path
            elif config_field == 'logo':
                config.logo = dest_path
            
            config.save()
            
            return True, "Image synchronisée avec succès"
    except Exception as e:
        return False, f"Erreur lors de la synchronisation: {str(e)}"


def sync_dashboard_image_to_carousel(dashboard_image, carousel_id):
    """
    Synchronise une image du dashboard vers le carousel
    """
    try:
        carousel_image = CarouselImage.objects.get(id=carousel_id)
        
        if dashboard_image.file:
            # Créer le répertoire de destination
            carousel_dir = os.path.join(settings.MEDIA_ROOT, 'carousel')
            os.makedirs(carousel_dir, exist_ok=True)
            
            # Copier le fichier
            filename = os.path.basename(dashboard_image.file.name)
            dest_path = os.path.join('carousel', filename)
            full_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
            
            # Copier le fichier physique
            shutil.copy(dashboard_image.file.path, full_dest_path)
            
            # Mettre à jour le carousel
            carousel_image.image = dest_path
            carousel_image.save()
            
            return True, "Image synchronisée avec succès"
    except CarouselImage.DoesNotExist:
        return False, "Image du carousel non trouvée"
    except Exception as e:
        return False, f"Erreur lors de la synchronisation: {str(e)}"


def get_dashboard_images_by_type(image_type):
    """
    Récupère les images du dashboard par type
    """
    return StaticImage.objects.filter(image_type=image_type, is_active=True)


def get_sync_status():
    """
    Retourne le statut de synchronisation entre dashboard et site
    """
    from main.models import Service, Formation, CarouselImage, AboutImage
    
    services_without_images = Service.objects.filter(image__isnull=True).count()
    formations_without_images = Formation.objects.filter(image__isnull=True).count()
    
    available_carousel_images = CarouselImage.objects.filter(est_actif=True).count()
    available_about_images = AboutImage.objects.filter(est_actif=True).count()
    available_service_images = StaticImage.objects.filter(image_type='service', is_active=True).count()
    available_formation_images = StaticImage.objects.filter(image_type='formation', is_active=True).count()
    
    return {
        'services_without_images': services_without_images,
        'formations_without_images': formations_without_images,
        'available_carousel_images': available_carousel_images,
        'available_about_images': available_about_images,
        'available_service_images': available_service_images,
        'available_formation_images': available_formation_images,
    }