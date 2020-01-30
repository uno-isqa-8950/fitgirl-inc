import warnings
from unittest.mock import patch

from django.test import override_settings

from cogwheels import exceptions
from cogwheels.tests.conf import settings
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.classes import DefaultClass, ReplacementClass


class TestValidObjectSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``COGWHEELS_TESTS_VALID_OBJECT``
    """
    def test_returns_default_class_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_object('VALID_OBJECT'), DefaultClass,
        )

    @patch.object(settings, '_do_import')
    def test_returns_from_cache_after_first_import(self, mocked_method):
        settings.reset_caches()
        settings.get_object('VALID_OBJECT')
        settings.get_object('VALID_OBJECT')
        settings.get_object('VALID_OBJECT')
        self.assertEqual(mocked_method.call_count, 1)

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='cogwheels.tests.classes.ReplacementClass')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_object('VALID_OBJECT'), ReplacementClass
        )

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT=1)
    def test_raises_correct_error_type_when_value_is_not_a_string(self):
        with self.assertRaises(exceptions.OverrideValueTypeInvalid):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='no_dots_here')
    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.OverrideValueFormatInvalid):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='project.app.module.Class')
    def test_raises_correct_error_type_when_module_not_found(self):
        with self.assertRaises(exceptions.OverrideValueNotImportable):
            self.appsettingshelper.get_object('VALID_OBJECT')

    @override_settings(COGWHEELS_TESTS_VALID_OBJECT='cogwheels.tests.classes.NonExistentClass')
    def test_raises_correct_error_type_when_object_not_found(self):
        with self.assertRaises(exceptions.OverrideValueNotImportable):
            self.appsettingshelper.get_object('VALID_OBJECT')


class TestInvalidDefaultObjectSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_correct_error_type_when_format_is_invalid(self):
        with self.assertRaises(exceptions.DefaultValueFormatInvalid):
            self.appsettingshelper.get_object('INCORRECT_FORMAT_OBJECT')

    def test_raises_correct_error_type_when_module_not_found(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_object('MODULE_UNAVAILABLE_OBJECT')

    def test_raises_correct_error_type_when_object_not_found(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_object('OBJECT_UNAVAILABLE_OBJECT')


class TestReplacedObjectSetting(AppSettingTestCase):

    @override_settings(COGWHEELS_TESTS_REPLACED_OBJECT_SETTING='cogwheels.tests.classes.ReplacementClass')
    def test_referencing_deprecated_setting_returns_correct_value_but_a_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING'),
                ReplacementClass,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The REPLACED_OBJECT_SETTING app setting is deprecated in favour of using "
                "REPLACEMENT_OBJECT_SETTING. Please update your code to reference the new setting, "
                "as continuing to reference REPLACED_OBJECT_SETTING will cause an exception to be "
                "raised once support is removed in two versions time.",
                str(w[0])
            )

    def test_multiple_references_to_deprecated_setting_raises_a_warning_each_time(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING')
            self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING')
            self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING')
            self.assertEqual(len(w), 3)

    def test_no_warnings_raised_by_replacement_setting_by_default(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_object('REPLACEMENT_OBJECT_SETTING'),
                DefaultClass,
            )
            self.assertEqual(len(w), 0)

    @override_settings(COGWHEELS_TESTS_REPLACED_OBJECT_SETTING='cogwheels.tests.classes.ReplacementClass')
    def test_single_warning_raised_by_replacement_setting_when_deprecated_setting_value_used(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_object('REPLACEMENT_OBJECT_SETTING'),
                ReplacementClass,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The COGWHEELS_TESTS_REPLACED_OBJECT_SETTING setting is deprecated in favour of "
                "using COGWHEELS_TESTS_REPLACEMENT_OBJECT_SETTING. Please update your Django "
                "settings to use the new setting, otherwise the app will revert to it's default "
                "behaviour once support for COGWHEELS_TESTS_REPLACED_OBJECT_SETTING is removed in "
                "two versions time.",
                str(w[0])
            )

    @override_settings(COGWHEELS_TESTS_REPLACED_MODEL_SETTING='cogwheels.tests.classes.ReplacementClass')
    def test_using_suppress_warnings_has_the_desired_effect(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING', suppress_warnings=True)
            self.appsettingshelper.get_object('REPLACEMENT_OBJECT_SETTING', suppress_warnings=True)
            self.assertEqual(len(w), 0)
