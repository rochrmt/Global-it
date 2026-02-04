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
from django.db.models import Q
from django.core.paginator import Paginator
import os
import json
import time
from PIL import Image
from io import BytesIO

from .models import StaticImage, DashboardActivity, SiteSettings, ImageCategory
from .forms import PartnerForm
from main.models import (
    Service, Formation, SiteConfiguration, CarouselImage, AboutImage, Partner,
    OffreEmploi, Candidature, CandidatureSpontanee
)
from main.forms import OffreEmploiForm
from .utils import (
    sync_dashboard_image_to_service,
    sync_dashboard_image_to_formation,
    sync_dashboard_image_to_site_config,
    get_dashboard_images_by_type,
    get_sync_status
)


def dashboard_login(request):
    """Page de connexion au dashboard"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Enregistrer l'activité
            DashboardActivity.objects.create(
                user=user,
                action='login',
                object_type='User',
                object_id=user.id,
                description='Connexion au dashboard'
            )
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Identifiants invalides')
    
    return render(request, 'dashboard/login.html')


@login_required
def dashboard_logout(request):
    """Déconnexion du dashboard"""
    # Enregistrer l'activité
    DashboardActivity.objects.create(
        user=request.user,
        action='logout',
        object_type='User',
        object_id=request.user.id,
        description='Déconnexion du dashboard'
    )
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('dashboard:login')


@login_required
def home(request):
    """Page d'accueil du dashboard"""
    # Statistiques
    total_images = StaticImage.objects.count()
    active_images = StaticImage.objects.filter(is_active=True).count()
    total_carousel_images = CarouselImage.objects.count()
    active_carousel_images = CarouselImage.objects.filter(est_actif=True).count()
    total_services = Service.objects.count()
    total_formations = Formation.objects.count()
    
    # Activités récentes
    recent_activities = DashboardActivity.objects.select_related('user').order_by('-timestamp')[:10]
    
    context = {
        'total_images': total_images,
        'active_images': active_images,
        'total_carousel_images': total_carousel_images,
        'active_carousel_images': active_carousel_images,
        'total_services': total_services,
        'total_formations': total_formations,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def image_manager(request):
    """Gestionnaire d'images avec vue d'ensemble complète"""
    images = StaticImage.objects.select_related('uploaded_by')
    
    # Filtrage
    image_type = request.GET.get('type')
    if image_type:
        images = images.filter(image_type=image_type)
    
    status = request.GET.get('status')
    if status:
        images = images.filter(is_active=(status == 'active'))
    
    search = request.GET.get('search')
    if search:
        images = images.filter(name__icontains=search)
    
    # Statistiques détaillées
    total_images = images.count()
    active_images = images.filter(is_active=True).count()
    inactive_images = images.filter(is_active=False).count()
    
    # Images par type
    images_by_type = {}
    for type_value, type_label in StaticImage.IMAGE_TYPES:
        count = images.filter(image_type=type_value).count()
        images_by_type[type_label] = count
    
    # Images récemment uploadées (7 derniers jours)
    recent_images = images.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count()
    
    # Images non utilisées (non synchronisées)
    unused_images = []
    for image in images:
        is_used = (
            Service.objects.filter(image=image.file).exists() or
            Formation.objects.filter(image=image.file).exists() or
            SiteConfiguration.objects.filter(logo=image.file).exists() or
            SiteConfiguration.objects.filter(hero_image=image.file).exists() or
            SiteConfiguration.objects.filter(about_image=image.file).exists()
        )
        if not is_used:
            unused_images.append(image)
    
    context = {
        'images': images.order_by('-created_at'),
        'image_types': StaticImage.IMAGE_TYPES,
        'current_filters': {
            'type': image_type,
            'status': status,
            'search': search,
        },
        'statistics': {
            'total': total_images,
            'active': active_images,
            'inactive': inactive_images,
            'recent': recent_images,
            'unused_count': len(unused_images),
        },
        'images_by_type': images_by_type,
        'unused_images': unused_images[:10],  # Top 10 unused images
    }
    return render(request, 'dashboard/image_manager.html', context)


@login_required
def upload_image(request):
    """Upload d'images"""
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        image_type = request.POST.get('image_type', 'other')
        category_id = request.POST.get('category')
        
        uploaded_count = 0
        for file in files:
            try:
                # Créer l'image
                static_image = StaticImage.objects.create(
                    file=file,
                    image_type=image_type,
                    uploaded_by=request.user
                )
                
                # Ajouter la catégorie si spécifiée
                if category_id:
                    try:
                        category = ImageCategory.objects.get(id=category_id)
                        static_image.imagecategory_set.add(category)
                    except ImageCategory.DoesNotExist:
                        pass
                
                uploaded_count += 1
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='upload',
                    object_type='StaticImage',
                    object_id=static_image.id,
                    description=f"Image uploadée: {static_image.name}"
                )
                
            except Exception as e:
                messages.error(request, f"Erreur lors de l'upload de {file.name}: {str(e)}")
        
        if uploaded_count > 0:
            messages.success(request, f"{uploaded_count} image(s) uploadée(s) avec succès!")
        
        return redirect('dashboard:image_manager')
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
@require_POST
def toggle_image_status(request, image_id):
    """Basculer le statut actif/inactif d'une image avec mise à jour en temps réel"""
    try:
        image = StaticImage.objects.get(id=image_id)
        image.is_active = not image.is_active
        image.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='StaticImage',
            object_id=image.id,
            description=f"Image {'activée' if image.is_active else 'désactivée'}: {image.name}"
        )
        
        # Retourner les statistiques mises à jour
        total_images = StaticImage.objects.count()
        active_images = StaticImage.objects.filter(is_active=True).count()
        inactive_images = StaticImage.objects.filter(is_active=False).count()
        
        return JsonResponse({
            'success': True, 
            'is_active': image.is_active,
            'statistics': {
                'total': total_images,
                'active': active_images,
                'inactive': inactive_images,
            }
        })
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})


