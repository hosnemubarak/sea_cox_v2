"""
SEO data for each page — meta descriptions, keywords, OG tags.
Centralized here for easy maintenance.
"""

# Default site-wide SEO
SITE_SEO = {
    "site_name": "Sea Cox's Fire & Safety LLC",
    "site_url": "https://seacoxfire.com",
    "default_image": "/static/assets/images/logo-final.png",
    "locale": "en_US",
    "twitter_handle": "@seacoxfire",
}

# Per-page SEO metadata
PAGE_SEO = {
    "home": {
        "title": "Sea Cox's Fire & Safety LLC — DCD Grade A+ Fire Protection Dubai",
        "meta_description": "Sea Cox's Fire & Safety LLC is a DCD Grade A+ approved fire protection company in Dubai. We provide fire alarm systems, firefighting equipment, safety solutions, and engineering services. ISO accredited & NFPA member.",
        "meta_keywords": "fire safety Dubai, fire protection company Dubai, fire alarm system Dubai, DCD Grade A+ fire company, firefighting equipment UAE, Sea Cox fire safety, fire engineering Dubai, NFPA member Dubai, fire extinguisher Dubai, smoke detector Dubai",
        "og_type": "website",
    },
    "about": {
        "title": "About Us — Sea Cox's Fire & Safety LLC",
        "meta_description": "Learn about Sea Cox's Fire & Safety LLC, an ISO accredited and NFPA member fire protection company in Dubai. Established in 2020, we are DCD Grade A+ approved with a commitment to safety excellence.",
        "meta_keywords": "about Sea Cox fire safety, fire protection company history, ISO accredited fire company Dubai, DCD approved fire company, NFPA member UAE, fire safety engineers Dubai",
        "og_type": "website",
    },
    "services": {
        "title": "Fire Safety Services — Sea Cox's Fire & Safety LLC",
        "meta_description": "Comprehensive fire protection services including fire alarm installation, firefighting systems, maintenance, and fire safety projects. Expert fire engineering solutions in Dubai by Sea Cox's Fire & Safety.",
        "meta_keywords": "fire alarm installation Dubai, fire safety services, fire system maintenance Dubai, firefighting system installation, fire protection engineering, sprinkler system Dubai, fire pump installation",
        "og_type": "website",
    },
    "news": {
        "title": "News & Certifications — Sea Cox's Fire & Safety LLC",
        "meta_description": "Latest news, certifications, and updates from Sea Cox's Fire & Safety LLC. View our Dubai Civil Defense License, Chamber Membership Certificate, and Commercial License.",
        "meta_keywords": "fire safety news Dubai, Sea Cox certifications, Dubai Civil Defense license, fire company certificates UAE, fire safety updates",
        "og_type": "website",
    },
    "clients": {
        "title": "Our Clients — Sea Cox's Fire & Safety LLC",
        "meta_description": "Trusted by leading real estate companies, hotels, and businesses across Dubai. Sea Cox's Fire & Safety LLC proudly serves Al Taraheeb, Grand Mayfair Hotel, Depa Interiors, and many more.",
        "meta_keywords": "fire safety clients Dubai, fire protection portfolio, Sea Cox clients, fire alarm customers Dubai, real estate fire safety, hotel fire safety Dubai",
        "og_type": "website",
    },
    "team": {
        "title": "Our Team — Sea Cox's Fire & Safety LLC",
        "meta_description": "Meet the expert team at Sea Cox's Fire & Safety LLC. Our experienced fire protection engineers and safety professionals deliver world-class fire engineering solutions in Dubai.",
        "meta_keywords": "fire safety team Dubai, fire protection engineers, Sea Cox team members, fire safety professionals UAE",
        "og_type": "website",
    },
    "contact": {
        "title": "Contact Us — Sea Cox's Fire & Safety LLC",
        "meta_description": "Contact Sea Cox's Fire & Safety LLC for fire protection services in Dubai. Visit us at Naïf Road, Al Nakhil Deira Dubai. Call +971 556540461 or email seacoxsfirensafety@gmail.com.",
        "meta_keywords": "contact fire safety company Dubai, Sea Cox contact, fire protection inquiry, fire safety quote Dubai, fire alarm company phone number",
        "og_type": "website",
    },
}


def get_page_seo(page_key, request, extra=None):
    """
    Build a complete SEO context dict for a given page.
    `extra` can override any field (e.g. for news detail pages).
    """
    seo = {**SITE_SEO, **PAGE_SEO.get(page_key, {})}

    # Build canonical URL
    seo["canonical_url"] = f"{SITE_SEO['site_url']}{request.path}"

    # OG image — absolute URL
    if extra and extra.get("og_image"):
        seo["og_image"] = extra["og_image"]
    else:
        seo["og_image"] = f"{SITE_SEO['site_url']}{SITE_SEO['default_image']}"

    # Allow overrides
    if extra:
        seo.update(extra)

    return {"seo": seo}
