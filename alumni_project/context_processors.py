from django.conf import settings


def brand_colors(request):
    return {
        'SITE_PRIMARY_COLOR': getattr(settings, 'SITE_PRIMARY_COLOR', '#901d78'),
        'SITE_SECONDARY_COLOR': getattr(settings, 'SITE_SECONDARY_COLOR', '#7a1866'),
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'AlumniConnect'),
    }
