"""
Request/Response Logging Middleware for Sea Cox V2
===================================================
Logs every incoming HTTP request and outgoing response with useful metadata
such as method, path, status code, response time, and client IP.

Unhandled exceptions are also captured with full tracebacks.
"""

import time
import logging
import traceback

logger = logging.getLogger('sea_cox_v2.request')


class RequestResponseLoggingMiddleware:
    """
    Middleware that logs:
    - Every incoming request (method, path, IP, user-agent)
    - Every outgoing response (status code, response time)
    - Unhandled exceptions with full tracebacks
    
    Add to MIDDLEWARE in settings.py:
        'core.middleware.RequestResponseLoggingMiddleware',
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ── Pre-request ──────────────────────────────────────────────
        start_time = time.monotonic()
        client_ip = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        logger.info(
            "Request: %s %s | IP: %s | User-Agent: %s",
            request.method,
            request.get_full_path(),
            client_ip,
            user_agent,
        )

        # ── Process request → response ──────────────────────────────
        response = self.get_response(request)

        # ── Post-response ────────────────────────────────────────────
        duration_ms = (time.monotonic() - start_time) * 1000
        status_code = response.status_code

        log_method = logger.info if status_code < 400 else logger.warning
        if status_code >= 500:
            log_method = logger.error

        log_method(
            "Response: %s %s | Status: %d | Duration: %.2fms | IP: %s",
            request.method,
            request.get_full_path(),
            status_code,
            duration_ms,
            client_ip,
        )

        return response

    def process_exception(self, request, exception):
        """
        Called when a view raises an unhandled exception.
        Logs the full traceback at ERROR level.
        """
        from django.http import Http404
        if isinstance(exception, Http404):
            return None

        client_ip = self._get_client_ip(request)
        logger.error(
            "Unhandled Exception: %s %s | IP: %s\n%s",
            request.method,
            request.get_full_path(),
            client_ip,
            traceback.format_exc(),
        )
        # Return None to let Django's default exception handling continue
        return None

    @staticmethod
    def _get_client_ip(request):
        """
        Extract the real client IP, accounting for reverse proxies
        (e.g., Nginx, load balancers, Docker networking).
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # First IP in the chain is the real client
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'Unknown')
