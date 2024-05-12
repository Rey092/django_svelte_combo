"""Base render function for Inertia responses."""

from collections.abc import Callable

# TODO: from base.inertia.middleware import InertiaRequest
from django.http import HttpRequest as InertiaRequest
from django.template import loader

from config.svelte.responses import InertiaHttpResponse


#  TODO: Simplify method.
def base_render(  # noqa: PLR0913
    request: InertiaRequest,
    template_name: str,
    callback: Callable | None = None,
    context=None,
    content_type=None,
    status=None,
    using=None,
):
    """Return an HttpResponse whose content is filled with the result.

    Result of django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return InertiaHttpResponse(
        data=content, callback=callback, content_type=content_type, status=status
    )
