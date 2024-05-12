"""Inertia HTTP response class."""

from django.http import HttpResponse
from django.http import JsonResponse


class InertiaResponseCallbackMixin:
    """Mixin for InertiaResponse.

    Adds a callback to be called after the response is sent.
    """

    def __init__(self, data, callback, **kwargs):
        """Initialize the mixin."""
        super().__init__(data, **kwargs)
        self.callback = callback

    def close(self):
        """Close the response and call the callback."""
        super().close()
        if self.callback:
            self.callback()


class InertiaHttpResponse(InertiaResponseCallbackMixin, HttpResponse):
    """An HTTP response class."""


class InertiaJsonResponse(InertiaResponseCallbackMixin, JsonResponse):
    """An HTTP response class that consumes data to be serialized to JSON."""
