from collections import Iterable
from django.core.exceptions import ImproperlyConfigured
from cms.app_base import CMSAppExtension

from djangocms_versioning.models import BaseVersion


class ModerationExtension(CMSAppExtension):

    def __init__(self):
        self.versioned_moderation_models = []

    def configure_app(self, cms_config):
        versioned_models = getattr(cms_config, 'versioned_moderation_models', [])

        if isinstance(versioned_models, Iterable):
            for versioned_model in versioned_models:
                if issubclass(versioned_model, BaseVersion):
                    self.versioned_moderation_models.append(versioned_model)
                else:
                    raise ImproperlyConfigured(
                "Moderation model must be versionable, it should extend djangocms_versioning.models.BaseVersion")
        
        else:
            raise ImproperlyConfigured(
                "versioned_moderation_models must be a Iterable object")
