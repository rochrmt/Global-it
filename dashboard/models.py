from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class StaticImage(models.Model):
    """Modèle pour gérer les images statiques"""
    IMAGE_TYPES = [
        ('carousel', 'Carousel'),
        ('service', 'Service'),
        ('formation', 'Formation'),
        ('about', 'À propos'),
        ('contact', 'Contact'),
        ('other', 'Autre'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom de l'image")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='other', verbose_name="Type d'image")
    file = models.ImageField(upload_to='dashboard/static_images/', verbose_name="Fichier")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    position = models.PositiveIntegerField(default=0, verbose_name="Position")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Uploadé par")

    class Meta:
        verbose_name = "Image statique"
        verbose_name_plural = "Images statiques"
        ordering = ['position', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name and self.file:
            self.name = os.path.splitext(os.path.basename(self.file.name))[0]
        super().save(*args, **kwargs)


class DashboardActivity(models.Model):
    """Modèle pour tracer les activités du dashboard"""
    ACTION_TYPES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('upload', 'Upload'),
        ('activate', 'Activation'),
        ('deactivate', 'Désactivation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    action = models.CharField(max_length=20, choices=ACTION_TYPES, verbose_name="Action")
    object_type = models.CharField(max_length=50, verbose_name="Type d'objet")
    object_id = models.CharField(max_length=100, blank=True, verbose_name="ID de l'objet")
    description = models.TextField(blank=True, verbose_name="Description")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")

    class Meta:
        verbose_name = "Activité du dashboard"
        verbose_name_plural = "Activités du dashboard"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.object_type}"


class SiteSettings(models.Model):
    """Modèle pour les paramètres globaux du site"""
    site_name = models.CharField(max_length=100, default="GlobalTit", verbose_name="Nom du site")
    site_description = models.TextField(blank=True, verbose_name="Description du site")
    logo = models.ImageField(upload_to='dashboard/site/', blank=True, null=True, verbose_name="Logo")
    favicon = models.ImageField(upload_to='dashboard/site/', blank=True, null=True, verbose_name="Favicon")
    contact_email = models.EmailField(blank=True, verbose_name="Email de contact")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone de contact")
    contact_address = models.TextField(blank=True, verbose_name="Adresse")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    maintenance_mode = models.BooleanField(default=False, verbose_name="Mode maintenance")
    analytics_code = models.TextField(blank=True, verbose_name="Code Google Analytics")
    custom_css = models.TextField(blank=True, verbose_name="CSS personnalisé")
    custom_js = models.TextField(blank=True, verbose_name="JavaScript personnalisé")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Modifié par")

    class Meta:
        verbose_name = "Paramètre du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule instance
        if not self.pk and SiteSettings.objects.exists():
            raise Exception("Il ne peut y avoir qu'une seule instance de SiteSettings")
        super().save(*args, **kwargs)


class ImageCategory(models.Model):
    """Catégories pour organiser les images"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Catégorie parente")
    
    class Meta:
        verbose_name = "Catégorie d'image"
        verbose_name_plural = "Catégories d'images"
        ordering = ['name']

    def __str__(self):
        return self.name