import logging

from django.shortcuts import render
from .data import (
    PRODUCTS, CLIENTS, TEAMS, VIDEOS, LATEST_WORKS,
    LATEST_NEWS, SERVICES_CATEGORIES, STATS, ABOUT_TEXT, CORE_VALUES
)
from .seo import get_page_seo, SITE_SEO

# Get a logger for this module — logs to 'home' logger configured in settings
logger = logging.getLogger(__name__)


def home(request):
    published_news = [n for n in LATEST_NEWS if n['status'] == 1]
    context = {
        'products': PRODUCTS[:8],
        'clients': CLIENTS[:3],
        'videos': VIDEOS[:8],
        'teams': TEAMS[:3],
        'works': LATEST_WORKS,
        'news': published_news[:2],
        'services_categories': SERVICES_CATEGORIES,
        'stats': STATS,
        'about_text': ABOUT_TEXT,
        'page_title': 'Home',
    }
    context.update(get_page_seo('home', request))
    logger.info("Home page rendered | IP: %s", request.META.get('REMOTE_ADDR'))
    return render(request, 'home/home.html', context)


def about_us(request):
    context = {
        'about_text': ABOUT_TEXT,
        'core_values': CORE_VALUES,
        'stats': STATS,
        'page_title': 'About Us',
    }
    context.update(get_page_seo('about', request))
    logger.info("About Us page rendered")
    return render(request, 'home/about_us.html', context)


def services(request):
    context = {
        'services_categories': SERVICES_CATEGORIES,
        'products': PRODUCTS,
        'page_title': 'Services',
    }
    context.update(get_page_seo('services', request))
    logger.info("Services page rendered")
    return render(request, 'home/services.html', context)


def clients(request):
    context = {
        'clients': CLIENTS,
        'page_title': 'Our Clients',
    }
    context.update(get_page_seo('clients', request))
    logger.info("Clients page rendered")
    return render(request, 'home/clients.html', context)


def news(request):
    published_news = [n for n in LATEST_NEWS if n['status'] == 1]
    context = {
        'news': published_news,
        'page_title': 'News & Update',
    }
    context.update(get_page_seo('news', request))
    logger.info("News listing page rendered | Articles count: %d", len(published_news))
    return render(request, 'home/news.html', context)


def news_details(request, slug):
    try:
        article = None
        for n in LATEST_NEWS:
            if n['slug'] == slug:
                article = n
                break

        if not article:
            logger.warning("News article not found | Slug: %s | IP: %s", slug, request.META.get('REMOTE_ADDR'))

        published_news = [n for n in LATEST_NEWS if n['status'] == 1]
        recent = [n for n in published_news if n.get('slug') != slug][:2]

        context = {
            'article': article,
            'recent_news': recent,
            'page_title': article['title'] if article else 'News Details',
        }

        # Dynamic SEO for news detail pages
        if article:
            extra = {
                "title": f"{article['title']} — Sea Cox's Fire & Safety LLC",
                "meta_description": f"{article['content'][:150]}. Read more about {article['title']} at Sea Cox's Fire & Safety LLC.",
                "meta_keywords": f"{article['title']}, fire safety news, Sea Cox certifications, Dubai fire safety",
                "og_type": "article",
                "og_image": f"{SITE_SEO['site_url']}/media/{article['img']}",
                "article_published": article.get('created_on', ''),
                "article_modified": article.get('updated_on', ''),
                "article_author": article.get('author', 'Admin'),
            }
            context.update(get_page_seo('news', request, extra))
            logger.info("News detail rendered | Slug: %s | Title: %s", slug, article['title'])
        else:
            context.update(get_page_seo('news', request))

        return render(request, 'home/news_details.html', context)

    except Exception:
        logger.exception("Error rendering news detail | Slug: %s", slug)
        raise


def contact(request):
    context = {
        'page_title': 'Contact Us',
    }
    context.update(get_page_seo('contact', request))
    logger.info("Contact page rendered")
    return render(request, 'home/contact.html', context)


def team(request):
    context = {
        'teams': TEAMS,
        'page_title': 'Our Team',
    }
    context.update(get_page_seo('team', request))
    logger.info("Team page rendered")
    return render(request, 'home/team.html', context)

