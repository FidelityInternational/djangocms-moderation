from cms.app_base import CMSAppConfig

from .models import TestModel3, TestModel4


class CMSApp1Config(CMSAppConfig):
    django_versioning_enabled = True
    djangocms_moderation_enabled = True
    versioned_moderation_models = [TestModel3, TestModel4]