@login_required
def carousel_manager(request):
    """Gestion des images du carousel"""
    carousel_images = CarouselImage.objects.all().order_by('ordre')
    
    context = {
        'carousel_images': carousel_images,
        'total_images': carousel_images.count(),
        'active_images': carousel_images.filter(est_actif=True).count(),
    }
    return render(request, 'dashboard/carousel_manager.html', context)


@login_required
def about_manager(request):
    """Gestion des images de la section à propos"""
    about_images = AboutImage.objects.all().order_by('ordre')
    
    context = {
        'about_images': about_images,
        'total_images': about_images.count(),
        'active_images': about_images.filter(est_actif=True).count(),
    }
    return render(request, 'dashboard/about_manager.html', context)


@login_required
def add_carousel_image(request):
    """Ajouter une nouvelle image au carousel"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        image_file = request.FILES.get('image')
        
        if titre and image_file:
            try:
                carousel_image = CarouselImage.objects.create(
                    titre=titre,
                    description=description,
                    ordre=int(ordre) if ordre else 0,
                    image=image_file,
                    est_actif=True
                )
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='create',
                    object_type='CarouselImage',
                    object_id=carousel_image.id,
                    description=f"Image carousel ajoutée: {titre}"
                )
                
                messages.success(request, 'Image carousel ajoutée avec succès!')
                return redirect('dashboard:carousel_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')
    
    return render(request, 'dashboard/add_carousel_image.html')


@login_required
def add_about_image(request):
    """Ajouter une nouvelle image à la section about"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        image_file = request.FILES.get('image')
        
        if titre and image_file:
            try:
                about_image = AboutImage.objects.create(
                    titre=titre,
                    description=description,
                    ordre=ordre,
                    image=image_file
                )
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='create',
                    object_type='AboutImage',
                    object_id=about_image.id,
                    description=f"Image about créée: {titre}"
                )
                
                messages.success(request, 'Image about ajoutée avec succès!')
                return redirect('dashboard:about_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
    
    return render(request, 'dashboard/add_about_image.html')


@login_required
def edit_about_image(request, image_id):
    """Modifier une image de la section about"""
    about_image = get_object_or_404(AboutImage, id=image_id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        est_actif = request.POST.get('est_actif') == 'on'
        
        if titre:
            try:
                about_image.titre = titre
                about_image.description = description
                about_image.ordre = ordre
                about_image.est_actif = est_actif
                
                # Gérer le remplacement d'image
                if request.FILES.get('image'):
                    about_image.image = request.FILES.get('image')
                
                about_image.save()
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='update',
                    object_type='AboutImage',
                    object_id=about_image.id,
                    description=f"Image about modifiée: {titre}"
                )
                
                messages.success(request, 'Image about modifiée avec succès!')
                return redirect('dashboard:about_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de la modification: {str(e)}')
        else:
            messages.error(request, 'Le titre est obligatoire.')
    
    context = {
        'about_image': about_image,
    }
    return render(request, 'dashboard/edit_about_image.html', context)


@login_required
def delete_about_image(request, image_id):
    """Supprimer une image de la section about"""
    about_image = get_object_or_404(AboutImage, id=image_id)
    
    if request.method == 'POST':
        try:
            titre = about_image.titre
            about_image.delete()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='delete',
                object_type='AboutImage',
                object_id=image_id,
                description=f"Image about supprimée: {titre}"
            )
            
            messages.success(request, 'Image about supprimée avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
    
    return redirect('dashboard:about_manager')


@login_required
def toggle_about_status(request, image_id):
    """Activer/désactiver une image de la section about"""
    about_image = get_object_or_404(AboutImage, id=image_id)
    
    if request.method == 'POST':
        try:
            about_image.est_actif = not about_image.est_actif
            about_image.save()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='toggle',
                object_type='AboutImage',
                object_id=about_image.id,
                description=f"Image about {'activée' if about_image.est_actif else 'désactivée'}: {about_image.titre}"
            )
            
            messages.success(request, f"Image about {'activée' if about_image.est_actif else 'désactivée'}!")
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    return redirect('dashboard:about_manager')


@login_required
def edit_carousel_image(request, image_id):
    """Modifier une image du carousel"""
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        est_actif = request.POST.get('est_actif') == 'on'
        
        if titre:
            try:
                carousel_image.titre = titre
                carousel_image.description = description
                carousel_image.ordre = int(ordre) if ordre else 0
                carousel_image.est_actif = est_actif
                
                # Mettre à jour l'image si un nouveau fichier est fourni
                if request.FILES.get('image'):
                    # Supprimer l'ancienne image
                    if carousel_image.image:
                        carousel_image.image.delete()
                    carousel_image.image = request.FILES.get('image')
                
                carousel_image.save()
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='update',
                    object_type='CarouselImage',
                    object_id=carousel_image.id,
                    description=f"Image carousel modifiée: {titre}"
                )
                
                messages.success(request, 'Image carousel modifiée avec succès!')
                return redirect('dashboard:carousel_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de la modification: {str(e)}')
        else:
            messages.error(request, 'Le titre est requis.')
    
    context = {
        'carousel_image': carousel_image,
    }
    return render(request, 'dashboard/edit_carousel_image.html', context)


