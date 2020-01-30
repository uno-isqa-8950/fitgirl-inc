from django.test import TestCase

from cogwheels.helpers import BaseAppSettingsHelper, DeprecatedAppSetting


class TestSettingsHelper(BaseAppSettingsHelper):
    defaults_path = 'cogwheels.tests.conf.defaults'
    prefix = 'TEST_'
    deprecations = ()


class TestHelperInit(TestCase):

    def test_providing_prefix_overrides_the_class_attribute_value(self):
        test_val = 'ABRACADABRA'
        self.assertIs(
            TestSettingsHelper(prefix=test_val)._prefix,
            test_val
        )

    def test_prefix_attribute_never_has_trailing_underscores(self):
        self.assertEqual(TestSettingsHelper()._prefix, 'TEST')
        self.assertEqual(TestSettingsHelper(prefix="ABRACADABRA_")._prefix, 'ABRACADABRA')
        self.assertEqual(TestSettingsHelper(prefix="BEEP_BOOP___")._prefix, 'BEEP_BOOP')

    def test_providing_defaults_path_overrides_the_class_attribute_value(self):
        test_val = 'cogwheels'
        self.assertIs(
            TestSettingsHelper(defaults_path=test_val)._defaults_module_path,
            test_val
        )

    def test_providing_deprecations_overrides_the_class_attribute_value(self):
        test_val = (
            DeprecatedAppSetting('STRING_SETTING'),
        )
        self.assertIs(
            TestSettingsHelper(deprecations=test_val)._deprecations,
            test_val
        )

    def test_raises_import_error_if_defaults_module_cannot_be_imported(self):
        with self.assertRaises(ImportError):
            TestSettingsHelper(defaults_path='invalid.module.path')
