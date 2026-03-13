"""
Context processor to inject site info into every template.
"""
from .data import SITE_INFO


def site_info(request):
    return {'site_info': SITE_INFO}
