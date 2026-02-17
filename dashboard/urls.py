from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentification
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    
    # Page d'accueil du dashboard
    path('', views.home, name='home'),
    
    # Gestion des images
    path('images/', views.image_manager, name='image_manager'),
    path('images/upload/', views.upload_image, name='upload_image'),
    path('images/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('images/<int:image_id>/toggle/', views.toggle_image_status, name='toggle_image_status'),
    path('images/<int:image_id>/delete-overview/', views.delete_image_overview, name='delete_image_overview'),
    path('images/<int:image_id>/toggle-overview/', views.toggle_image_overview, name='toggle_image_overview'),
    
    # Synchronisation des images
    path('sync/', views.sync_dashboard, name='sync_dashboard'),
    path('sync/service/', views.sync_image_to_service, name='sync_image_to_service'),
    path('sync/formation/', views.sync_image_to_formation, name='sync_image_to_formation'),
    path('sync/site-config/', views.sync_image_to_site_config, name='sync_image_to_site_config'),
    path('sync/carousel/', views.sync_image_to_carousel, name='sync_image_to_carousel'),
    
    # Gestion des images carousel
    path('carousel/', views.carousel_manager, name='carousel_manager'),
    path('carousel/add/', views.add_carousel_image, name='add_carousel_image'),
    path('carousel/<int:image_id>/edit/', views.edit_carousel_image, name='edit_carousel_image'),
    path('carousel/<int:image_id>/delete/', views.delete_carousel_image, name='delete_carousel_image'),
    path('carousel/<int:image_id>/toggle/', views.toggle_carousel_status, name='toggle_carousel_status'),
    
    # Gestion des images about
    path('about/', views.about_manager, name='about_manager'),
    path('about/add/', views.add_about_image, name='add_about_image'),
    path('about/<int:image_id>/edit/', views.edit_about_image, name='edit_about_image'),
    path('about/<int:image_id>/delete/', views.delete_about_image, name='delete_about_image'),
    path('about/<int:image_id>/toggle/', views.toggle_about_status, name='toggle_about_status'),
    
    # Synchronisation about
    path('sync/about/', views.sync_image_to_about, name='sync_image_to_about'),
    
    # Paramètres du site
    path('settings/', views.site_settings, name='site_settings'),
    
    # Gestion du contenu
    path('content/', views.content_manager, name='content_manager'),
    
    # CRUD pour les services
    path('services/<int:service_id>/toggle/', views.toggle_service_status, name='toggle_service_status'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    
    # CRUD pour les formations
    path('formations/<int:formation_id>/toggle/', views.toggle_formation_status, name='toggle_formation_status'),
    path('formations/<int:formation_id>/delete/', views.delete_formation, name='delete_formation'),
    
    # CRUD pour l'équipe
    path('team/<int:member_id>/delete/', views.delete_team_member, name='delete_team_member'),
    
    # CRUD pour le blog
    path('blog/<int:post_id>/toggle/', views.toggle_blog_post_status, name='toggle_blog_post_status'),
    path('blog/<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    
    # Gestion des avis clients
    path('customer-reviews/', views.customer_reviews_manager, name='customer_reviews_manager'),
    path('customer-reviews/add/', views.add_customer_review, name='add_customer_review'),
    path('customer-reviews/<int:review_id>/edit/', views.edit_customer_review, name='edit_customer_review'),
    path('customer-reviews/<int:review_id>/delete/', views.delete_customer_review, name='delete_customer_review'),
    path('customer-reviews/<int:review_id>/toggle/', views.toggle_customer_review_status, name='toggle_customer_review_status'),
    path('customer-reviews/<int:review_id>/get/', views.get_customer_review, name='get_customer_review'),
    
    # API pour récupérer les données
    path('services/<int:service_id>/get/', views.get_service, name='get_service'),
    path('formations/<int:formation_id>/get/', views.get_formation, name='get_formation'),
    
    # Ajout et édition
    path('services/add/', views.add_service, name='add_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('formations/add/', views.add_formation, name='add_formation'),
    path('formations/<int:formation_id>/edit/', views.edit_formation, name='edit_formation'),
    
    # Journal d'activité
    path('activity/', views.activity_log, name='activity_log'),
    
    # Gestion des partenaires
    path('partners/', views.partner_manager, name='partner_manager'),
    path('partners/add/', views.add_partner, name='add_partner'),
    path('partners/<int:partner_id>/edit/', views.edit_partner, name='edit_partner'),
    path('partners/<int:partner_id>/delete/', views.delete_partner, name='delete_partner'),
    path('partners/<int:partner_id>/toggle/', views.toggle_partner_status, name='toggle_partner_status'),
    
    # Gestion des marques
    path('brands/', views.brand_manager, name='brand_manager'),
    path('brands/add/', views.add_brand, name='add_brand'),
    path('brands/<int:brand_id>/edit/', views.edit_brand, name='edit_brand'),
    path('brands/<int:brand_id>/delete/', views.delete_brand, name='delete_brand'),
    path('brands/<int:brand_id>/toggle/', views.toggle_brand_status, name='toggle_brand_status'),
    
    # Gestionnaire de fichiers
    path('files/', views.file_manager, name='file_manager'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/create-folder/', views.create_folder, name='create_folder'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    
    # Gestion du recrutement
    path('recruitment/', views.recruitment_manager, name='recruitment_manager'),
    path('recruitment/jobs/add/', views.add_job_offer, name='add_job_offer'),
    path('recruitment/jobs/<int:pk>/edit/', views.edit_job_offer, name='edit_job_offer'),
    path('recruitment/jobs/<int:pk>/delete/', views.delete_job_offer, name='delete_job_offer'),
    path('recruitment/jobs/<int:pk>/toggle/', views.toggle_job_offer_status, name='toggle_job_offer_status'),
    path('recruitment/applications/<int:pk>/', views.view_application, name='view_application'),
    path('recruitment/applications/<int:pk>/<str:type>/', views.view_application, name='view_application'),
    path('recruitment/applications/<int:pk>/status/', views.update_application_status, name='update_application_status'),
    path('recruitment/applications/<int:pk>/delete/', views.delete_application, name='delete_application'),
    
    # Gestion des demandes (Services/Formations/Contact)
    path('requests/', views.request_manager, name='request_manager'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
]
