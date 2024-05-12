"""Base inertia view."""

import logging

# TODO: from base.inertia.middleware import InertiaRequest
from django.http import HttpRequest as InertiaRequest
from django.views import View
from inertia import lazy

from config.svelte.render import render

logger = logging.getLogger(__name__)


class InertiaView(View):
    """Inertia view."""

    component: str = ""

    @staticmethod
    def get_context_data(**kwargs):
        """Get context data."""
        raise NotImplementedError

    def get_user_context(self, **kwargs):
        """Get user context."""
        return {
            "user": self.get_user_data(**kwargs),
        }

    @staticmethod
    def get_user_data(self, **kwargs):
        """Get user data."""
        # TODO: return lambda: self.request.user
        return

    @staticmethod
    def get_template_data(**kwargs):
        """Get template data."""
        return {}

    @staticmethod
    def get_metadata(**kwargs):
        """Get metadata."""
        return {}

    def callback(self, request: InertiaRequest):
        """Run callback function to be called after render."""

    def get(self, request: InertiaRequest, *args, **kwargs):
        """Get render of either Inertia page or json response."""
        # define props
        props: dict = {}

        # get context data
        props.update(self.get_context_data(**kwargs))

        # if request is not inertia, add initial context data
        if not request.inertia_details.is_inertia_request:
            props.update(self.get_user_context(**kwargs))

        # render response
        return render(
            request=request,
            component=self.component,
            callback=lazy(lambda: self.callback(request=request)),
            props=props,
            template_data=self.get_template_data(**kwargs),
        )

    # noinspection PyAttributeOutsideInit
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request: InertiaRequest = request
        self.args = args
        self.kwargs = kwargs
