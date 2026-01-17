from .models import SiteConfiguration

def site_config(request):
    """Context processor pour rendre la configuration du site disponible dans tous les templates"""
    try:
        config = SiteConfiguration.objects.get(active=True)
    except SiteConfiguration.DoesNotExist:
        config = SiteConfiguration.objects.create()
    
    return {
        'site_config': config
    }