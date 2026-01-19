from django.db import models
from django.core.validators import FileExtensionValidator

class SiteConfiguration(models.Model):
    """Configuration globale du site"""
    
    # Hero Section
    hero_titre = models.CharField(max_length=200, default="Transformez votre entreprise avec nos solutions IT")
    hero_sous_titre = models.TextField(max_length=500, default="GLOBALT-IT vous accompagne dans votre transformation digitale")
    hero_image = models.ImageField(upload_to='config/', blank=True, null=True, 
                                 validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    
    # Section À propos
    about_titre = models.CharField(max_length=200, default="Notre mission")
    about_description = models.TextField(max_length=1000, 
                                       default="Chez GLOBALT-IT, nous croyons que la technologie est un levier puissant pour transformer les entreprises.")
    about_image = models.ImageField(upload_to='config/', blank=True, null=True,
                                  validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    
    # Contact
    telephone = models.CharField(max_length=20, default="+33 1 23 45 67 89")
    email = models.EmailField(default="contact@globalt-it.fr")
    adresse = models.TextField(default="123 Rue de l'Innovation\n75000 Paris\nFrance")
    
    # Réseaux sociaux
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, default="GLOBALT-IT - Services Informatiques & Formations")
    meta_description = models.TextField(max_length=160, 
                                       default="GLOBALT-IT : Services informatiques sur-mesure et formations professionnelles pour transformer votre entreprise.")
    
    # Configuration active
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"
    
    def __str__(self):
        return "Configuration du site"
    
    def save(self, *args, **kwargs):
        # S'assure qu'il n'y a qu'une seule configuration active
        if self.active:
            SiteConfiguration.objects.exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Récupère la configuration active"""
        try:
            return cls.objects.get(active=True)
        except cls.DoesNotExist:
            return cls.objects.create()