@login_required
def delete_carousel_image(request, image_id):
    """Supprimer une image du carousel"""
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        try:
            titre = carousel_image.titre
            
            # Supprimer le fichier physique
            if carousel_image.image:
                carousel_image.image.delete()
            
            # Supprimer l'objet
            carousel_image.delete()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='delete',
                object_type='CarouselImage',
                object_id=image_id,
                description=f"Image carousel supprimée: {titre}"
            )
            
            messages.success(request, 'Image carousel supprimée avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
    
    return redirect('dashboard:carousel_manager')


@login_required
def toggle_carousel_status(request, image_id):
    """Activer/désactiver une image du carousel"""
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        try:
            carousel_image.est_actif = not carousel_image.est_actif
            carousel_image.save()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='toggle',
                object_type='CarouselImage',
                object_id=carousel_image.id,
                description=f"Image carousel {'activée' if carousel_image.est_actif else 'désactivée'}: {carousel_image.titre}"
            )
            
            messages.success(request, f"Image carousel {'activée' if carousel_image.est_actif else 'désactivée'}!")
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    return redirect('dashboard:carousel_manager')


@login_required
@require_POST
def delete_image(request, image_id):
    """Supprimer une image"""
    try:
        image = StaticImage.objects.get(id=image_id)
        image_name = image.name
        
        # Supprimer le fichier physique
        if image.file:
            image.file.delete()
        
        # Supprimer l'objet
        image.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='StaticImage',
            object_id=image_id,
            description=f"Image supprimée: {image_name}"
        )
        
        return JsonResponse({'success': True})
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})


@login_required
def site_settings(request):
    """Paramètres du site"""
    site_settings, created = SiteSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        site_name = request.POST.get('site_name')
        site_description = request.POST.get('site_description')
        maintenance_mode = request.POST.get('maintenance_mode') == 'on'
        
        # Mettre à jour les paramètres
        site_settings.site_name = site_name
        site_settings.site_description = site_description
        site_settings.maintenance_mode = maintenance_mode
        site_settings.save()
        
        messages.success(request, 'Paramètres du site mis à jour avec succès!')
        return redirect('dashboard:site_settings')
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'dashboard/site_settings.html', context)


@login_required
def content_manager(request):
    """Gestionnaire de contenu"""
    services = Service.objects.all()
    formations = Formation.objects.all()
    
    context = {
        'services': services,
        'formations': formations,
    }
    return render(request, 'dashboard/content_manager.html', context)


@login_required
def activity_log(request):
    """Journal d'activité"""
    activities = DashboardActivity.objects.select_related('user').order_by('-timestamp')
    
    # Filtrage
    action = request.GET.get('action')
    if action:
        activities = activities.filter(action=action)
    
    object_type = request.GET.get('object_type')
    if object_type:
        activities = activities.filter(object_type=object_type)
    
    context = {
        'activities': activities,
        'current_filters': {
            'action': action,
            'object_type': object_type,
        }
    }
    return render(request, 'dashboard/activity_log.html', context)


@login_required
def file_manager(request):
    """Gestionnaire de fichiers"""
    # Récupérer tous les fichiers dans le dossier uploads
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    files = []
    
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'url': os.path.join(settings.MEDIA_URL, 'uploads', filename),
                })
    
    # Trier par date de modification (plus récent en premier)
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    context = {
        'files': files,
    }
    return render(request, 'dashboard/file_manager.html', context)


def get_file_badge_color(filename):
    """Obtenir la couleur du badge selon le type de fichier"""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
        return 'text-success'
    elif ext in ['.pdf']:
        return 'text-danger'
    elif ext in ['.doc', '.docx']:
        return 'text-primary'
    elif ext in ['.xls', '.xlsx']:
        return 'text-success'
    elif ext in ['.zip', '.rar', '.7z']:
        return 'text-warning'
    elif ext in ['.mp3', '.wav', '.flac']:
        return 'text-info'
    elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
        return 'text-danger'
    elif ext in ['.txt', '.md']:
        return 'text-secondary'
    elif ext in ['.html', '.css', '.js', '.py', '.php']:
        return 'text-dark'
    else:
        return 'text-muted'


