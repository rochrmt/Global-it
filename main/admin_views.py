from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from main.models import Service, Formation, Contact, Partner
import datetime
import psutil
import os

@staff_member_required
def admin_dashboard(request):
    """Tableau de bord administrateur avec statistiques"""
    
    # Statistiques des modèles
    stats = {
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(est_actif=True).count(),
        'total_formations': Formation.objects.count(),
        'available_formations': Formation.objects.filter(disponible=True).count(),
        'total_contacts': Contact.objects.count(),
        'unread_contacts': Contact.objects.filter(est_traite=False).count(),
        'total_candidatures': Candidature.objects.count(),
        'active_candidatures': Candidature.objects.filter(est_actif=True).count(),
        'nouvelles_candidatures': Candidature.objects.filter(statut='nouvelle').count(),
        'candidatures_en_cours': Candidature.objects.filter(statut='en_cours').count(),
        'candidatures_traitees': Candidature.objects.filter(statut='traitee').count(),
    }
    
    # Contacts récents
    recent_contacts = Contact.objects.order_by('-date_creation')[:10]
    
    # Candidatures récentes
    recent_candidatures = Candidature.objects.order_by('-date_creation')[:10]
    
    # Services par catégorie
    services_by_category = {}
    for category, label in Service.CATEGORIE_CHOICES:
        count = Service.objects.filter(categorie=category).count()
        services_by_category[label] = count
    
    # Formations par niveau
    formations_by_level = {}
    for level, label in Formation.NIVEAU_CHOICES:
        count = Formation.objects.filter(niveau=level).count()
        formations_by_level[label] = count
    
    context = {
        'stats': stats,
        'recent_contacts': recent_contacts,
        'recent_candidatures': recent_candidatures,
        'services_by_category': services_by_category,
        'formations_by_level': formations_by_level,
        'server_time': datetime.datetime.now(),
    }
    
    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def system_info(request):
    """Informations système et performance"""
    
    try:
        # Informations système
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Uptime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        
        # Processus Django
        django_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if 'python' in proc.info['name'].lower() and 'manage.py' in ' '.join(proc.cmdline()):
                django_processes.append(proc.info)
        
        context = {
            'cpu_percent': cpu_percent,
            'memory_total': memory.total // (1024**3),  # GB
            'memory_used': memory.used // (1024**3),    # GB
            'memory_percent': memory.percent,
            'disk_total': disk.total // (1024**3),      # GB
            'disk_used': disk.used // (1024**3),        # GB
            'disk_percent': disk.percent,
            'uptime': str(uptime).split('.')[0],        # Remove microseconds
            'django_processes': django_processes,
            'server_time': datetime.datetime.now(),
        }
        
    except Exception as e:
        messages.error(request, f"Erreur lors de la récupération des informations système : {e}")
        context = {
            'error': True,
            'server_time': datetime.datetime.now(),
        }
    
    return render(request, 'admin/system_info.html', context)

@staff_member_required
def contact_management(request):
    """Gestion des contacts"""
    
    # Filtrer les contacts
    filter_status = request.GET.get('status', 'all')
    if filter_status == 'unread':
        contacts = Contact.objects.filter(est_traite=False)
    elif filter_status == 'read':
        contacts = Contact.objects.filter(est_traite=True)
    else:
        contacts = Contact.objects.all()
    
    # Trier par date
    contacts = contacts.order_by('-date_creation')
    
    # Marquer comme lus
    if request.method == 'POST':
        contact_ids = request.POST.getlist('contact_ids')
        if contact_ids:
            Contact.objects.filter(id__in=contact_ids).update(est_traite=True)
            messages.success(request, f"{len(contact_ids)} contact(s) marqué(s) comme traité(s)")
    
    context = {
        'contacts': contacts,
        'filter_status': filter_status,
        'total_contacts': Contact.objects.count(),
        'unread_count': Contact.objects.filter(est_traite=False).count(),
    }
    
    return render(request, 'admin/contact_management.html', context)

@staff_member_required
def quick_actions(request):
    """Actions rapides admin"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'backup':
            # Créer une sauvegarde
            from django.core.management import call_command
            from django.http import FileResponse
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
                call_command('dumpdata', stdout=f)
                f.flush()
                
                response = FileResponse(
                    open(f.name, 'rb'),
                    as_attachment=True,
                    filename=f'globaltit_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                )
                
                # Nettoyer le fichier temporaire après l'envoi
                def cleanup(temp_file):
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                
                response['X-Temp-File'] = f.name
                return response
        
        elif action == 'clear_cache':
            # Vider le cache (si configuré)
            from django.core.cache import cache
            cache.clear()
            messages.success(request, "Cache vidé avec succès")
        
        elif action == 'mark_all_contacts_read':
            # Marquer tous les contacts comme lus
            count = Contact.objects.filter(est_traite=False).update(est_traite=True)
            messages.success(request, f"{count} contact(s) marqué(s) comme traité(s)")
    
    return render(request, 'admin/quick_actions.html')

@staff_member_required
def partner_management(request):
    """Gestion des partenaires"""
    partners = Partner.objects.all().order_by('ordre', 'nom')
    
    context = {
        'partners': partners,
        'total_partners': partners.count(),
        'active_partners': partners.filter(est_actif=True).count(),
    }
    return render(request, 'admin/partner_management.html', context)

@staff_member_required
def partner_create(request):
    """Créer un nouveau partenaire"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        site_web = request.POST.get('site_web')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        est_actif = request.POST.get('est_actif') == 'on'
        logo = request.FILES.get('logo')
        
        if nom and site_web and logo:
            partner = Partner.objects.create(
                nom=nom,
                site_web=site_web,
                description=description,
                ordre=ordre,
                est_actif=est_actif,
                logo=logo
            )
            messages.success(request, f'Partenaire "{nom}" créé avec succès.')
            return redirect('partner_management')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
    
    return render(request, 'admin/partner_create.html')

@staff_member_required
def partner_edit(request, pk):
    """Modifier un partenaire"""
    partner = get_object_or_404(Partner, pk=pk)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        site_web = request.POST.get('site_web')
        description = request.POST.get('description', '')
        ordre = request.POST.get('ordre', 0)
        est_actif = request.POST.get('est_actif') == 'on'
        logo = request.FILES.get('logo')
        
        if nom and site_web:
            partner.nom = nom
            partner.site_web = site_web
            partner.description = description
            partner.ordre = ordre
            partner.est_actif = est_actif
            
            if logo:
                partner.logo = logo
            
            partner.save()
            messages.success(request, f'Partenaire "{nom}" modifié avec succès.')
            return redirect('partner_management')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
    
    context = {
        'partner': partner,
    }
    return render(request, 'admin/partner_edit.html', context)

@staff_member_required
def partner_delete(request, pk):
    """Supprimer un partenaire"""
    partner = get_object_or_404(Partner, pk=pk)
    
    if request.method == 'POST':
        nom = partner.nom
        partner.delete()
        messages.success(request, f'Partenaire "{nom}" supprimé avec succès.')
        return redirect('partner_management')
    
    context = {
        'partner': partner,
    }
    return render(request, 'admin/partner_delete.html', context)

