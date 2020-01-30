import warnings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from cogwheels import DefaultValueTypeInvalid
from cogwheels.tests.base import AppSettingTestCase
from cogwheels.tests.conf import defaults


class TestGetMethod(AppSettingTestCase):

    def test_raises_error_if_no_default_defined(self):
        with self.assertRaises(ImproperlyConfigured):
            self.appsettingshelper.get('NOT_REAL_SETTING')

    def test_integer_setting_returns_default_value_by_default(self):
        self.assertEqual(
            self.appsettingshelper.get('INTEGER_SETTING'),
            defaults.INTEGER_SETTING
        )

    @override_settings(COGWHEELS_TESTS_INTEGER_SETTING=1234)
    def test_integer_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('INTEGER_SETTING')
        self.assertNotEqual(result, defaults.INTEGER_SETTING)
        self.assertEqual(result, 1234)

    def test_str_type_enforcement_raises_error(self):
        with self.assertRaises(DefaultValueTypeInvalid):
            self.appsettingshelper.get('INTEGER_SETTING', enforce_type=str)

    def test_multiple_type_enforcement_raises_error(self):
        with self.assertRaises(DefaultValueTypeInvalid):
            self.appsettingshelper.get('INTEGER_SETTING', enforce_type=(str, list, float))

    def test_multiple_type_enforcement_does_not_raise_error_if_one_type_matches(self):
        self.appsettingshelper.get('INTEGER_SETTING', enforce_type=(str, list, int))

    def test_boolean_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('BOOLEAN_SETTING'),
            defaults.BOOLEAN_SETTING
        )

    @override_settings(COGWHEELS_TESTS_BOOLEAN_SETTING=True)
    def test_boolean_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('BOOLEAN_SETTING')
        self.assertNotEqual(result, defaults.BOOLEAN_SETTING)
        self.assertIs(result, True)

    def test_string_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('STRING_SETTING'),
            defaults.STRING_SETTING
        )

    @override_settings(COGWHEELS_TESTS_STRING_SETTING='abc')
    def test_string_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('STRING_SETTING')
        self.assertNotEqual(result, defaults.STRING_SETTING)
        self.assertIs(result, 'abc')

    def test_tuples_setting_returns_default_value_by_default(self):
        self.assertIs(
            self.appsettingshelper.get('TUPLES_SETTING'),
            defaults.TUPLES_SETTING
        )

    @override_settings(COGWHEELS_TESTS_TUPLES_SETTING=())
    def test_tuples_setting_returns_user_defined_value_if_overridden(self):
        result = self.appsettingshelper.get('TUPLES_SETTING')
        self.assertNotEqual(result, defaults.TUPLES_SETTING)
        self.assertIs(result, ())


