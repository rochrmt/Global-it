from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import timezone
import os
import json
import time
from PIL import Image
from io import BytesIO

from .models import StaticImage, DashboardActivity, SiteSettings, ImageCategory
from main.models import Service, Formation, SiteConfiguration
from .utils import (
    sync_dashboard_image_to_service,
    sync_dashboard_image_to_formation,
    sync_dashboard_image_to_site_config,
    get_dashboard_images_by_type,
    get_sync_status
)

# Les vues existantes restent ici...

@login_required
def image_site_manager(request):
    """Gestionnaire d'images du site - Interface complète pour gérer toutes les images"""
    
    # Récupérer toutes les images du site
    context = {
        'carousel_images': StaticImage.objects.filter(image_type='carousel', is_active=True).order_by('-created_at'),
        'service_images': Service.objects.filter(est_actif=True).exclude(image='').order_by('-created_at'),
        'formation_images': Formation.objects.filter(disponible=True).exclude(image='').order_by('-created_at'),
        'site_config': SiteConfiguration.objects.filter(est_active=True).first(),
        'dashboard_images': StaticImage.objects.filter(is_active=True).order_by('-created_at'),
        'image_types': StaticImage.IMAGE_TYPES,
    }
    
    return render(request, 'dashboard/image_site_manager.html', context)


@login_required
def update_site_image(request):
    """Mettre à jour une image du site"""
    if request.method == 'POST':
        try:
            content_type = request.POST.get('content_type')  # 'service', 'formation', 'carousel', 'site'
            object_id = request.POST.get('object_id')
            image_source = request.POST.get('image_source')  # 'upload' ou 'dashboard'
            
            if image_source == 'upload':
                # Upload direct
                if 'image_file' not in request.FILES:
                    return JsonResponse({'success': False, 'error': 'Aucun fichier fourni'})
                
                image_file = request.FILES['image_file']
                
                # Créer une image dashboard si nécessaire
                dashboard_image = StaticImage.objects.create(
                    file=image_file,
                    name=f"{content_type}_{object_id}_updated",
                    image_type=content_type,
                    uploaded_by=request.user,
                    is_active=True
                )
                
            else:
                # Utiliser une image existante du dashboard
                dashboard_image_id = request.POST.get('dashboard_image_id')
                dashboard_image = get_object_or_404(StaticImage, id=dashboard_image_id, is_active=True)
            
            # Appliquer l'image au contenu approprié
            if content_type == 'service':
                service = get_object_or_404(Service, id=object_id)
                old_image = service.image
                service.image = dashboard_image.file
                service.save()
                
                # Supprimer l'ancienne image si elle n'est pas utilisée ailleurs
                if old_image and not Service.objects.filter(image=old_image).exists() and not Formation.objects.filter(image=old_image).exists():
                    old_image.delete()
                
            elif content_type == 'formation':
                formation = get_object_or_404(Formation, id=object_id)
                old_image = formation.image
                formation.image = dashboard_image.file
                formation.save()
                
                # Supprimer l'ancienne image si elle n'est pas utilisée ailleurs
                if old_image and not Service.objects.filter(image=old_image).exists() and not Formation.objects.filter(image=old_image).exists():
                    old_image.delete()
                
            elif content_type == 'carousel':
                # Pour le carousel, on met à jour l'image statique correspondante
                if image_source == 'upload':
                    # L'image est déjà créée, on laisse le template l'utiliser
                    pass
                else:
                    # Utiliser l'image du dashboard
                    pass
                
            elif content_type == 'site':
                site_config = SiteConfiguration.objects.filter(est_active=True).first()
                if site_config:
                    old_logo = site_config.logo
                    site_config.logo = dashboard_image.file
                    site_config.save()
                    
                    # Supprimer l'ancien logo s'il n'est pas utilisé ailleurs
                    if old_logo and not SiteConfiguration.objects.filter(logo=old_logo).exists():
                        old_logo.delete()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='update',
                object_type=content_type.capitalize(),
                object_id=object_id,
                description=f"Image mise à jour pour {content_type} #{object_id}"
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Image mise à jour avec succès!',
                'new_image_url': dashboard_image.file.url if dashboard_image.file else ''
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def remove_site_image(request):
    """Supprimer une image du site"""
    if request.method == 'POST':
        try:
            content_type = request.POST.get('content_type')
            object_id = request.POST.get('object_id')
            
            if content_type == 'service':
                service = get_object_or_404(Service, id=object_id)
                if service.image:
                    service.image.delete(save=False)
                    service.image = None
                    service.save()
                    
            elif content_type == 'formation':
                formation = get_object_or_404(Formation, id=object_id)
                if formation.image:
                    formation.image.delete(save=False)
                    formation.image = None
                    formation.save()
                    
            elif content_type == 'site':
                site_config = SiteConfiguration.objects.filter(est_active=True).first()
                if site_config and site_config.logo:
                    site_config.logo.delete(save=False)
                    site_config.logo = None
                    site_config.save()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='delete',
                object_type=content_type.capitalize(),
                object_id=object_id,
                description=f"Image supprimée pour {content_type} #{object_id}"
            )
            
            return JsonResponse({'success': True, 'message': 'Image supprimée avec succès!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def quick_upload_image(request):
    """Upload rapide d'image avec application automatique"""
    if request.method == 'POST':
        try:
            content_type = request.POST.get('content_type')
            object_id = request.POST.get('object_id')
            
            if 'image_file' not in request.FILES:
                return JsonResponse({'success': False, 'error': 'Aucun fichier fourni'})
            
            image_file = request.FILES['image_file']
            
            # Créer l'image dans le dashboard
            dashboard_image = StaticImage.objects.create(
                file=image_file,
                name=f"{content_type}_{object_id}_quick",
                image_type=content_type,
                uploaded_by=request.user,
                is_active=True
            )
            
            # Appliquer immédiatement au contenu
            if content_type == 'service':
                service = get_object_or_404(Service, id=object_id)
                service.image = dashboard_image.file
                service.save()
                
            elif content_type == 'formation':
                formation = get_object_or_404(Formation, id=object_id)
                formation.image = dashboard_image.file
                formation.save()
                
            elif content_type == 'carousel':
                # Pour le carousel, on retourne juste l'URL de l'image uploadée
                pass
                
            elif content_type == 'site':
                site_config = SiteConfiguration.objects.filter(est_active=True).first()
                if site_config:
                    site_config.logo = dashboard_image.file
                    site_config.save()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='upload',
                object_type=content_type.capitalize(),
                object_id=object_id,
                description=f"Image uploadée et appliquée à {content_type} #{object_id}"
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Image uploadée et appliquée avec succès!',
                'new_image_url': dashboard_image.file.url if dashboard_image.file else ''
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)