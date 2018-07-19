from unittest.mock import Mock
from unittest import TestCase

from django.core.exceptions import ImproperlyConfigured

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase

from djangocms_moderation.cms_config import ModerationExtension
from .utils.app_1.models import (
    TestModel3,
    TestModel4,
)
from .utils.app_2.models import (
    TestModel1,
    TestModel2,
)


class AppIntegrationTestCase(CMSTestCase, TestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    def test_missing_versioning_enabled(self):
        extension = ModerationExtension()
        cms_config = Mock(
            djangocms_moderation_enabled=True,
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extension.configure_app(cms_config)

    def test_invalid_moderated_models_type(self):
        extension = ModerationExtension()
        cms_config = Mock(
            djangocms_moderation_enabled=True,
            moderated_models=23234,
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extension.configure_app(cms_config)

    def test_moderated_model_not_in_versioning_models(self):
        extension = ModerationExtension()
        cms_config = Mock(
            djangocms_moderation_enabled=True,
            moderated_models=[TestModel1, TestModel2, TestModel3, TestModel4],
            versioning_models=[TestModel3, TestModel4],
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extension.configure_app(cms_config)

    def test_valid_cms_config(self):
        extension = ModerationExtension()
        cms_config = Mock(
            djangocms_moderation_enabled=True,
            moderated_models=[TestModel1, TestModel2, TestModel3, TestModel4],
            versioning_models=[TestModel1, TestModel2, TestModel3, TestModel4],
            app_config=Mock(label='blah_cms_config')
        )

        extension.configure_app(cms_config)
        self.assertTrue(TestModel1 in extension.moderated_models)
        self.assertTrue(TestModel2 in extension.moderated_models)
        self.assertTrue(TestModel3 in extension.moderated_models)
        self.assertTrue(TestModel4 in extension.moderated_models)