class TestDeprecatedSetting(AppSettingTestCase):

    def test_referencing_deprecated_setting_returns_a_value_but_raises_a_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(
                self.appsettingshelper.get('DEPRECATED_SETTING'),
                defaults.DEPRECATED_SETTING,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The DEPRECATED_SETTING app setting is deprecated. Please remove any references to "
                "it from your project, as continuing to reference it will cause an exception to be "
                "raised once support is removed in the next version.",
                str(w[0])
            )

    def test_multiple_references_to_deprecated_setting_raises_a_warning_each_time(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('DEPRECATED_SETTING')
            self.appsettingshelper.get('DEPRECATED_SETTING')
            self.appsettingshelper.get('DEPRECATED_SETTING')
            self.assertEqual(len(w), 3)


class TestRenamedSetting(AppSettingTestCase):

    def test_referencing_deprecated_setting_returns_a_value_but_raises_a_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(
                self.appsettingshelper.get('RENAMED_SETTING_OLD'),
                defaults.RENAMED_SETTING_OLD,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The RENAMED_SETTING_OLD app setting has been renamed to RENAMED_SETTING_NEW. "
                "Please update your code to reference the new setting, as continuing to reference "
                "RENAMED_SETTING_OLD will cause an exception to be raised once support is removed "
                "in the next version.",
                str(w[0])
            )

    def test_multiple_references_to_deprecated_setting_raises_a_warning_each_time(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('RENAMED_SETTING_OLD')
            self.appsettingshelper.get('RENAMED_SETTING_OLD')
            self.appsettingshelper.get('RENAMED_SETTING_OLD')
            self.assertEqual(len(w), 3)

    @override_settings(COGWHEELS_TESTS_RENAMED_SETTING_OLD='ooolaalaa')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        with self.assertWarns(DeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.get('RENAMED_SETTING_NEW'),
                'ooolaalaa'
            )
        self.assertIn(
            "The COGWHEELS_TESTS_RENAMED_SETTING_OLD setting has been renamed to "
            "COGWHEELS_TESTS_RENAMED_SETTING_NEW. Please update your Django settings to use the "
            "new setting, otherwise the app will revert to it's default behaviour once support for "
            "COGWHEELS_TESTS_RENAMED_SETTING_OLD is removed in the next version.",
            str(cm.warning)
        )


class TestReplacedSetting(AppSettingTestCase):

    def test_referencing_deprecated_setting_returns_a_value_but_raises_a_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(
                self.appsettingshelper.get('REPLACED_SETTING'),
                defaults.REPLACED_SETTING,
            )
            self.assertEqual(len(w), 1)
            self.assertIn(
                "The REPLACED_SETTING app setting is deprecated in favour of using "
                "REPLACEMENT_SETTING. Please update your code to reference the new setting, as "
                "continuing to reference REPLACED_SETTING will cause an exception to be raised "
                "once support is removed in two versions time.",
                str(w[0])
            )
            # The additional guidance should be present also
            self.assertIn(
                self.appsettingshelper.COMPLEX_REPLACEMENT_GUIDANCE,
                str(w[0])
            )

    def test_multiple_references_to_deprecated_setting_raises_a_warning_each_time(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('REPLACED_SETTING')
            self.appsettingshelper.get('REPLACED_SETTING')
            self.appsettingshelper.get('REPLACED_SETTING')
            self.assertEqual(len(w), 3)

    @override_settings(COGWHEELS_TESTS_REPLACED_SETTING='boom!')
    def test_user_defined_setting_with_old_name_still_used_when_new_setting_referenced(self):
        with self.assertWarns(PendingDeprecationWarning) as cm:
            self.assertEqual(
                self.appsettingshelper.get('REPLACEMENT_SETTING'), 'boom!'
            )
        self.assertIn(
            "The COGWHEELS_TESTS_REPLACED_SETTING setting is deprecated in favour of using "
            "COGWHEELS_TESTS_REPLACEMENT_SETTING. Please update your Django settings to use the "
            "new setting, otherwise the app will revert to it's default behaviour once support for "
            "COGWHEELS_TESTS_REPLACED_SETTING is removed in two versions time.",
            str(cm.warning)
        )
        # The additional guidance should be present also
        self.assertIn(
            self.appsettingshelper.COMPLEX_REPLACEMENT_GUIDANCE,
            str(cm.warning)
        )

    @override_settings(COGWHEELS_TESTS_REPLACED_SETTING='boom!')
    def test_using_suppress_warnings_has_the_desired_effect(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.appsettingshelper.get('REPLACED_SETTING', suppress_warnings=True)
            self.appsettingshelper.get('REPLACEMENT_SETTING', suppress_warnings=True)
            self.assertEqual(len(w), 0)


@override_settings(
    COGWHEELS_TESTS_REPLACED_SETTING_ONE='overridden-one',
    COGWHEELS_TESTS_REPLACED_SETTING_TWO='overridden-two',
)
class TestMultipleReplacementSetting(AppSettingTestCase):

    def test_referencing_each_old_setting_on_settings_module_raises_warning(self):
        for deprecated_setting_name in (
            'REPLACED_SETTING_ONE', 'REPLACED_SETTING_TWO', 'REPLACED_SETTING_THREE'
        ):
            with self.assertWarns(DeprecationWarning):
                self.appsettingshelper.get(deprecated_setting_name)

    def test_user_defined_setting_with_old_name_is_only_used_if_its_name_matches_accept_deprecated(self):
        # REPLACES_MULTIPLE should return the value from defaults, because a user could be
        # overriding any one of the deprecated settings being replaced, and because we have no idea
        # which to prioritize over the other, picking one could yield unpredictable results.
        self.assertIs(
            self.appsettingshelper.get('REPLACES_MULTIPLE'), defaults.REPLACES_MULTIPLE
        )
        # Instead, developers can specify which deprecated setting in particular they are willing to
        # use a value from, and override values for those settings will be returned.
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(
                self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_ONE'),
                'overridden-one'
            )

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(
                self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_TWO'),
                'overridden-two'
            )
        # But the the default value will still be returned if the specified deprecated setting has
        # not been overridden
        self.assertIs(
            self.appsettingshelper.get('REPLACES_MULTIPLE', accept_deprecated='REPLACED_SETTING_THREE'),
            defaults.REPLACES_MULTIPLE
        )
