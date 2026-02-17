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
    nom_site = models.CharField(max_length=100, default="Global-IT")
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


class Brand(models.Model):
    """Marques de l'entreprise"""
    
    nom = models.CharField(max_length=100, help_text="Nom de la marque")
    site_web = models.URLField(help_text="URL du site web de la marque")
    logo = models.ImageField(upload_to='brands/', 
                           validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])],
                           help_text="Logo de la marque")
    description = models.TextField(blank=True, help_text="Description optionnelle de la marque")
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    est_actif = models.BooleanField(default=True, help_text="Afficher cette marque sur le site")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
    
    def __str__(self):
        return self.nom


class OffreEmploi(models.Model):
    """Offres d'emploi"""
    
    TYPE_CONTRAT_CHOICES = [
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('stage', 'Stage'),
        ('alternance', 'Alternance'),
        ('freelance', 'Freelance'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre du poste")
    description = models.TextField(verbose_name="Description du poste")
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES, default='cdi', verbose_name="Type de contrat")
    lieu = models.CharField(max_length=200, verbose_name="Lieu de travail")
    missions = models.TextField(verbose_name="Missions principales")
    profil_recherche = models.TextField(verbose_name="Profil recherché")
    experience_min = models.CharField(max_length=100, blank=True, verbose_name="Expérience minimale", help_text="Ex: 2 ans, Débutant accepté")
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salaire minimum (€)")
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salaire maximum (€)")
    date_debut = models.DateField(blank=True, null=True, verbose_name="Date de début souhaitée")
    date_limite = models.DateField(blank=True, null=True, verbose_name="Date limite de candidature")
    avantages = models.TextField(blank=True, verbose_name="Avantages", help_text="Tickets restaurant, télétravail, etc.")
    image = models.ImageField(upload_to='job_offers/', blank=True, null=True, 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
                             help_text="Image de présentation de l'offre")
    urgent = models.BooleanField(default=False, verbose_name="Recrutement urgent")
    est_actif = models.BooleanField(default=True, verbose_name="Offre active")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        ordering = ['-urgent', '-date_creation']
        verbose_name = 'Offre d\'emploi'
        verbose_name_plural = 'Offres d\'emploi'
    
    def __str__(self):
        return f"{self.titre} ({self.get_type_contrat_display()})"
    
    def nb_candidatures(self):
        """Retourne le nombre de candidatures pour cette offre"""
        return self.candidatures.count()


class Candidature(models.Model):
    """Candidatures pour les offres d'emploi"""
    
    STATUT_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('en_cours', 'En cours d\'examen'),
        ('acceptee', 'Acceptée'),
        ('rejetee', 'Rejetée'),
    ]
    
    offre_emploi = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, related_name='candidatures', verbose_name="Offre d'emploi")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    motivation = models.TextField(verbose_name="Lettre de motivation")
    cv = models.FileField(upload_to='cv/', 
                         validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
                         verbose_name="CV",
                         help_text="Formats acceptés: PDF, DOC, DOCX (max 5MB)")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouvelle', verbose_name="Statut")
    notes_admin = models.TextField(blank=True, verbose_name="Notes internes", help_text="Visibles uniquement par les administrateurs")
    date_candidature = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        ordering = ['-date_candidature']
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.offre_emploi.titre}"
    
    def get_cv_filename(self):
        """Retourne le nom du fichier CV"""
        import os
        return os.path.basename(self.cv.name) if self.cv else ''


class CandidatureSpontanee(models.Model):
    """Candidatures spontanées"""
    
    STATUT_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('en_cours', 'En cours d\'examen'),
        ('acceptee', 'Acceptée'),
        ('rejetee', 'Rejetée'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    poste_souhaite = models.CharField(max_length=200, verbose_name="Poste souhaité")
    motivation = models.TextField(verbose_name="Lettre de motivation")
    cv = models.FileField(upload_to='cv/', 
                         validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
                         verbose_name="CV",
                         help_text="Formats acceptés: PDF, DOC, DOCX (max 5MB)")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouvelle', verbose_name="Statut")
    notes_admin = models.TextField(blank=True, verbose_name="Notes internes", help_text="Visibles uniquement par les administrateurs")
    date_candidature = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        ordering = ['-date_candidature']
        verbose_name = 'Candidature spontanée'
        verbose_name_plural = 'Candidatures spontanées'
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.poste_souhaite}"
    
    def get_cv_filename(self):
        """Retourne le nom du fichier CV"""
        import os
        return os.path.basename(self.cv.name) if self.cv else ''
