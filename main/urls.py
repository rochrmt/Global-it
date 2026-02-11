from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('formations/', views.formations, name='formations'),
    path('formation/<int:pk>/', views.formation_detail, name='formation_detail'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.about, name='about'),
    path('partenaires/', views.partners, name='partners'),
    
    # URLs Soumission formulaires
    path('contact/submit-service/', views.submit_service_request, name='submit_service_request'),
    path('contact/submit-formation/', views.submit_formation_request, name='submit_formation_request'),
    path('contact/submit-quick/', views.submit_quick_request, name='submit_quick_request'),
    
    # URLs Recrutement
    path('recrutement/', views.job_offers, name='job_offers'),
    path('recrutement/offre/<int:pk>/', views.job_offer_detail, name='job_offer_detail'),
    
    # URLs Admin personnalisées
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/system-info/', admin_views.system_info, name='system_info'),
    path('admin/contacts/', admin_views.contact_management, name='contact_management'),
    path('admin/quick-actions/', admin_views.quick_actions, name='quick_actions'),
]