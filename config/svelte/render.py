"""Render Inertia pages."""

from collections.abc import Callable
from json import dumps as json_encode

from django.conf import settings
from django.http import HttpRequest as InertiaRequest
from inertia.utils import InertiaJsonEncoder
from inertia.utils import LazyProp

from config.svelte.base_render import base_render
from config.svelte.responses import InertiaJsonResponse


def render(  # noqa: C901
    request: InertiaRequest,
    component: str,
    callback: Callable | None = None,
    props: dict | None = None,
    template_data: dict | None = None,
):
    """Render an Inertia page."""
    # TODO: simplify method
    props = props or {}
    template_data = template_data or {}

    def is_a_partial_render():
        return (
            "X-Inertia-Partial-Data" in request.headers
            and request.headers.get("X-Inertia-Partial-Component", "") == component
        )

    def partial_keys():
        return request.headers.get("X-Inertia-Partial-Data", "").split(",")

    def deep_transform_callables(prop):
        if not isinstance(prop, dict):
            return prop() if callable(prop) else prop

        for key in list(prop.keys()):
            prop[key] = deep_transform_callables(prop[key])

        return prop

    def build_props():
        _props = {
            **(request.inertia.all() if hasattr(request, "inertia") else {}),
            **props,
        }

        for key in list(_props.keys()):
            if is_a_partial_render():
                if key not in partial_keys():
                    del _props[key]
            elif isinstance(_props[key], LazyProp):
                del _props[key]

        return deep_transform_callables(_props)

    def page_data():
        return {
            "component": component,
            "props": build_props(),
            "url": request.get_full_path(),
            "version": settings.INERTIA_VERSION,
        }

    if "X-Inertia" in request.headers:
        return InertiaJsonResponse(
            data=page_data(),
            callback=callback,
            headers={
                "Vary": "Accept",
                "X-Inertia": "true",
            },
            encoder=InertiaJsonEncoder,
        )

    return base_render(
        request=request,
        template_name="inertia.html",
        callback=callback,
        context={
            "inertia_layout": settings.INERTIA_LAYOUT,
            "page": json_encode(page_data(), cls=InertiaJsonEncoder),
            **template_data,
        },
    )
