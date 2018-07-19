from cms.app_base import CMSAppConfig

from .models import TestModel1, TestModel2


class CMSApp2Config(CMSAppConfig):
    django_versioning_enabled = True
    djangocms_moderation_enabled = True
    versioned_moderation_models = [TestModel1, TestModel2]

