from django.conf import settings
from django.utils.translation import ugettext_lazy as _

UUID_BACKEND = 'djangocms_moderation.backends.uuid4_backend'
SEQUENTIAL_BACKEND = 'djangocms_moderation.backends.sequential_number_backend'

CORE_REFERENCE_NUMBER_BACKENDS = (
    (UUID_BACKEND, _('Unique alpha-numeric string')),
    (SEQUENTIAL_BACKEND, _('Sequential number'))
)

DEFAULT_REFERENCE_NUMBER_BACKEND = getattr(settings, 'CMS_MODERATION_DEFAULT_REFERENCE_NUMBER_BACKEND', UUID_BACKEND)

REFERENCE_NUMBER_BACKENDS = getattr(settings, 'CMS_MODERATION_REFERENCE_NUMBER_BACKENDS', CORE_REFERENCE_NUMBER_BACKENDS)

ENABLE_WORKFLOW_OVERRIDE = getattr(settings, 'CMS_MODERATION_ENABLE_WORKFLOW_OVERRIDE', False)

DEFAULT_CONFIRMATION_PAGE_TEMPLATE = getattr(settings, 'CMS_MODERATION_DEFAULT_CONFIRMATION_PAGE_TEMPLATE', 'djangocms_moderation/moderation_confirmation.html')

CORE_CONFIRMATION_PAGE_TEMPLATES = (
    (DEFAULT_CONFIRMATION_PAGE_TEMPLATE, _('Default')),
)

CONFIRMATION_PAGE_TEMPLATES = getattr(settings, 'CMS_MODERATION_CONFIRMATION_PAGE_TEMPLATES', CORE_CONFIRMATION_PAGE_TEMPLATES)
