"""Inertia middleware."""

from functools import cached_property
from urllib.parse import unquote

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django_ratelimit.exceptions import Ratelimited
from inertia import share
from inertia.settings import settings

from config.svelte.validation import VALIDATION_ERRORS_SESSION_KEY
from config.svelte.validation import InertiaValidationError


class InertiaDetails:
    """Inertia details."""

    def __init__(self, request: HttpRequest) -> None:
        """Initialize the Inertia details."""
        self.request = request

    def _get_header_value(self, name: str) -> str | None:
        """Get header value."""
        value = self.request.headers.get(name) or None
        if value:
            if self.request.headers.get(f"{name}-URI-AutoEncoded") == "true":
                value = unquote(value)
        return value

    def __bool__(self) -> bool:
        """Check if the request is an Inertia request."""
        return self.is_inertia_request

    @cached_property
    def is_inertia_request(self):
        """Check if the request is an Inertia request."""
        return self._get_header_value("X-Inertia") == "true"

    @cached_property
    def context_to_add(self) -> list[str]:
        """Get context to add."""
        header = self._get_header_value("X-Inertia-Add-Data")
        # if header, split by comma and return
        return header.split(",") if header else []

    @cached_property
    def is_stale(self):
        """Check if the request is stale."""
        return (
            self._get_header_value("X-Inertia-Version") or settings.INERTIA_VERSION
        ) != settings.INERTIA_VERSION

    @cached_property
    def is_stale_inertia_get(self):
        """Check if the GET request is stale."""
        return self.request.method == "GET" and self.is_stale()


class InertiaRequest(HttpRequest):
    """Inertia request typing."""

    inertia_details: InertiaDetails


class InertiaMiddleware:
    """Inertia middleware."""

    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Handle Inertia requests."""
        validation_errors = request.session.get(VALIDATION_ERRORS_SESSION_KEY, None)

        if self.is_inertia_get_request(request) and validation_errors is not None:
            request.session.pop(VALIDATION_ERRORS_SESSION_KEY)
            request.session.modified = True
            # Must be shared before rendering the response
            share(request, errors=validation_errors)

        request.inertia_details = InertiaDetails(request)

        response = self.get_response(request)

        # Inertia requests don't ever render templates, so they skip the typical Django
        # CSRF path. We'll manually add a CSRF token for every request here.
        get_token(request)

        if not self.is_inertia_request(request):
            return response

        if self.is_non_post_redirect(request, response):
            response.status_code = 303

        if self.is_stale(request):
            return self.force_refresh(request)

        if self.is_error_response(response):
            return self.force_refresh(request)
            # TODO: check it - response.headers['X-Inertia-Location'] = "/500/"
            # TODO: check it - response.status_code = 409

        return response

    @staticmethod
    def process_exception(request: InertiaRequest, exception: Exception) -> None:
        """Handle inertia exceptions."""
        # if request.inertia_details.is_inertia_request:
        if isinstance(exception, InertiaValidationError):
            # Set validation errors
            errors = {field: errors[0] for field, errors in exception.errors.items()}
            request.session[VALIDATION_ERRORS_SESSION_KEY] = errors
            request.session.modified = True
            return exception.redirect

        if isinstance(exception, Ratelimited):
            # Set ratelimit error
            errors = {"ratelimit": "Too many requests. Please try again later."}
            request.session[VALIDATION_ERRORS_SESSION_KEY] = errors
            request.session.modified = True
            if request.method == "GET":
                return redirect(request.path)
            return HttpResponse(status=429)

        if isinstance(exception, ObjectDoesNotExist):
            # Raise a 404 error
            raise Http404

        return None

    def is_non_post_redirect(self, request, response):
        """Check if the response is a redirect for a non-POST request."""
        return self.is_redirect_request(response) and request.method in [
            "PUT",
            "PATCH",
            "DELETE",
        ]

    @staticmethod
    def is_inertia_request(request):
        """Check if the request is an Inertia request."""
        return "X-Inertia" in request.headers

    def is_inertia_get_request(self, request):
        """Check if the request is an Inertia GET request."""
        return request.method == "GET" and self.is_inertia_request(request)

    @staticmethod
    def is_redirect_request(response):
        """Check if the response is a redirect."""
        return response.status_code in [301, 302]

    @staticmethod
    def is_stale(request):
        """Check if the request is stale."""
        return (
            request.headers.get("X-Inertia-Version", settings.INERTIA_VERSION)
            != settings.INERTIA_VERSION
        )

    def is_stale_inertia_get(self, request):
        """Check if the GET request is stale."""
        return request.method == "GET" and self.is_stale(request)

    @staticmethod
    def is_error_response(response):
        """Check if the response is an error response."""
        return response.status_code in [500, 404] and not isinstance(
            response, HttpResponseRedirect
        )

    def force_refresh(self, request):
        """Force a refresh of the page."""
        messages.get_messages(request).used = False
        return HttpResponse(
            "",
            status=409,
            headers={
                "X-Inertia-Location": request.get_full_path(),
            },
        )
