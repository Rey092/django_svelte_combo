"""Inertia validation helpers."""

from django.forms import Form
from django.forms import ModelForm
from django.forms.utils import ErrorDict
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect

VALIDATION_ERRORS_SESSION_KEY = "_inertia_validation_errors"

InertiaRedirect = HttpResponseRedirect | HttpResponsePermanentRedirect


class InertiaValidationError(Exception):
    """Exception raised when form validation fails."""

    def __init__(self, errors: ErrorDict, redirect: InertiaRedirect):
        """Initialize the exception."""
        super().__init__()
        self.redirect = redirect
        self.errors = errors


def inertia_validate(form: Form | ModelForm, redirect: InertiaRedirect):
    """Validate a form and raise an InertiaValidationError if invalid."""
    if not form.is_valid():
        raise InertiaValidationError(form.errors, redirect)

    return form.cleaned_data