@login_required
def upload_file(request):
    """Upload de fichiers"""
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        folder_id = request.POST.get('folder')
        
        uploaded_count = 0
        for file in files:
            try:
                # Sauvegarder le fichier
                file_path = default_storage.save(f'uploads/{file.name}', file)
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='upload',
                    object_type='File',
                    object_id=file.name,
                    description=f"Fichier uploadé: {file.name}"
                )
                
                uploaded_count += 1
            except Exception as e:
                messages.error(request, f"Erreur lors de l'upload de {file.name}: {str(e)}")
        
        if uploaded_count > 0:
            messages.success(request, f"{uploaded_count} fichier(s) uploadé(s) avec succès!")
        
        return redirect('dashboard:file_manager')
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def create_folder(request):
    """Créer un nouveau dossier"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folder_name = data.get('folder_name')
            parent_folder = data.get('parent_folder')
            
            if not folder_name:
                return JsonResponse({'success': False, 'error': 'Nom du dossier requis'})
            
            # Créer le dossier
            folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads', folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='create',
                    object_type='Folder',
                    object_id=folder_name,
                    description=f"Dossier créé: {folder_name}"
                )
                
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Le dossier existe déjà'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def delete_file(request):
    """Supprimer un fichier"""
    try:
        data = json.loads(request.body)
        filename = data.get('filename')
        
        if not filename:
            return JsonResponse({'success': False, 'error': 'Nom du fichier requis'})
        
        # Construire le chemin complet
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='delete',
                object_type='File',
                object_id=filename,
                description=f"Fichier supprimé: {filename}"
            )
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Fichier non trouvé'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def sync_image_to_service(request):
    """Synchroniser une image du dashboard vers un service"""
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        service_id = request.POST.get('service_id')
        try:
            dashboard_image = StaticImage.objects.get(id=image_id)
            success, message = sync_dashboard_image_to_service(dashboard_image, service_id)
            if success:
                DashboardActivity.objects.create(
                    user=request.user,
                    action='sync',
                    object_type='Service',
                    object_id=service_id,
                    description=f"Image synchronisée vers le service {service_id}"
                )
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})
        except StaticImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image non trouvée'})


@login_required
def sync_image_to_about(request):
    """Synchroniser une image du dashboard vers la section about"""
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        about_id = request.POST.get('about_id')
        try:
            dashboard_image = StaticImage.objects.get(id=image_id)
            success, message = sync_dashboard_image_to_about(dashboard_image, about_id)
            if success:
                DashboardActivity.objects.create(
                    user=request.user,
                    action='sync',
                    object_type='AboutImage',
                    object_id=about_id,
                    description=f"Image synchronisée vers la section about {about_id}"
                )
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})
        except StaticImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image non trouvée'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def sync_image_to_formation(request):
    """Synchroniser une image du dashboard vers une formation"""
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        formation_id = request.POST.get('formation_id')
        
        # Debug logging
        print(f"DEBUG: sync_image_to_formation called with image_id={image_id}, formation_id={formation_id}")
        
        if not image_id or not formation_id:
            return JsonResponse({'success': False, 'error': 'Image ID et Formation ID sont requis'})
        
        try:
            dashboard_image = StaticImage.objects.get(id=image_id)
            success, message = sync_dashboard_image_to_formation(dashboard_image, formation_id)
            if success:
                DashboardActivity.objects.create(
                    user=request.user,
                    action='sync',
                    object_type='Formation',
                    object_id=formation_id,
                    description=f"Image synchronisée vers la formation {formation_id}"
                )
                print(f"DEBUG: Image synchronisée avec succès pour formation {formation_id}")
                return JsonResponse({'success': True, 'message': message})
            else:
                print(f"DEBUG: Échec de synchronisation: {message}")
                return JsonResponse({'success': False, 'error': message})
        except StaticImage.DoesNotExist:
            print(f"DEBUG: Image non trouvée avec ID {image_id}")
            return JsonResponse({'success': False, 'error': 'Image non trouvée'})
        except Exception as e:
            print(f"DEBUG: Exception lors de la synchronisation: {str(e)}")
            return JsonResponse({'success': False, 'error': f'Exception: {str(e)}'})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def sync_image_to_site_config(request):
    """Synchroniser une image du dashboard vers la configuration du site"""
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        config_type = request.POST.get('config_type')
        try:
            dashboard_image = StaticImage.objects.get(id=image_id)
            success, message = sync_dashboard_image_to_site_config(dashboard_image, config_type)
            if success:
                DashboardActivity.objects.create(
                    user=request.user,
                    action='sync',
                    object_type='SiteConfiguration',
                    object_id=config_type,
                    description=f"Image synchronisée vers la configuration {config_type}"
                )
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})
        except StaticImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image non trouvée'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def sync_image_to_carousel(request):
    """Synchroniser une image du dashboard vers le carousel"""
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        carousel_id = request.POST.get('carousel_id')
        try:
            dashboard_image = StaticImage.objects.get(id=image_id)
            success, message = sync_dashboard_image_to_carousel(dashboard_image, carousel_id)
            if success:
                DashboardActivity.objects.create(
                    user=request.user,
                    action='sync',
                    object_type='CarouselImage',
                    object_id=carousel_id,
                    description=f"Image synchronisée vers le carousel {carousel_id}"
                )
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})
        except StaticImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image non trouvée'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def sync_dashboard(request):
    """Page de synchronisation du dashboard"""
    context = {
        'services': Service.objects.all().order_by('titre'),
        'formations': Formation.objects.all().order_by('titre'),
        'service_images': StaticImage.objects.filter(image_type='service', is_active=True),
        'formation_images': StaticImage.objects.filter(image_type='formation', is_active=True),
        'carousel_images': CarouselImage.objects.filter(est_actif=True).order_by('ordre'),
        'sync_status': get_sync_status(),
        'site_config': SiteConfiguration.objects.filter(active=True).first(),
    }
    return render(request, 'dashboard/sync_dashboard.html', context)


@login_required
def image_overview(request):
    """Vue d'ensemble complète des images du site avec interface CRUD"""
    # Récupérer toutes les images avec leurs relations
    dashboard_images = StaticImage.objects.select_related('uploaded_by').all()
    
    # Récupérer les images des services
    services_with_images = Service.objects.exclude(image='').values('id', 'titre', 'image', 'description')
    
    # Récupérer les images des formations  
    formations_with_images = Formation.objects.exclude(image='').values('id', 'titre', 'image', 'description')
    
    # Récupérer la configuration du site
    site_config = SiteConfiguration.objects.first()
    
    # Filtrage
    image_type = request.GET.get('type')
    if image_type:
        dashboard_images = dashboard_images.filter(image_type=image_type)
    
    status = request.GET.get('status')
    if status:
        dashboard_images = dashboard_images.filter(is_active=(status == 'active'))
    
    search = request.GET.get('search')
    if search:
        dashboard_images = dashboard_images.filter(name__icontains=search)
    
    context = {
        'dashboard_images': dashboard_images.order_by('-created_at'),
        'services_with_images': services_with_images,
        'formations_with_images': formations_with_images,
        'site_config': site_config,
        'image_types': StaticImage.IMAGE_TYPES,
        'current_filters': {
            'type': image_type,
            'status': status,
            'search': search,
        },
        'total_images': dashboard_images.count(),
        'active_images': dashboard_images.filter(is_active=True).count(),
        'inactive_images': dashboard_images.filter(is_active=False).count(),
    }
    return render(request, 'dashboard/image_overview.html', context)


