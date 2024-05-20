"""Base inertia view."""

import abc
import logging

from django.urls import resolve
from django.views import View
from inertia import lazy

from config.svelte.middleware import InertiaRequest
from config.svelte.render import render

logger = logging.getLogger(__name__)


class InertiaView(View):
    """Inertia view."""

    component: str = ""

    def get_component_name(self):
        """Get component name."""
        # return component name if defined
        if self.component:
            return self.component

        # else compose component name as "{app_name}:{view_file_name}"
        return f"{self.__module__.split('.')[1]}:{resolve(self.request.path_info).url_name}"  # noqa: E501

    @abc.abstractmethod
    def get_context_data(self, **kwargs):
        """Get context data."""
        raise NotImplementedError

    def get_initial_context(self, **kwargs):
        """Get initial context."""
        return {
            "user": self.get_user_data(**kwargs),
        }

    def get_user_data(self, **kwargs):
        """Get user data."""
        # TODO: return lambda: self.request.user
        return

    @staticmethod
    def get_template_data(**kwargs):
        """Get template data."""
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
            props.update(self.get_initial_context(**kwargs))

        # render response
        return render(
            request=request,
            component=self.get_component_name(),
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
