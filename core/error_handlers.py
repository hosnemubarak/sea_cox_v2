"""
Custom Error Handler Views for Sea Cox V2
==========================================
Production-grade error handlers that render branded error pages,
generate unique error IDs for tracking, and log comprehensive
diagnostic information.

Each handler:
  • Returns the correct HTTP status code
  • Generates a UUID-based error ID (logged + shown on page)
  • Passes rich context to the template (path, timestamp, error ID)
  • Logs method, path, IP, user-agent, and (for 500s) the full traceback
"""

import uuid
import logging
import traceback
from datetime import datetime

from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template.loader import render_to_string
from django.utils.timezone import now as tz_now

logger = logging.getLogger('sea_cox_v2')


# ── Helpers ──────────────────────────────────────────────────────────
def _get_client_ip(request):
    """Extract real client IP, accounting for proxies."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'Unknown')


def _build_error_context(request, status_code, error_id):
    """Build the template context common to every error page."""
    return {
        'error_code': status_code,
        'error_id': error_id,
        'request_path': request.path,
        'request_method': request.method,
        'timestamp': tz_now().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'page_title': f'Error {status_code}',
    }


def _log_error(request, status_code, error_id, *, exc_info=False):
    """Centralised error logging with request metadata."""
    client_ip = _get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    message = (
        "HTTP %d | Error ID: %s | %s %s | IP: %s | UA: %s"
    )
    args = (
        status_code,
        error_id,
        request.method,
        request.get_full_path(),
        client_ip,
        user_agent,
    )

    if status_code >= 500:
        logger.error(message, *args, exc_info=exc_info)
    elif status_code >= 400:
        logger.warning(message, *args)


# ── 400 Bad Request ──────────────────────────────────────────────────
def handler_400(request, exception=None):
    error_id = str(uuid.uuid4())
    _log_error(request, 400, error_id)

    context = _build_error_context(request, 400, error_id)
    context.update({
        'error_title': 'Bad Request',
        'error_message': (
            'The server could not understand your request. '
            'Please check the URL or form data and try again.'
        ),
        'error_icon': 'fas fa-exclamation-circle',
    })

    html = render_to_string('errors/400.html', context, request=request)
    return HttpResponseBadRequest(html)


# ── 403 Forbidden ────────────────────────────────────────────────────
def handler_403(request, exception=None):
    error_id = str(uuid.uuid4())
    _log_error(request, 403, error_id)

    context = _build_error_context(request, 403, error_id)
    context.update({
        'error_title': 'Access Denied',
        'error_message': (
            "You don't have permission to access this resource. "
            "If you believe this is an error, please contact our support team."
        ),
        'error_icon': 'fas fa-shield-alt',
    })

    html = render_to_string('errors/403.html', context, request=request)
    return HttpResponseForbidden(html)


# ── 404 Not Found ────────────────────────────────────────────────────
def handler_404(request, exception=None):
    error_id = str(uuid.uuid4())
    _log_error(request, 404, error_id)

    context = _build_error_context(request, 404, error_id)
    context.update({
        'error_title': 'Page Not Found',
        'error_message': (
            "The page you're looking for doesn't exist or has been moved. "
            "Please check the URL or navigate back to our homepage."
        ),
        'error_icon': 'fas fa-compass',
    })

    html = render_to_string('errors/404.html', context, request=request)
    return HttpResponseNotFound(html)


# ── 500 Internal Server Error ────────────────────────────────────────
def handler_500(request):
    """
    The 500 handler receives NO exception argument from Django.
    We still capture the traceback via exc_info=True in the logger.
    """
    error_id = str(uuid.uuid4())
    _log_error(request, 500, error_id, exc_info=True)

    context = _build_error_context(request, 500, error_id)
    context.update({
        'error_title': 'Server Error',
        'error_message': (
            "Something went wrong on our end. Our team has been notified "
            "and is working to fix the issue. Please try again later."
        ),
        'error_icon': 'fas fa-server',
    })

    # For 500 errors, render_to_string without request to avoid
    # potential infinite loops if the error originates from a
    # context processor or middleware.
    try:
        html = render_to_string('errors/500.html', context, request=request)
    except Exception:
        # Ultimate fallback – minimal HTML if template rendering itself fails
        logger.critical(
            "Failed to render 500 template | Error ID: %s\n%s",
            error_id,
            traceback.format_exc(),
        )
        html = render_to_string('errors/500.html', context)

    return HttpResponseServerError(html)
