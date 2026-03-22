from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.views.static import serve
from django.template.loader import render_to_string


def robots_txt(request):
    """Dynamic robots.txt with sitemap reference."""
    host = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and private paths",
        "Disallow: /static/assets/css/",
        "Disallow: /static/assets/js/",
        "",
        "# Sitemaps",
        f"Sitemap: {protocol}://{host}/sitemap.xml",
        "",
        "# Crawl-delay",
        "Crawl-delay: 1",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """Dynamic XML sitemap listing all public URLs."""
    from home.data import LATEST_NEWS
    host = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
    base_url = f"{protocol}://{host}"

    # Static pages with their priority and change frequency
    pages = [
        {"loc": "/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": "/about/", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/services/", "changefreq": "monthly", "priority": "0.9"},
        {"loc": "/news/", "changefreq": "weekly", "priority": "0.7"},
        {"loc": "/clients/", "changefreq": "monthly", "priority": "0.6"},
        {"loc": "/team/", "changefreq": "monthly", "priority": "0.5"},
        {"loc": "/contact/", "changefreq": "monthly", "priority": "0.8"},
    ]

    # Add news detail pages
    published_news = [n for n in LATEST_NEWS if n.get('status') == 1]
    for article in published_news:
        pages.append({
            "loc": f"/news/{article['slug']}/",
            "changefreq": "yearly",
            "priority": "0.6",
            "lastmod": article.get('updated_on', article.get('created_on', '')),
        })

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
    ]

    for page in pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}{page['loc']}</loc>")
        if page.get('lastmod'):
            xml_lines.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{page['priority']}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    return HttpResponse("\n".join(xml_lines), content_type="application/xml")


urlpatterns = [
    path('', include('home.urls')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

urlpatterns += [
    re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ── Custom Error Handlers (used when DEBUG = False) ──────────────────
handler400 = 'core.error_handlers.handler_400'
handler403 = 'core.error_handlers.handler_403'
handler404 = 'core.error_handlers.handler_404'
handler500 = 'core.error_handlers.handler_500'