@login_required
@require_POST
def update_image(request, image_id):
    """Mise à jour d'une image avec actualisation automatique du site"""
    try:
        image = StaticImage.objects.get(id=image_id)
        
        # Mise à jour des champs
        name = request.POST.get('name')
        if name:
            image.name = name
        
        image_type = request.POST.get('image_type')
        if image_type:
            image.image_type = image_type
        
        description = request.POST.get('description')
        if description is not None:
            image.description = description
        
        # Gestion du statut
        is_active = request.POST.get('is_active')
        if is_active:
            image.is_active = is_active == 'true'
        
        # Gestion du nouveau fichier
        if request.FILES.get('file'):
            # Supprimer l'ancien fichier
            if image.file:
                image.file.delete()
            image.file = request.FILES.get('file')
        
        image.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='update',
            object_type='StaticImage',
            object_id=image.id,
            description=f"Image mise à jour: {image.name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Image mise à jour avec succès',
            'image': {
                'id': image.id,
                'name': image.name,
                'image_type': image.image_type,
                'is_active': image.is_active,
                'file_url': image.file.url,
                'description': image.description,
            }
        })
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def quick_toggle_image(request, image_id):
    """Activation/désactivation rapide d'une image"""
    try:
        image = StaticImage.objects.get(id=image_id)
        image.is_active = not image.is_active
        image.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='StaticImage',
            object_id=image.id,
            description=f"Image {'activée' if image.is_active else 'désactivée'}: {image.name}"
        )
        
        return JsonResponse({
            'success': True,
            'is_active': image.is_active,
            'message': f"Image {'activée' if image.is_active else 'désactivée'}"
        })
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})


@login_required
@require_POST
def delete_image_overview(request, image_id):
    """Suppression d'une image avec confirmation et logging"""
    try:
        image = StaticImage.objects.get(id=image_id)
        image_name = image.name
        
        # Supprimer le fichier physique
        if image.file:
            image.file.delete()
        
        # Supprimer l'objet
        image.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='StaticImage',
            object_id=image_id,
            description=f"Image supprimée: {image_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Image supprimée avec succès'
        })
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})


@login_required
@require_POST
def toggle_image_overview(request, image_id):
    """Activer/désactiver une image de vue d'ensemble"""
    try:
        image = StaticImage.objects.get(id=image_id)
        image.is_active = not image.is_active
        image.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='StaticImage',
            object_id=image.id,
            description=f"Image {'activée' if image.is_active else 'désactivée'}: {image.name}"
        )
        
        return JsonResponse({
            'success': True,
            'is_active': image.is_active,
            'message': f"Image {'activée' if image.is_active else 'désactivée'}"
        })
        
    except StaticImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Image non trouvée'})


# CRUD pour les services
@login_required
@require_POST
def toggle_service_status(request, service_id):
    """Activer/désactiver un service"""
    try:
        service = Service.objects.get(id=service_id)
        service.est_actif = not service.est_actif
        service.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='Service',
            object_id=service.id,
            description=f"Service {'activé' if service.est_actif else 'désactivé'}: {service.titre}"
        )
        
        return JsonResponse({
            'success': True,
            'is_active': service.est_actif,
            'message': f"Service {'activé' if service.est_actif else 'désactivé'}"
        })
        
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service non trouvé'})


@login_required
@require_POST
def delete_service(request, service_id):
    """Supprimer un service"""
    try:
        service = Service.objects.get(id=service_id)
        service_name = service.titre
        
        # Supprimer l'objet
        service.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='Service',
            object_id=service_id,
            description=f"Service supprimé: {service_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Service supprimé avec succès'
        })
        
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service non trouvé'})


# CRUD pour les formations
@login_required
@require_POST
def toggle_formation_status(request, formation_id):
    """Activer/désactiver une formation"""
    try:
        formation = Formation.objects.get(id=formation_id)
        formation.est_actif = not formation.est_actif
        formation.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='Formation',
            object_id=formation.id,
            description=f"Formation {'activée' if formation.est_actif else 'désactivée'}: {formation.titre}"
        )
        
        return JsonResponse({
            'success': True,
            'is_active': formation.est_actif,
            'message': f"Formation {'activée' if formation.est_actif else 'désactivée'}"
        })
        
    except Formation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Formation non trouvée'})


@login_required
@require_POST
def delete_team_member(request, member_id):
    """Suppression d'un membre d'équipe"""
    try:
        member = TeamMember.objects.get(id=member_id)
        member_name = member.nom
        
        # Supprimer l'objet
        member.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='TeamMember',
            object_id=member_id,
            description=f"Membre d'équipe supprimé: {member_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Membre d\'équipe supprimé avec succès'
        })
        
    except TeamMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Membre non trouvé'})


@login_required
@require_POST
def delete_blog_post(request, post_id):
    """Suppression d'un article de blog"""
    try:
        post = BlogPost.objects.get(id=post_id)
        post_title = post.titre
        
        # Supprimer l'objet
        post.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='BlogPost',
            object_id=post_id,
            description=f"Article de blog supprimé: {post_title}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Article de blog supprimé avec succès'
        })
        
    except BlogPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article non trouvé'})


@login_required
def get_service(request, service_id):
    """Obtenir les données d'un service"""
    try:
        service = Service.objects.get(id=service_id)
        return JsonResponse({
            'success': True,
            'service': {
                'id': service.id,
                'titre': service.titre,
                'description': service.description,
                'description_courte': service.description_courte,
                'categorie': service.categorie,
                'icone': service.icone,
                'est_actif': service.est_actif,
                'ordre': service.ordre,
            }
        })
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service non trouvé'})

