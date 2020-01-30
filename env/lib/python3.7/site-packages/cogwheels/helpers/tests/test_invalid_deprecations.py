from django.test import TestCase

from cogwheels import exceptions
from cogwheels.helpers import BaseAppSettingsHelper, DeprecatedAppSetting


class TestSettingsHelper(BaseAppSettingsHelper):
    defaults_path = 'cogwheels.tests.conf.defaults'
    prefix = 'TEST_'
    deprecations = ()


class TestHelperInitErrors(TestCase):

    def test_raises_correct_error_type_if_deprecations_value_is_wrong_type(self):
        with self.assertRaises(exceptions.IncorrectDeprecationsValueType):
            TestSettingsHelper(deprecations={})

    def test_raises_correct_error_type_if_deprecated_value_not_found_in_defaults(self):
        with self.assertRaises(exceptions.InvalidDeprecationDefinition):
            TestSettingsHelper(deprecations=(
                DeprecatedAppSetting('NON_EXISTENT_SETTING'),
            ))

    def test_raises_correct_error_type_if_replacement_value_not_found_in_defaults(self):
        with self.assertRaises(exceptions.InvalidDeprecationDefinition):
            TestSettingsHelper(deprecations=(
                DeprecatedAppSetting(
                    'DEPRECATED_SETTING', renamed_to="NON_EXISTENT_SETTING"
                ),
            ))

    def test_raises_correct_error_type_if_setting_name_repeated_in_deprecation_definitions(self):
        with self.assertRaises(exceptions.DuplicateDeprecationError):
            TestSettingsHelper(deprecations=(
                DeprecatedAppSetting('DEPRECATED_SETTING'),
                DeprecatedAppSetting('DEPRECATED_SETTING'),
            ))
