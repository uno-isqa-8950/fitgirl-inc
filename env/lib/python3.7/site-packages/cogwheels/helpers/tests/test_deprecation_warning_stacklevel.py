import warnings
from django.test import override_settings

from cogwheels.tests.base import AppSettingTestCase


class TestDeprecationWarningStackLevelSetting(AppSettingTestCase):

    def assert_this_file_appears_as_cause_of_warning(self, warning):
        self.assertIn(
            '/cogwheels/helpers/tests/test_deprecation_warning_stacklevel.py',
            str(warning)
        )

    def test_raise_all_deprecated_setting_reference_warnings(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('DEPRECATED_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_model('REPLACED_MODEL_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.models.REPLACED_MODEL_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_module('REPLACED_MODULE_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.modules.REPLACED_MODULE_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_object('REPLACED_OBJECT_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.objects.REPLACED_OBJECT_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

    @override_settings(
        COGWHEELS_TESTS_RENAMED_SETTING_OLD='ooolaalaa',
        COGWHEELS_TESTS_REPLACED_MODEL_SETTING='tests.ReplacementModel',
        COGWHEELS_TESTS_REPLACED_MODULE_SETTING='cogwheels.tests.modules.replacement_module',
        COGWHEELS_TESTS_REPLACED_OBJECT_SETTING='cogwheels.tests.classes.ReplacementClass'
    )
    def test_raise_all_deprecated_setting_value_used_by_replacement_warnings(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('RENAMED_SETTING_NEW')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_model('REPLACEMENT_MODEL_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_module('REPLACEMENT_MODULE_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.get_object('REPLACEMENT_OBJECT_SETTING')
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

    @override_settings(
        COGWHEELS_TESTS_RENAMED_SETTING_OLD='ooolaalaa',
        COGWHEELS_TESTS_REPLACED_MODEL_SETTING='tests.ReplacementModel',
        COGWHEELS_TESTS_REPLACED_MODULE_SETTING='cogwheels.tests.modules.replacement_module',
        COGWHEELS_TESTS_REPLACED_OBJECT_SETTING='cogwheels.tests.classes.ReplacementClass'
    )
    def test_raise_all_deprecated_setting_value_used_by_replacement_warnings_via_attribute_shortcuts(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.RENAMED_SETTING_NEW
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.models.REPLACEMENT_MODEL_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.modules.REPLACEMENT_MODULE_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())

            self.appsettingshelper.objects.REPLACEMENT_OBJECT_SETTING
            self.assert_this_file_appears_as_cause_of_warning(w.pop())