@login_required
@require_POST
def edit_service(request, service_id):
    """Modifier un service"""
    try:
        service = Service.objects.get(id=service_id)
        
        # Mettre à jour les champs
        service.titre = request.POST.get('titre')
        service.description = request.POST.get('description')
        service.description_courte = request.POST.get('description_courte')
        service.categorie = request.POST.get('categorie')
        service.icone = request.POST.get('icone')
        service.ordre = int(request.POST.get('ordre', 0))
        service.est_actif = request.POST.get('est_actif') == 'on'
        
        service.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='edit',
            object_type='Service',
            object_id=service.id,
            description=f"Service modifié: {service.titre}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Service modifié avec succès'
        })
        
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service non trouvé'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def add_service(request):
    """Ajouter un service"""
    try:
        service = Service.objects.create(
            titre=request.POST.get('titre'),
            description=request.POST.get('description'),
            description_courte=request.POST.get('description_courte'),
            categorie=request.POST.get('categorie'),
            icone=request.POST.get('icone'),
            ordre=int(request.POST.get('ordre', 0)),
            est_actif=request.POST.get('est_actif') == 'on'
        )
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='add',
            object_type='Service',
            object_id=service.id,
            description=f"Service créé: {service.titre}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Service créé avec succès'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def edit_formation(request, formation_id):
    """Modifier une formation"""
    try:
        formation = Formation.objects.get(id=formation_id)
        
        # Mettre à jour les champs
        formation.titre = request.POST.get('titre')
        formation.description = request.POST.get('description')
        formation.categorie = request.POST.get('categorie')
        formation.niveau = request.POST.get('niveau')
        formation.objectifs = request.POST.get('objectifs')
        formation.programme = request.POST.get('programme')
        formation.duree = request.POST.get('duree')
        formation.prix = float(request.POST.get('prix', 0))
        formation.disponible = request.POST.get('disponible') == 'on'
        
        formation.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='edit',
            object_type='Formation',
            object_id=formation.id,
            description=f"Formation modifiée: {formation.title}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Formation modifiée avec succès'
        })
        
    except Formation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Formation non trouvée'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def add_formation(request):
    """Ajouter une formation"""
    try:
        formation = Formation.objects.create(
            titre=request.POST.get('titre'),
            description=request.POST.get('description'),
            categorie=request.POST.get('categorie'),
            niveau=request.POST.get('niveau'),
            objectifs=request.POST.get('objectifs'),
            programme=request.POST.get('programme'),
            duree=request.POST.get('duree'),
            prix=float(request.POST.get('prix', 0)),
            disponible=request.POST.get('disponible') == 'on'
        )
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='add',
            object_type='Formation',
            object_id=formation.id,
            description=f"Formation créée: {formation.title}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Formation créée avec succès'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_formation(request, formation_id):
    """Obtenir les données d'une formation"""
    try:
        formation = Formation.objects.get(id=formation_id)
        return JsonResponse({
            'success': True,
            'formation': {
                'id': formation.id,
                'titre': formation.titre,
                'description': formation.description,
                'categorie': formation.categorie,
                'niveau': formation.niveau,
                'objectifs': formation.objectifs,
                'programme': formation.programme,
                'duree': formation.duree,
                'prix': float(formation.prix),
                'disponible': formation.disponible,
            }
        })
    except Formation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Formation non trouvée'})

@login_required
@require_POST
def toggle_blog_post_status(request, post_id):
    """Activer/désactiver un article de blog"""
    try:
        post = BlogPost.objects.get(id=post_id)
        post.est_publie = not post.est_publie
        post.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='BlogPost',
            object_id=post.id,
            description=f"Article {'publié' if post.est_publie else 'dépublié'}: {post.titre}"
        )
        
        return JsonResponse({
            'success': True,
            'is_published': post.est_publie,
            'message': f"Article {'publié' if post.est_publie else 'mis en brouillon'}"
        })
        
    except BlogPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Article non trouvé'})


@login_required
@require_POST
def delete_formation(request, formation_id):
    """Supprimer une formation"""
    try:
        formation = Formation.objects.get(id=formation_id)
        formation_name = formation.titre
        
        # Supprimer l'objet
        formation.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='Formation',
            object_id=formation_id,
            description=f"Formation supprimée: {formation_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Formation supprimée avec succès'
        })
        
    except Formation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Formation non trouvée'})


# ===== VUES POUR LES AVIS CLIENTS =====

@login_required
def customer_reviews_manager(request):
    """Gestionnaire des avis clients"""
    from main.models import CustomerReview
    
    reviews = CustomerReview.objects.all()
    context = {
        'reviews': reviews,
        'section': 'customer_reviews'
    }
    return render(request, 'dashboard/customer_reviews_manager.html', context)


@login_required
@require_POST
def add_customer_review(request):
    """Ajouter un avis client"""
    from main.models import CustomerReview
    
    try:
        review = CustomerReview.objects.create(
            nom=request.POST.get('nom'),
            entreprise=request.POST.get('entreprise', ''),
            poste=request.POST.get('poste', ''),
            commentaire=request.POST.get('commentaire'),
            note=int(request.POST.get('note', 5)),
            est_actif=request.POST.get('est_actif') == 'on',
            ordre=int(request.POST.get('ordre', 0))
        )
        
        # Gérer l'upload de photo si présent
        if 'photo' in request.FILES:
            review.photo = request.FILES['photo']
            review.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='create',
            object_type='CustomerReview',
            object_id=review.id,
            description=f"Avis client créé: {review.nom}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Avis client créé avec succès'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def edit_customer_review(request, review_id):
    """Modifier un avis client"""
    from main.models import CustomerReview
    
    try:
        review = CustomerReview.objects.get(id=review_id)
        
        # Mettre à jour les champs
        review.nom = request.POST.get('nom')
        review.entreprise = request.POST.get('entreprise', '')
        review.poste = request.POST.get('poste', '')
        review.commentaire = request.POST.get('commentaire')
        review.note = int(request.POST.get('note', 5))
        review.est_actif = request.POST.get('est_actif') == 'on'
        review.ordre = int(request.POST.get('ordre', 0))
        
        # Gérer l'upload de photo si présent
        if 'photo' in request.FILES:
            # Supprimer l'ancienne photo si elle existe
            if review.photo:
                review.photo.delete(save=False)
            review.photo = request.FILES['photo']
        
        review.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='update',
            object_type='CustomerReview',
            object_id=review.id,
            description=f"Avis client modifié: {review.nom}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Avis client modifié avec succès'
        })
        
    except CustomerReview.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Avis client non trouvé'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def delete_customer_review(request, review_id):
    """Supprimer un avis client"""
    from main.models import CustomerReview
    
    try:
        review = CustomerReview.objects.get(id=review_id)
        review_name = review.nom
        
        # Supprimer la photo si elle existe
        if review.photo:
            review.photo.delete(save=False)
        
        # Supprimer l'objet
        review.delete()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='delete',
            object_type='CustomerReview',
            object_id=review_id,
            description=f"Avis client supprimé: {review_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Avis client supprimé avec succès'
        })
        
    except CustomerReview.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Avis client non trouvé'})


