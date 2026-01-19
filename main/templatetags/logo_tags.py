from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def get_logo_url(site_config):
    """
    Retourne l'URL du logo avec fallback vers le logo statique par défaut.
    Utilise le logo de la base de données si disponible, sinon utilise le logo statique.
    """
    if site_config and site_config.logo:
        return site_config.logo.url
    else:
        # Fallback vers le logo statique par défaut
        return static('images/logo-global-it-new.png')

@register.simple_tag
def get_logo_static():
    """
    Retourne toujours l'URL du logo statique (utile pour forcer le logo statique).
    """
    return static('images/logo-global-it-new.png')

@register.simple_tag
def get_about_image_static():
    """
    Retourne l'URL de l'image about statique.
    """
    return static('images/about/Design_sans_titre10.png')

@register.simple_tag
def get_about_image_url(site_config):
    """
    Retourne l'URL de l'image about avec fallback vers l'image statique.
    Utilise l'image de la base de données si disponible, sinon utilise l'image statique.
    """
    if site_config and hasattr(site_config, 'about_image') and site_config.about_image:
        return site_config.about_image.url
    else:
        # Fallback vers l'image statique par défaut
        return static('images/about/Design_sans_titre10.png')