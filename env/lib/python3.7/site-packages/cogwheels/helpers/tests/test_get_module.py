import warnings
from unittest.mock import patch
from django.test import override_settings

from cogwheels import exceptions
from cogwheels.tests.conf import settings
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.modules import default_module, replacement_module


class TestValidModuleSettingOverride(AppSettingTestCase):
    """
    Tests the effect of overriding ``COGWHEELS_TESTS_VALID_MODULE``
    """
    def test_returns_default_module_by_default(self):
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), default_module,
        )

    @patch.object(settings, '_do_import')
    def test_returns_from_cache_after_first_import(self, mocked_method):
        settings.reset_caches()
        settings.get_module('VALID_MODULE')
        settings.get_module('VALID_MODULE')
        settings.get_module('VALID_MODULE')
        self.assertEqual(mocked_method.call_count, 1)

    @override_settings(COGWHEELS_TESTS_VALID_MODULE='cogwheels.tests.modules.replacement_module')
    def test_successful_override(self):
        self.assertIs(
            self.appsettingshelper.get_module('VALID_MODULE'), replacement_module
        )

    @override_settings(COGWHEELS_TESTS_VALID_MODULE=1)
    def test_raises_correct_error_type_when_value_is_not_a_string(self):
        with self.assertRaises(exceptions.OverrideValueTypeInvalid):
            self.appsettingshelper.get_module('VALID_MODULE')

    @override_settings(COGWHEELS_TESTS_VALID_MODULE='project.app.module')
    def test_raises_correct_error_type_when_module_not_importable(self):
        with self.assertRaises(exceptions.OverrideValueNotImportable):
            self.appsettingshelper.get_module('VALID_MODULE')


class TestInvalidDefaultModuleSettings(AppSettingTestCase):
    """
    Tests what happens when an app setting (which is supposed to be a valid
    python import path) is referenced, but the default value provided by the
    app developer is invalid.
    """

    def test_raises_correct_error_type_when_module_unavailable(self):
        with self.assertRaises(exceptions.DefaultValueNotImportable):
            self.appsettingshelper.get_module('UNAVAILABLE_MODULE')


class TestReplacedModuleSetting(AppSettingTestCase):

    @override_settings(COGWHEELS_TESTS_REPLACED_MODULE_SETTING='cogwheels.tests.modules.replacement_module')
    def test_referencing_deprecated_setting_returns_correct_value_but_a_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_module('REPLACED_MODULE_SETTING'),
                replacement_module,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The REPLACED_MODULE_SETTING app setting is deprecated in favour of using "
                "REPLACEMENT_MODULE_SETTING. Please update your code to reference the new setting, "
                "as continuing to reference REPLACED_MODULE_SETTING will cause an exception to be "
                "raised once support is removed in two versions time.",
                str(w[0])
            )

    def test_multiple_references_to_deprecated_setting_raises_a_warning_each_time(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get_module('REPLACED_MODULE_SETTING')
            self.appsettingshelper.get_module('REPLACED_MODULE_SETTING')
            self.appsettingshelper.get_module('REPLACED_MODULE_SETTING')
            self.assertEqual(len(w), 3)

    def test_no_warnings_raised_by_replacement_setting_by_default(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_module('REPLACEMENT_MODULE_SETTING'),
                default_module,
            )
            self.assertEqual(len(w), 0)

    @override_settings(COGWHEELS_TESTS_REPLACED_MODULE_SETTING='cogwheels.tests.modules.replacement_module')
    def test_single_warning_raised_by_replacement_setting_when_deprecated_setting_value_used(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIs(
                self.appsettingshelper.get_module('REPLACEMENT_MODULE_SETTING'),
                replacement_module,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The COGWHEELS_TESTS_REPLACED_MODULE_SETTING setting is deprecated in favour of "
                "using COGWHEELS_TESTS_REPLACEMENT_MODULE_SETTING. Please update your Django "
                "settings to use the new setting, otherwise the app will revert to it's default "
                "behaviour once support for COGWHEELS_TESTS_REPLACED_MODULE_SETTING is removed in "
                "two versions time.",
                str(w[0])
            )

    @override_settings(COGWHEELS_TESTS_REPLACED_MODEL_SETTING='cogwheels.tests.modules.replacement_module')
    def test_using_suppress_warnings_has_the_desired_effect(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get_module('REPLACED_MODULE_SETTING', suppress_warnings=True)
            self.appsettingshelper.get_module('REPLACEMENT_MODULE_SETTING', suppress_warnings=True)
            self.assertEqual(len(w), 0)