@login_required
@require_POST
def toggle_customer_review_status(request, review_id):
    """Activer/désactiver un avis client"""
    from main.models import CustomerReview
    
    try:
        review = CustomerReview.objects.get(id=review_id)
        review.est_actif = not review.est_actif
        review.save()
        
        # Logger l'activité
        DashboardActivity.objects.create(
            user=request.user,
            action='toggle',
            object_type='CustomerReview',
            object_id=review.id,
            description=f"Avis client {'activé' if review.est_actif else 'désactivé'}: {review.nom}"
        )
        
        return JsonResponse({
            'success': True,
            'is_active': review.est_actif,
            'message': f"Avis client {'activé' if review.est_actif else 'désactivé'}"
        })
        
    except CustomerReview.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Avis client non trouvé'})


@login_required
def get_customer_review(request, review_id):
    """Obtenir les données d'un avis client"""
    from main.models import CustomerReview
    
    try:
        review = CustomerReview.objects.get(id=review_id)
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'nom': review.nom,
                'entreprise': review.entreprise,
                'poste': review.poste,
                'commentaire': review.commentaire,
                'note': review.note,
                'photo_url': review.photo.url if review.photo else None,
                'est_actif': review.est_actif,
                'ordre': review.ordre,
            }
        })
    except CustomerReview.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Avis client non trouvé'})


@login_required
def partner_manager(request):
    """Gestion des partenaires"""
    partners = Partner.objects.all().order_by('ordre', 'nom')
    
    # Statistiques
    total_partners = partners.count()
    active_partners = partners.filter(est_actif=True).count()
    inactive_partners = partners.filter(est_actif=False).count()
    
    context = {
        'partners': partners,
        'total_partners': total_partners,
        'active_partners': active_partners,
        'inactive_partners': inactive_partners,
    }
    return render(request, 'dashboard/partner_manager.html', context)


@login_required
def add_partner(request):
    """Ajouter un nouveau partenaire"""
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                partner = form.save()
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='create',
                    object_type='Partner',
                    object_id=partner.id,
                    description=f"Partenaire créé: {partner.nom}"
                )
                
                messages.success(request, 'Partenaire ajouté avec succès!')
                return redirect('dashboard:partner_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = PartnerForm()
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_partner.html', context)


@login_required
def edit_partner(request, partner_id):
    """Modifier un partenaire"""
    partner = get_object_or_404(Partner, id=partner_id)
    
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            try:
                # Gérer le remplacement du logo
                if request.FILES.get('logo') and partner.logo:
                    partner.logo.delete()
                
                partner = form.save()
                
                # Logger l'activité
                DashboardActivity.objects.create(
                    user=request.user,
                    action='update',
                    object_type='Partner',
                    object_id=partner.id,
                    description=f"Partenaire modifié: {partner.nom}"
                )
                
                messages.success(request, 'Partenaire modifié avec succès!')
                return redirect('dashboard:partner_manager')
            except Exception as e:
                messages.error(request, f'Erreur lors de la modification: {str(e)}')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = PartnerForm(instance=partner)
    
    context = {
        'form': form,
        'partner': partner,
    }
    return render(request, 'dashboard/edit_partner.html', context)


@login_required
def delete_partner(request, partner_id):
    """Supprimer un partenaire"""
    partner = get_object_or_404(Partner, id=partner_id)
    
    if request.method == 'POST':
        try:
            nom = partner.nom
            
            # Supprimer le fichier logo
            if partner.logo:
                partner.logo.delete()
            
            # Supprimer l'objet
            partner.delete()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='delete',
                object_type='Partner',
                object_id=partner_id,
                description=f"Partenaire supprimé: {nom}"
            )
            
            messages.success(request, 'Partenaire supprimé avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
    
    return redirect('dashboard:partner_manager')


@login_required
def toggle_partner_status(request, partner_id):
    """Activer/désactiver un partenaire"""
    partner = get_object_or_404(Partner, id=partner_id)
    
    if request.method == 'POST':
        try:
            partner.est_actif = not partner.est_actif
            partner.save()
            
            # Logger l'activité
            DashboardActivity.objects.create(
                user=request.user,
                action='toggle',
                object_type='Partner',
                object_id=partner.id,
                description=f"Partenaire {'activé' if partner.est_actif else 'désactivé'}: {partner.nom}"
            )
            
            messages.success(request, f"Partenaire {'activé' if partner.est_actif else 'désactivé'}!")
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    return redirect('dashboard:partner_manager')
# --- Gestion du Recrutement ---

@login_required
def recruitment_manager(request):
    """Tableau de bord pour la gestion du recrutement"""
    offres = OffreEmploi.objects.all().order_by('-date_creation')
    candidatures = Candidature.objects.all().order_by('-date_candidature')
    candidatures_spontanees = CandidatureSpontanee.objects.all().order_by('-date_candidature')
    
    context = {
        'job_offers': offres,
        'applications': candidatures,
        'spontaneous_applications': candidatures_spontanees,
        'total_offers': offres.count(),
        'total_applications': candidatures.count() + candidatures_spontanees.count(),
        'new_applications': (
            candidatures.filter(statut='nouvelle').count() + 
            candidatures_spontanees.filter(statut='nouvelle').count()
        )
    }
    return render(request, 'dashboard/recruitment_manager.html', context)


@login_required
def add_job_offer(request):
    """Ajouter une offre d'emploi"""
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST, request.FILES)
        if form.is_valid():
            offre = form.save()
            DashboardActivity.objects.create(
                user=request.user,
                action='add',
                object_type='OffreEmploi',
                object_id=offre.id,
                description=f"Nouvelle offre d'emploi : {offre.titre}"
            )
            messages.success(request, "L'offre d'emploi a été créée avec succès.")
            return redirect('dashboard:recruitment_manager')
    else:
        form = OffreEmploiForm()
        
    return render(request, 'dashboard/job_offer_form.html', {'form': form, 'title': "Ajouter une offre"})


