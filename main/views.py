from django.shortcuts import render, redirect, get_object_or_404
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
            
            messages.success(request, 'Votre message a été envoyé avec succès ! Nous vous répondrons rapidement.')
            return redirect('contact')
    else:
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