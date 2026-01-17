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
    
    # URLs Admin personnalisées
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/system-info/', admin_views.system_info, name='system_info'),
    path('admin/contacts/', admin_views.contact_management, name='contact_management'),
    path('admin/quick-actions/', admin_views.quick_actions, name='quick_actions'),
]