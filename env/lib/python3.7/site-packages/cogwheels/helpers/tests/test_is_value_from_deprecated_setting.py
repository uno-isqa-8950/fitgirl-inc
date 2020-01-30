from django.test import override_settings

from cogwheels.tests.base import AppSettingTestCase


class TestIsValueFromDeprecatedSetting(AppSettingTestCase):
    """
    Unit tests for BaseAppSettingsHelper.is_value_from_deprecated_setting()
    """

    def test_returns_false_when_neither_setting_is_overridden(self):
        for new_name, deprecated_name in (
            ('RENAMED_SETTING_NEW', 'RENAMED_SETTING_OLD'),
            ('REPLACEMENT_SETTING', 'REPLACED_SETTING'),
            ('REPLACES_MULTIPLE', 'REPLACED_SETTING_THREE'),
        ):
            self.assertIs(
                self.appsettingshelper.is_value_from_deprecated_setting(new_name, deprecated_name),
                False
            )

    @override_settings(
        COGWHEELS_TESTS_RENAMED_SETTING_NEW='new',
        COGWHEELS_TESTS_REPLACEMENT_SETTING='new',
        COGWHEELS_TESTS_REPLACES_MULTIPLE='new'
    )
    def test_returns_false_if_just_the_new_setting_is_overridden(self):
        for new_name, deprecated_name in (
            ('RENAMED_SETTING_NEW', 'RENAMED_SETTING_OLD'),
            ('REPLACEMENT_SETTING', 'REPLACED_SETTING'),
            ('REPLACES_MULTIPLE', 'REPLACED_SETTING_THREE'),
        ):
            self.assertIs(
                self.appsettingshelper.is_value_from_deprecated_setting(new_name, deprecated_name),
                False,
            )

    @override_settings(
        COGWHEELS_TESTS_RENAMED_SETTING_NEW='new',
        COGWHEELS_TESTS_RENAMED_SETTING_OLD='old',
        COGWHEELS_TESTS_REPLACEMENT_SETTING='new',
        COGWHEELS_TESTS_REPLACED_SETTING='old',
        COGWHEELS_TESTS_REPLACES_MULTIPLE='new',
        COGWHEELS_TESTS_REPLACED_SETTING_THREE='old',
    )
    def test_returns_false_if_both_new_and_old_settings_are_overridden(self):
        for new_name, deprecated_name in (
            ('RENAMED_SETTING_NEW', 'RENAMED_SETTING_OLD'),
            ('REPLACEMENT_SETTING', 'REPLACED_SETTING'),
            ('REPLACES_MULTIPLE', 'REPLACED_SETTING_THREE'),
        ):
            self.assertIs(
                self.appsettingshelper.is_value_from_deprecated_setting(new_name, deprecated_name),
                False,
            )

    @override_settings(
        COGWHEELS_TESTS_RENAMED_SETTING_OLD='somevalue',
        COGWHEELS_TESTS_REPLACED_SETTING='someothervalue',
        COGWHEELS_TESTS_REPLACED_SETTING_THREE='anothervalue',
    )
    def test_returns_true_if_just_the_old_setting_is_overridden(self):
        for new_name, deprecated_name in (
            ('RENAMED_SETTING_NEW', 'RENAMED_SETTING_OLD'),
            ('REPLACEMENT_SETTING', 'REPLACED_SETTING'),
            ('REPLACES_MULTIPLE', 'REPLACED_SETTING_THREE'),
        ):
            self.assertIs(
                self.appsettingshelper.is_value_from_deprecated_setting(new_name, deprecated_name),
                True,
            )

    @override_settings(COGWHEELS_TESTS_REPLACED_SETTING_ONE='somevalue')
    def test_returns_expected_value_for_a_multiple_setting_replacement(self):
        self.assertIs(
            self.appsettingshelper.is_value_from_deprecated_setting('REPLACES_MULTIPLE', 'REPLACED_SETTING_ONE'),
            True
        )
        self.assertIs(
            self.appsettingshelper.is_value_from_deprecated_setting('REPLACES_MULTIPLE', 'REPLACED_SETTING_TWO'),
            False
        )
        self.assertIs(
            self.appsettingshelper.is_value_from_deprecated_setting('REPLACES_MULTIPLE', 'REPLACED_SETTING_THREE'),
            False
        )

    def test_raises_valueerror_if_unknown_setting_name_supplied(self):
        with self.assertRaisesRegex(ValueError, "'NOT_IN_DEFAULTS' is not a valid setting name"):
            self.appsettingshelper.is_value_from_deprecated_setting('NOT_IN_DEFAULTS', 'REPLACED_SETTING_ONE')

    def test_raises_valueerror_if_unknown_deprecated_setting_name_supplied(self):
        with self.assertRaisesRegex(ValueError, "'NOT_IN_DEFAULTS' is not a valid setting name"):
            self.appsettingshelper.is_value_from_deprecated_setting('REPLACES_MULTIPLE', 'NOT_IN_DEFAULTS')

    def test_raises_valueerror_if_the_deprecated_setting_name_setting_is_not_deprecated(self):
        with self.assertRaisesRegex(ValueError, "The 'REPLACES_MULTIPLE' setting is not deprecated"):
            self.appsettingshelper.is_value_from_deprecated_setting('REPLACED_SETTING_ONE', 'REPLACES_MULTIPLE')
