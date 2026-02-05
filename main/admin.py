from django.contrib import admin
from django.utils.html import format_html
from .models import (Contact, Service, Formation, SiteConfiguration, CarouselImage, 
                     AboutImage, Partner, OffreEmploi, Candidature, CandidatureSpontanee, CustomerReview)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'image_preview', 'date_creation', 'date_modification']
    list_filter = ['categorie', 'date_creation']
    search_fields = ['titre', 'description']
    readonly_fields = ['image_preview_large', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'categorie', 'description_courte', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Apparence', {
            'fields': ('icone', 'ordre', 'est_actif')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    image_preview.short_description = 'Aperçu'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.image.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    image_preview_large.short_description = 'Aperçu de l\'image'
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['nom', 'site_web', 'ordre', 'est_actif', 'logo_preview', 'date_creation']
    list_filter = ['est_actif', 'date_creation']
    list_editable = ['ordre', 'est_actif']
    search_fields = ['nom', 'description']
    readonly_fields = ['logo_preview_large', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'site_web', 'description', 'ordre', 'est_actif')
        }),
        ('Logo', {
            'fields': ('logo', 'logo_preview_large')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.logo.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    logo_preview.short_description = 'Aperçu'
    
    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: contain; border-radius: 10px; background: white; padding: 20px;" /><small style="display: block; margin-top: 8px;">Logo actuel</small>', obj.logo.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucun logo</small></div>')
    logo_preview_large.short_description = 'Aperçu du logo'


@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'ordre', 'est_actif', 'image_preview', 'date_creation']
    list_filter = ['est_actif', 'date_creation']
    list_editable = ['ordre', 'est_actif']
    search_fields = ['titre', 'description']
    readonly_fields = ['image_preview_large', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations', {
            'fields': ('titre', 'description', 'ordre', 'est_actif')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    image_preview.short_description = 'Aperçu'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.image.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    image_preview_large.short_description = 'Aperçu de l\'image'

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'niveau', 'image_preview', 'prix', 'disponible', 'date_creation']
    list_filter = ['categorie', 'niveau', 'disponible', 'date_creation']
    search_fields = ['titre', 'description', 'objectifs']
    readonly_fields = ['image_preview_large', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'categorie', 'niveau', 'description_courte', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Détails de la formation', {
            'fields': ('duree', 'prix', 'disponible', 'objectifs', 'contenu', 'prerequis')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    image_preview.short_description = 'Aperçu'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.image.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    image_preview_large.short_description = 'Aperçu de l\'image'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'date_creation', 'traite']
    list_filter = ['traite', 'date_creation']
    search_fields = ['nom', 'email', 'sujet', 'message']
    readonly_fields = ['nom', 'email', 'telephone', 'sujet', 'message', 'date_creation']
    list_editable = ['traite']
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'email', 'telephone')
        }),
        ('Message', {
            'fields': ('sujet', 'message')
        }),
        ('Intérêts', {
            'fields': ('service_interesse', 'formation_interessee')
        }),
        ('Statut', {
            'fields': ('traite', 'date_creation'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marquer_comme_traite', 'marquer_comme_non_traite']
    
    def marquer_comme_traite(self, request, queryset):
        queryset.update(traite=True)
        self.message_user(request, f'{queryset.count()} message(s) marqué(s) comme traité(s).')
    marquer_comme_traite.short_description = 'Marquer comme traité'
    
    def marquer_comme_non_traite(self, request, queryset):
        queryset.update(traite=False)
        self.message_user(request, f'{queryset.count()} message(s) marqué(s) comme non traité(s).')
    marquer_comme_non_traite.short_description = 'Marquer comme non traité'

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'active', 'updated_at']
    readonly_fields = ['logo_preview', 'hero_preview', 'about_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_site', 'logo', 'logo_preview')
        }),
        ('Activation', {
            'fields': ('active',)
        }),
        ('Section Hero', {
            'fields': ('hero_titre', 'hero_sous_titre', 'hero_image', 'hero_image_preview')
        }),
        ('Section À propos', {
            'fields': ('about_titre', 'about_description', 'about_image', 'about_image_preview')
        }),
        ('Contact', {
            'fields': ('telephone', 'email', 'adresse')
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="200" height="60" style="object-fit: contain; border-radius: 8px; background: white; padding: 10px;" /><small style="display: block; margin-top: 8px;">Logo actuel</small>', obj.logo.url)
        return format_html('<div style="width: 200px; height: 60px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i><span style="margin-left: 8px;">Aucun logo</span></div>')
    logo_preview.short_description = 'Aperçu Logo'
    
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="400" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.hero_image.url)
        return format_html('<div style="width: 400px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    hero_preview.short_description = 'Aperçu Hero'
    
    def about_preview(self, obj):
        if obj.about_image:
            return format_html('<img src="{}" width="400" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.about_image.url)
        return format_html('<div style="width: 400px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    about_preview.short_description = 'Aperçu About'
    
    def has_add_permission(self, request):
        # Empêche d'ajouter plusieurs configurations
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Empêche la suppression de la seule configuration
        return False


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'ordre', 'est_actif', 'image_preview', 'date_creation']
    list_filter = ['est_actif', 'date_creation']
    list_editable = ['ordre', 'est_actif']
    search_fields = ['titre', 'description']
    readonly_fields = ['image_preview_large', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations', {
            'fields': ('titre', 'description', 'ordre', 'est_actif')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 5px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image text-muted"></i></div>')
    image_preview.short_description = 'Aperçu'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.image.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    image_preview_large.short_description = 'Aperçu de l\'image'

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['nom', 'note', 'entreprise', 'est_actif',  'date_creation']
    list_filter = ['est_actif', 'note', 'date_creation']
    list_editable = ['est_actif']
    search_fields = ['nom', 'entreprise', 'commentaire']


@admin.register(OffreEmploi)
class OffreEmploiAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_contrat', 'lieu', 'urgent', 'est_actif', 'nb_candidatures_display', 'date_creation']
    list_filter = ['type_contrat', 'urgent', 'est_actif', 'date_creation']
    list_editable = ['urgent', 'est_actif']
    search_fields = ['titre', 'description', 'lieu']
    readonly_fields = ['image_preview_large', 'date_creation', 'date_modification', 'nb_candidatures_display']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'type_contrat', 'lieu', 'description')
        }),
        ('Détails du poste', {
            'fields': ('missions', 'profil_recherche', 'experience_min')
        }),
        ('Rémunération', {
            'fields': ('salaire_min', 'salaire_max')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_limite')
        }),
        ('Avantages', {
            'fields': ('avantages',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Options', {
            'fields': ('urgent', 'est_actif', 'nb_candidatures_display')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def nb_candidatures_display(self, obj):
        count = obj.nb_candidatures()
        if count > 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">{} candidature(s)</span>', count)
        return format_html('<span style="color: #6c757d;">0 candidature</span>')
    nb_candidatures_display.short_description = 'Candidatures'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="200" style="object-fit: cover; border-radius: 10px;" /><small style="display: block; margin-top: 8px;">Image actuelle</small>', obj.image.url)
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-direction: column;"><i class="fas fa-image text-muted" style="font-size: 48px;"></i><small style="margin-top: 8px;">Aucune image</small></div>')
    image_preview_large.short_description = 'Aperçu de l\'image'


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'email', 'offre_emploi', 'statut_badge', 'date_candidature']
    list_filter = ['statut', 'date_candidature', 'offre_emploi']
    search_fields = ['nom', 'prenom', 'email', 'motivation']
    readonly_fields = ['nom', 'prenom', 'email', 'telephone', 'motivation', 'cv', 'cv_link', 'date_candidature', 'date_modification']
    
    fieldsets = (
        ('Candidat', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Offre', {
            'fields': ('offre_emploi',)
        }),
        ('Motivation et CV', {
            'fields': ('motivation', 'cv', 'cv_link')
        }),
        ('Gestion', {
            'fields': ('statut', 'notes_admin')
        }),
        ('Dates', {
            'fields': ('date_candidature', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marquer_en_cours', 'marquer_acceptee', 'marquer_rejetee']
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = 'Candidat'
    
    def statut_badge(self, obj):
        colors = {
            'nouvelle': '#ffc107',
            'en_cours': '#17a2b8',
            'acceptee': '#28a745',
            'rejetee': '#dc3545',
        }
        color = colors.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def cv_link(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank" class="button">📄 Télécharger le CV</a>', obj.cv.url)
        return '-'
    cv_link.short_description = 'CV'
    
    def marquer_en_cours(self, request, queryset):
        queryset.update(statut='en_cours')
        self.message_user(request, f'{queryset.count()} candidature(s) marquée(s) en cours.')
    marquer_en_cours.short_description = 'Marquer en cours d\'examen'
    
    def marquer_acceptee(self, request, queryset):
        queryset.update(statut='acceptee')
        self.message_user(request, f'{queryset.count()} candidature(s) acceptée(s).')
    marquer_acceptee.short_description = 'Marquer comme acceptée'
    
    def marquer_rejetee(self, request, queryset):
        queryset.update(statut='rejetee')
        self.message_user(request, f'{queryset.count()} candidature(s) rejetée(s).')
    marquer_rejetee.short_description = 'Marquer comme rejetée'


@admin.register(CandidatureSpontanee)
class CandidatureSpontaneeAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'email', 'poste_souhaite', 'statut_badge', 'date_candidature']
    list_filter = ['statut', 'date_candidature']
    search_fields = ['nom', 'prenom', 'email', 'poste_souhaite', 'motivation']
    readonly_fields = ['nom', 'prenom', 'email', 'telephone', 'poste_souhaite', 'motivation', 'cv', 'cv_link', 'date_candidature', 'date_modification']
    
    fieldsets = (
        ('Candidat', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Poste souhaité', {
            'fields': ('poste_souhaite',)
        }),
        ('Motivation et CV', {
            'fields': ('motivation', 'cv', 'cv_link')
        }),
        ('Gestion', {
            'fields': ('statut', 'notes_admin')
        }),
        ('Dates', {
            'fields': ('date_candidature', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marquer_en_cours', 'marquer_acceptee', 'marquer_rejetee']
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = 'Candidat'
    
    def statut_badge(self, obj):
        colors = {
            'nouvelle': '#ffc107',
            'en_cours': '#17a2b8',
            'acceptee': '#28a745',
            'rejetee': '#dc3545',
        }
        color = colors.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def cv_link(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank" class="button">📄 Télécharger le CV</a>', obj.cv.url)
        return '-'
    cv_link.short_description = 'CV'
    
    def marquer_en_cours(self, request, queryset):
        queryset.update(statut='en_cours')
        self.message_user(request, f'{queryset.count()} candidature(s) marquée(s) en cours.')
    marquer_en_cours.short_description = 'Marquer en cours d\'examen'
    
    def marquer_acceptee(self, request, queryset):
        queryset.update(statut='acceptee')
        self.message_user(request, f'{queryset.count()} candidature(s) acceptée(s).')
    marquer_acceptee.short_description = 'Marquer comme acceptée'
    
    def marquer_rejetee(self, request, queryset):
        queryset.update(statut='rejetee')
        self.message_user(request, f'{queryset.count()} candidature(s) rejetée(s).')
    marquer_rejetee.short_description = 'Marquer comme rejetée'
