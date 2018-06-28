from django.conf import settings
from django.utils.translation import ugettext_lazy as _


CORE_REFERENCE_NUMBER_BACKENDS = (
    ('djangocms_moderation.backends.uuid4_backend', _('Unique alpha-numeric string')),
    ('djangocms_moderation.backends.sequential_number_backend', _('Sequential number'))
)

DEFAULT_REFERENCE_NUMBER_BACKEND = getattr(settings, 'CMS_MODERATION_DEFAULT_REFERENCE_NUMBER_BACKEND', CORE_REFERENCE_NUMBER_BACKENDS[0][0])

REFERENCE_NUMBER_BACKENDS = getattr(settings, 'CMS_MODERATION_REFERENCE_NUMBER_BACKENDS', CORE_REFERENCE_NUMBER_BACKENDS)

ENABLE_WORKFLOW_OVERRIDE = getattr(settings, 'CMS_MODERATION_ENABLE_WORKFLOW_OVERRIDE', False)

DEFAULT_CONFIRMATION_PAGE_TEMPLATE = getattr(settings, 'CMS_MODERATION_DEFAULT_CONFIRMATION_PAGE_TEMPLATE', 'djangocms_moderation/moderation_confirmation.html')

CORE_CONFIRMATION_PAGE_TEMPLATES = (
    (DEFAULT_CONFIRMATION_PAGE_TEMPLATE, _('Default')),
)

CONFIRMATION_PAGE_TEMPLATES = getattr(settings, 'CMS_MODERATION_CONFIRMATION_PAGE_TEMPLATES', CORE_CONFIRMATION_PAGE_TEMPLATES)
