from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Service, Formation, Contact, CarouselImage, AboutImage, CustomerReview, Partner
from .forms import QuickContactForm, ContactForm


def home(request):
    services = Service.objects.filter(est_actif=True)[:6]
    formations = Formation.objects.filter(disponible=True)[:3]
    carousel_images = CarouselImage.objects.filter(est_actif=True).order_by('ordre')
    
    if request.method == 'POST':
        quick_form = QuickContactForm(request.POST)
        if quick_form.is_valid():
            contact = Contact.objects.create(
                nom=quick_form.cleaned_data['nom'],
                email=quick_form.cleaned_data['email'],
                telephone=quick_form.cleaned_data['telephone'],
                sujet=f"Demande rapide: {quick_form.cleaned_data['besoin']}",
                message=f"Demande rapide reçue via le formulaire de contact rapide.\n\nBesoin: {quick_form.cleaned_data['besoin']}"
            )
            
            # Envoyer un email
            try:
                send_mail(
                    f'Nouvelle demande rapide - {contact.nom}',
                    f'Nom: {contact.nom}\nEmail: {contact.email}\nTéléphone: {contact.telephone}\n\nBesoin: {quick_form.cleaned_data["besoin"]}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Votre demande a été envoyée avec succès ! Nous vous contacterons rapidement.')
            return redirect('home')
    else:
        quick_form = QuickContactForm()
    
    context = {
        'services': services,
        'formations': formations,
        'carousel_images': carousel_images,
        'quick_form': quick_form,
    }
    return render(request, 'main/home.html', context)


def services(request):
    services = Service.objects.filter(est_actif=True)
    context = {
        'services': services,
    }
    return render(request, 'main/services.html', context)


def service_detail(request, pk):
    service = Service.objects.get(pk=pk, est_actif=True)
    autres_services = Service.objects.filter(est_actif=True).exclude(pk=pk)[:3]
    
    context = {
        'service': service,
        'autres_services': autres_services,
    }
    return render(request, 'main/service_detail.html', context)


def formations(request):
    formations = Formation.objects.filter(disponible=True)
    
    # Filtrage par catégorie
    categorie = request.GET.get('categorie')
    if categorie:
        formations = formations.filter(categorie=categorie)
    
    # Filtrage par niveau
    niveau = request.GET.get('niveau')
    if niveau:
        formations = formations.filter(niveau=niveau)
    
    context = {
        'formations': formations,
    }
    return render(request, 'main/formations.html', context)


def formation_detail(request, pk):
    formation = Formation.objects.get(pk=pk, disponible=True)
    autres_formations = Formation.objects.filter(disponible=True).exclude(pk=pk)[:3]
    
    context = {
        'formation': formation,
        'autres_formations': autres_formations,
    }
    return render(request, 'main/formation_detail.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Envoyer un email
            try:
                send_mail(
                    f'Nouveau contact - {contact.nom}',
                    f'Nom: {contact.nom}\nEmail: {contact.email}\nTéléphone: {contact.telephone}\n\nSujet: {contact.sujet}\n\nMessage:\n{contact.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            # Si c'est une requête AJAX, retourner JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Votre message a été envoyé avec succès ! Nous vous répondrons rapidement.'
                })
            
            messages.success(request, 'Votre message a été envoyé avec succès ! Nous vous répondrons rapidement.')
            return redirect('contact')
    else:
        # Si c'est une requête AJAX POST avec erreurs, retourner les erreurs en JSON
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_json()
            }, status=400)
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/contact.html', context)


def about(request):
    services = Service.objects.filter(est_actif=True)[:6]
    about_images = AboutImage.objects.filter(est_actif=True).order_by('ordre')
    customer_reviews = CustomerReview.objects.filter(est_actif=True).order_by('-ordre', '-date_creation')[:6]
    context = {
        'services': services,
        'about_images': about_images,
        'customer_reviews': customer_reviews,
    }
    return render(request, 'main/about.html', context)


def partners(request):
    partners = Partner.objects.filter(est_actif=True).order_by('ordre', 'nom')
    context = {
        'partners': partners,
    }
    return render(request, 'main/partners.html', context)


