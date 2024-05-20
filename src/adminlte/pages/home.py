"""AdminLTE views."""

import random

from config.svelte.view import InertiaView


class HomePageInertiaView(InertiaView):
    """Home page view."""

    def get_context_data(self, **kwargs):
        """Get context data."""
        return {
            "number": random.randint(1, 100),  # noqa: S311
        }
