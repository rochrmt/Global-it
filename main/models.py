from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Service(models.Model):
    CATEGORIE_CHOICES = [
        ('developpement', 'Développement'),
        ('infrastructure', 'Infrastructure IT'),
        ('securite', 'Sécurité'),
        ('consulting', 'Consulting'),
        ('support', 'Support Technique'),
    ]
    
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='developpement')
    description = models.TextField()
    description_courte = models.CharField(max_length=200)
    icone = models.CharField(max_length=50, help_text="Classe Font Awesome (ex: fa-code)")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'titre']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.titre


class Formation(models.Model):
    CATEGORIE_CHOICES = [
        ('programmation', 'Programmation'),
        ('reseaux', 'Réseaux'),
        ('securite', 'Sécurité'),
        ('cloud', 'Cloud Computing'),
        ('data', 'Data Science'),
        ('autre', 'Autre'),
    ]
    
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
    ]
    
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='programmation')
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='debutant')
    description = models.TextField()
    objectifs = models.TextField()
    programme = models.TextField()
    duree = models.CharField(max_length=100, help_text="Durée de la formation (ex: 3 jours, 24h)")
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categorie', 'titre']
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
    
    def __str__(self):
        return f"{self.titre} ({self.categorie})"


class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    service_interesse = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    formation_interessee = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"


class SiteConfiguration(models.Model):
    """Configuration globale du site"""
    
    # Informations générales
    nom_site = models.CharField(max_length=100, default="GLOBALT-IT")
    logo = models.ImageField(upload_to='config/', blank=True, null=True,
                           validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])])
    
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
        return self.nom


class JobOffer(models.Model):
    """Offres d'emploi"""
    
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('STAGE', 'Stage'),
        ('ALTERNANCE', 'Alternance'),
        ('FREELANCE', 'Freelance'),
        ('INTERIM', 'Intérim'),
    ]
    
    titre = models.CharField(max_length=200, help_text="Titre du poste")
    description = models.TextField(help_text="Description détaillée du poste")
    missions = models.TextField(help_text="Principales missions du poste")
    profil_recherche = models.TextField(help_text="Profil et compétences recherchées")
    avantages = models.TextField(blank=True, help_text="Avantages proposés")
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES, default='CDI')
    lieu = models.CharField(max_length=100, help_text="Lieu de travail")
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Salaire minimum")
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Salaire maximum")
    experience_min = models.CharField(max_length=50, blank=True, help_text="Expérience minimum requise")
    date_debut = models.DateField(null=True, blank=True, help_text="Date de début souhaitée")
    date_limite = models.DateField(null=True, blank=True, help_text="Date limite de candidature")
    est_actif = models.BooleanField(default=True, help_text="Publier cette offre")
    urgent = models.BooleanField(default=False, help_text="Marquer cette offre comme urgente")
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-urgent', '-date_creation']
        verbose_name = 'Offre d\'emploi'
        verbose_name_plural = 'Offres d\'emploi'
    
    def __str__(self):
        return f"{self.titre} - {self.type_contrat}"
    
    @property
    def is_expired(self):
        """Vérifie si l'offre est expirée"""
        if self.date_limite:
            return timezone.now().date() > self.date_limite
        return False


class JobApplication(models.Model):
    """Candidatures aux offres d'emploi"""
    
    STATUT_CHOICES = [
        ('NOUVELLE', 'Nouvelle'),
        ('EN_COURS', 'En cours de traitement'),
        ('ENTRETIEN', 'Entretien programmé'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
        ('ARCHIVEE', 'Archivée'),
    ]
    
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='applications')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    experience = models.TextField(help_text="Expérience professionnelle")
    formations = models.TextField(blank=True, help_text="Formations et diplômes")
    competences = models.TextField(blank=True, help_text="Compétences techniques")
    motivations = models.TextField(help_text="Lettre de motivation")
    salaire_attendu = models.CharField(max_length=50, blank=True, help_text="Prétentions salariales")
    disponibilite = models.CharField(max_length=100, blank=True, help_text="Disponibilité")
    cv = models.FileField(upload_to='candidatures/cv/', 
                         validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
                         help_text="Formats acceptés : PDF, DOC, DOCX")
    lettre_motivation = models.FileField(upload_to='candidatures/lm/', 
                                        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
                                        blank=True, null=True,
                                        help_text="Lettre de motivation (optionnelle)")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='NOUVELLE')
    notes = models.TextField(blank=True, help_text="Notes internes")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.job_offer.titre}"
    
    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"


class CarouselImage(models.Model):
    """Images du carousel de la page d'accueil"""
    
    titre = models.CharField(max_length=100, help_text="Titre de l'image")
    description = models.CharField(max_length=200, blank=True, help_text="Description optionnelle")
    image = models.ImageField(upload_to='carousel/', 
                            validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage dans le carousel")
    est_actif = models.BooleanField(default=True, help_text="Afficher cette image dans le carousel")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'titre']
        verbose_name = 'Image Carousel'
        verbose_name_plural = 'Images Carousel'
    
    def __str__(self):
        return f"{self.titre} (ordre: {self.ordre})"


class AboutImage(models.Model):
    """Images de la section À propos"""
    
    titre = models.CharField(max_length=100, help_text="Titre de l'image")
    description = models.CharField(max_length=200, blank=True, help_text="Description optionnelle")
    image = models.ImageField(upload_to='about/', 
                            validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage dans la section about")
    est_actif = models.BooleanField(default=True, help_text="Afficher cette image dans la section about")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'titre']
        verbose_name = 'Image About'
        verbose_name_plural = 'Images About'
    
    def __str__(self):
        return f"{self.titre} (ordre: {self.ordre})"


class CustomerReview(models.Model):
    """Avis clients pour la section À propos"""
    
    NOTE_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]
    
    nom = models.CharField(max_length=100, help_text="Nom du client")
    entreprise = models.CharField(max_length=100, blank=True, help_text="Entreprise du client (optionnel)")
    poste = models.CharField(max_length=100, blank=True, help_text="Poste/fonction du client (optionnel)")
    commentaire = models.TextField(help_text="Commentaire de l'avis")
    note = models.IntegerField(choices=NOTE_CHOICES, default=5, help_text="Note sur 5 étoiles")
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True, 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
                             help_text="Photo du client (optionnel)")
    est_actif = models.BooleanField(default=True, help_text="Afficher cet avis sur le site")
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage des avis")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', '-date_creation']
        verbose_name = 'Avis client'
        verbose_name_plural = 'Avis clients'
    
    def __str__(self):
        return f"{self.nom} - {self.note} étoiles"
    
    def get_note_display(self):
        """Retourne l'affichage des étoiles"""
        return '★' * self.note + '☆' * (5 - self.note)


class Partner(models.Model):
    """Partenaires de l'entreprise"""
    
    nom = models.CharField(max_length=100, help_text="Nom du partenaire")
    site_web = models.URLField(help_text="URL du site web du partenaire")
    logo = models.ImageField(upload_to='partners/', 
                           validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])],
                           help_text="Logo du partenaire")
    description = models.TextField(blank=True, help_text="Description optionnelle du partenaire")
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    est_actif = models.BooleanField(default=True, help_text="Afficher ce partenaire sur le site")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'
    
    def __str__(self):
        return self.nom