def job_offers(request):
    """Page des offres d'emploi avec candidatures spontanées"""
    from .models import OffreEmploi
    from .forms import CandidatureSpontaneeForm
    
    # Récupérer les offres actives
    offres = OffreEmploi.objects.filter(est_actif=True).order_by('-urgent', '-date_creation')
    
    # Filtrage par type de contrat
    type_contrat = request.GET.get('type_contrat')
    if type_contrat:
        offres = offres.filter(type_contrat=type_contrat)
    
    # Traiter le formulaire de candidature spontanée
    spontaneous_form = CandidatureSpontaneeForm()
    if request.method == 'POST' and 'spontaneous_submit' in request.POST:
        spontaneous_form = CandidatureSpontaneeForm(request.POST, request.FILES)
        if spontaneous_form.is_valid():
            candidature = spontaneous_form.save()
            msg = 'Votre candidature spontanée a été envoyée avec succès ! Nous vous contacterons bientôt.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
            messages.success(request, msg)
            return redirect('job_offers')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': spontaneous_form.errors.as_json()}, status=400)
    
    context = {
        'job_offers': offres,
        'spontaneous_form': spontaneous_form,
        'type_contrat_choices': OffreEmploi.TYPE_CONTRAT_CHOICES,
    }
    return render(request, 'main/job_offers.html', context)


def job_offer_detail(request, pk):
    """Page de détail d'une offre d'emploi + formulaire de candidature"""
    from .models import OffreEmploi
    from .forms import CandidatureForm
    
    offre = get_object_or_404(OffreEmploi, pk=pk, est_actif=True)
    
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre_emploi = offre
            candidature.save()
            msg = 'Votre candidature a été envoyée avec succès ! Nous examinerons votre profil attentivement.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
            messages.success(request, msg)
            return redirect('job_offer_detail', pk=pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = CandidatureForm()
    
    # Autres offres similaires
    autres_offres = OffreEmploi.objects.filter(
        est_actif=True,
        type_contrat=offre.type_contrat
    ).exclude(pk=pk)[:3]
    
    context = {
        'job_offer': offre,
        'form': form,
        'autres_offres': autres_offres,
    }
    return render(request, 'main/job_offer_detail.html', context)



def submit_service_request(request):
    """Traitement AJAX de la demande de devis service"""
    from .forms import ContactForm
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send email (omitted for brevity, covered by save signal or general logic)
             # Envoyer un email
            try:
                send_mail(
                    f'Nouvelle demande de devis - {contact.nom}',
                    f'Nom: {contact.nom}\nEmail: {contact.email}\nTéléphone: {contact.telephone}\nService: {contact.service_interesse.titre}\n\nSujet: {contact.sujet}\n\nMessage:\n{contact.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            return JsonResponse({'success': True, 'message': 'Votre demande de devis a été envoyée avec succès.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def submit_quick_request(request):
    """Traitement AJAX du formulaire de devis rapide"""
    from .forms import QuickContactForm
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = QuickContactForm(request.POST)
        if form.is_valid():
            contact = Contact.objects.create(
                nom=form.cleaned_data['nom'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data['telephone'],
                sujet=f"Demande rapide: {form.cleaned_data['besoin']}",
                message=f"Demande rapide reçue via le formulaire de contact rapide.\n\nBesoin: {form.cleaned_data['besoin']}"
            )
            
            # Envoyer un email
            try:
                send_mail(
                    f'Nouvelle demande rapide - {contact.nom}',
                    f'Nom: {contact.nom}\nEmail: {contact.email}\nTéléphone: {contact.telephone}\n\nBesoin: {form.cleaned_data["besoin"]}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            return JsonResponse({'success': True, 'message': 'Votre demande a été envoyée avec succès ! Nous vous contacterons rapidement.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def submit_formation_request(request):
    """Traitement AJAX de la demande de formation"""
    from .forms import ContactForm
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
             # Envoyer un email
            try:
                send_mail(
                    f'Nouvelle demande de formation - {contact.nom}',
                    f'Nom: {contact.nom}\nEmail: {contact.email}\nTéléphone: {contact.telephone}\nFormation: {contact.formation_interessee.titre}\n\nSujet: {contact.sujet}\n\nMessage:\n{contact.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            return JsonResponse({'success': True, 'message': 'Votre inscription a été envoyée avec succès.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