@login_required
def edit_job_offer(request, pk):
    """Modifier une offre d'emploi"""
    offre = get_object_or_404(OffreEmploi, pk=pk)
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST, request.FILES, instance=offre)
        if form.is_valid():
            form.save()
            DashboardActivity.objects.create(
                user=request.user,
                action='edit',
                object_type='OffreEmploi',
                object_id=offre.id,
                description=f"Offre d'emploi modifiée : {offre.titre}"
            )
            messages.success(request, "L'offre a été mise à jour.")
            return redirect('dashboard:recruitment_manager')
    else:
        form = OffreEmploiForm(instance=offre)
        
    return render(request, 'dashboard/job_offer_form.html', {'form': form, 'title': "Modifier l'offre", 'offre': offre})


@login_required
@require_POST
def delete_job_offer(request, pk):
    """Supprimer une offre d'emploi"""
    offre = get_object_or_404(OffreEmploi, pk=pk)
    titre = offre.titre
    offre.delete()
    DashboardActivity.objects.create(
        user=request.user,
        action='delete',
        object_type='OffreEmploi',
        object_id=pk,
        description=f"Offre d'emploi supprimée : {titre}"
    )
    return JsonResponse({'success': True})


@login_required
@require_POST
def toggle_job_offer_status(request, pk):
    """Activer/désactiver une offre"""
    offre = get_object_or_404(OffreEmploi, pk=pk)
    offre.est_actif = not offre.est_actif
    offre.save()
    DashboardActivity.objects.create(
        user=request.user,
        action='toggle',
        object_type='OffreEmploi',
        object_id=offre.id,
        description=f"Statut offre '{offre.titre}' changé : {'Active' if offre.est_actif else 'Inactive'}"
    )
    return JsonResponse({'success': True, 'is_active': offre.est_actif})


@login_required
def view_application(request, pk, type='normal'):
    """Voir le détail d'une candidature"""
    if type == 'spontaneous':
        application = get_object_or_404(CandidatureSpontanee, pk=pk)
    else:
        application = get_object_or_404(Candidature, pk=pk)
        
    return render(request, 'dashboard/application_detail.html', {
        'application': application,
        'type': type
    })


@login_required
@require_POST
def update_application_status(request, pk):
    """Mettre à jour le statut d'une candidature"""
    type = request.POST.get('type', 'normal')
    new_status = request.POST.get('status')
    notes = request.POST.get('notes', '')
    
    if type == 'spontaneous':
        application = get_object_or_404(CandidatureSpontanee, pk=pk)
    else:
        application = get_object_or_404(Candidature, pk=pk)
        
    application.statut = new_status
    application.notes_admin = notes
    application.save()
    
    DashboardActivity.objects.create(
        user=request.user,
        action='edit',
        object_type='Candidature' if type == 'normal' else 'CandidatureSpontanee',
        object_id=application.id,
        description=f"Statut candidature de {application.prenom} {application.nom} mis à jour : {new_status}"
    )
    
    messages.success(request, "La candidature a été mise à jour.")
    return redirect('dashboard:view_application', pk=pk, type=type)


@login_required
@require_POST
def delete_application(request, pk):
    """Supprimer une candidature"""
    type = request.POST.get('type', 'normal')
    if type == 'spontaneous':
        application = get_object_or_404(CandidatureSpontanee, pk=pk)
    else:
        application = get_object_or_404(Candidature, pk=pk)
    
    nom = f"{application.prenom} {application.nom}"
    application.delete()
    
    DashboardActivity.objects.create(
        user=request.user,
        action='delete',
        object_type='Candidature' if type == 'normal' else 'CandidatureSpontanee',
        object_id=pk,
        description=f"Candidature de {nom} supprimée"
    )
    
    return JsonResponse({'success': True})

@login_required
def request_manager(request):
    """Vue pour gérer toutes les demandes (Services, Formations, Contact)"""
    from main.models import Contact
    
    demandes = Contact.objects.all().order_by('-date_creation')
    
    # Filtrage par statut
    statut = request.GET.get('statut')
    if statut == 'traite':
        demandes = demandes.filter(traite=True)
    elif statut == 'non_traite':
        demandes = demandes.filter(traite=False)
        
    # Filtrage par type
    type_demande = request.GET.get('type')
    if type_demande == 'service':
        demandes = demandes.filter(service_interesse__isnull=False)
    elif type_demande == 'formation':
        demandes = demandes.filter(formation_interessee__isnull=False)
    elif type_demande == 'contact':
        demandes = demandes.filter(service_interesse__isnull=True, formation_interessee__isnull=True)
    
    # Pagination
    paginator = Paginator(demandes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_statut': statut,
        'current_type': type_demande,
    }
    return render(request, 'dashboard/request_manager.html', context)

@login_required
def request_detail(request, pk):
    """Détail d'une demande avec possibilité de changer le statut"""
    from main.models import Contact
    
    demande = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_status':
            demande.traite = not demande.traite
            demande.save()
            status_msg = "traitée" if demande.traite else "non traitée"
            messages.success(request, f"La demande a été marquée comme {status_msg}.")
            return redirect('dashboard:request_detail', pk=pk)
            
    context = {
        'demande': demande,
    }
    return render(request, 'dashboard/request_detail.html', context)
