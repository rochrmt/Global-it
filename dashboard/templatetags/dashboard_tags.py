from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def get_badge_color(image_type):
    """Retourne la couleur Bootstrap pour un type d'image"""
    colors = {
        'carousel': 'primary',
        'service': 'success', 
        'formation': 'info',
        'team': 'warning',
        'testimonial': 'secondary',
        'blog': 'dark',
        'gallery': 'light',
        'logo': 'primary',
        'other': 'secondary'
    }
    return colors.get(image_type, 'secondary')

@register.filter
def get_status_badge_color(status):
    """Retourne la couleur Bootstrap pour un statut"""
    colors = {
        'active': 'success',
        'inactive': 'danger',
        'pending': 'warning',
        'draft': 'secondary'
    }
    return colors.get(status, 'secondary')

@register.filter
def get_file_icon(file_name):
    """Retourne l'icône Font Awesome appropriée pour un type de fichier"""
    extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
    
    icon_map = {
        'pdf': 'fas fa-file-pdf text-danger',
        'doc': 'fas fa-file-word text-primary',
        'docx': 'fas fa-file-word text-primary',
        'xls': 'fas fa-file-excel text-success',
        'xlsx': 'fas fa-file-excel text-success',
        'ppt': 'fas fa-file-powerpoint text-warning',
        'pptx': 'fas fa-file-powerpoint text-warning',
        'jpg': 'fas fa-file-image text-warning',
        'jpeg': 'fas fa-file-image text-warning',
        'png': 'fas fa-file-image text-warning',
        'gif': 'fas fa-file-image text-warning',
        'svg': 'fas fa-file-image text-info',
        'mp4': 'fas fa-file-video text-danger',
        'avi': 'fas fa-file-video text-danger',
        'mp3': 'fas fa-file-audio text-info',
        'wav': 'fas fa-file-audio text-info',
        'zip': 'fas fa-file-archive text-secondary',
        'rar': 'fas fa-file-archive text-secondary',
        'txt': 'fas fa-file-alt text-dark',
        'csv': 'fas fa-file-csv text-success',
        'json': 'fas fa-file-code text-info',
        'xml': 'fas fa-file-code text-info',
        'html': 'fas fa-file-code text-danger',
        'css': 'fas fa-file-code text-primary',
        'js': 'fas fa-file-code text-warning',
        'py': 'fas fa-file-code text-dark',
    }
    
    return icon_map.get(extension, 'fas fa-file text-secondary')

@register.filter
def get_file_size_display(size_bytes):
    """Convertit la taille en bytes en format lisible"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

@register.filter
def get_action_icon(action):
    """Retourne l'icône pour une action d'activité"""
    icons = {
        'create': 'fa-plus-circle text-success',
        'update': 'fa-edit text-warning',
        'delete': 'fa-trash text-danger',
        'toggle': 'fa-toggle-on text-info',
        'login': 'fa-sign-in-alt text-success',
        'logout': 'fa-sign-out-alt text-secondary',
        'upload': 'fa-upload text-primary',
        'download': 'fa-download text-info',
    }
    return icons.get(action, 'fa-info-circle text-secondary')

@register.simple_tag
def get_activity_icon(action):
    """Retourne l'icône pour une action d'activité (version simple tag)"""
    icons = {
        'create': 'fas fa-plus-circle text-success',
        'update': 'fas fa-edit text-warning',
        'delete': 'fas fa-trash text-danger',
        'toggle': 'fas fa-toggle-on text-info',
        'login': 'fas fa-sign-in-alt text-success',
        'logout': 'fas fa-sign-out-alt text-secondary',
        'upload': 'fas fa-upload text-primary',
        'download': 'fas fa-download text-info',
    }
    return mark_safe(f'<i class="{icons.get(action, "fas fa-info-circle text-secondary")}"></i>')

@register.filter
def get_action_color(action):
    """Retourne la couleur Bootstrap pour une action"""
    colors = {
        'create': 'success',
        'update': 'warning',
        'delete': 'danger',
        'toggle': 'info',
        'login': 'success',
        'logout': 'secondary',
        'upload': 'primary',
        'download': 'info',
    }
    return colors.get(action, 'secondary')

@register.filter
def truncate_chars(text, max_length=50):
    """Tronque le texte à la longueur maximale"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'