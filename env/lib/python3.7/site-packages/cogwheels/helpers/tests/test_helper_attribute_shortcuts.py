from unittest.mock import patch

from cogwheels.helpers import BaseAppSettingsHelper
from cogwheels.tests.base import AppSettingTestCase


class TestModelsShortcut(AppSettingTestCase):
    """
    Each settings helper instance has a 'models' attribute, which allows
    developers to retrieve Django model classes referenced by setting values
    as attributes, rather than passing the setting name as a string to the
    'get_model()' method.

    The 'get_model()' method is already well tested, so all we want to show
    is that attribute requests are always passed on to that method (unless we
    know there is no such setting).
    """
    @patch.object(BaseAppSettingsHelper, 'get_model')
    def test_raises_attributeerror_if_no_default_defined(self, mocked_method):
        expected_message = (
            "TestAppSettingsHelper object has no attribute 'I_DONT_THINK_SO'")
        with self.assertRaisesRegex(AttributeError, expected_message):
            self.appsettingshelper.models.I_DONT_THINK_SO
        mocked_method.assert_not_called()

    @patch.object(BaseAppSettingsHelper, 'get_model')
    def test_with_valid_object_setting(self, mocked_method):
        self.appsettingshelper.models.VALID_MODEL
        mocked_method.assert_called_with('VALID_MODEL', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_model')
    def test_with_invalid_object_setting(self, mocked_method):
        self.appsettingshelper.models.MODULE_UNAVAILABLE_OBJECT
        mocked_method.assert_called_with('MODULE_UNAVAILABLE_OBJECT', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_model')
    def test_with_completely_different_types_of_setting(self, mocked_method):
        self.appsettingshelper.models.INTEGER_SETTING
        mocked_method.assert_called_with('INTEGER_SETTING', warning_stacklevel=5)
        self.appsettingshelper.models.TUPLES_SETTING
        mocked_method.assert_called_with('TUPLES_SETTING', warning_stacklevel=5)


class TestModulesShortcut(AppSettingTestCase):
    """
    Each settings helper instance has a 'modules' attribute, which allows
    developers to easily retrieve Python modules referenced by setting
    values as attributes, instead of having to pass the setting name as a
    string to the 'get_model()' method.

    The 'get_modules()' method is already well tested, so all we want to show
    is that attribute requests are always passed on to that method (unless we
    know there is no such setting).
    """
    @patch.object(BaseAppSettingsHelper, 'get_module')
    def test_raises_attributeerror_if_no_default_defined(self, mocked_method):
        expected_message = (
            "TestAppSettingsHelper object has no attribute "
            "'I_DONT_THINK_SO'")
        with self.assertRaisesRegex(AttributeError, expected_message):
            self.appsettingshelper.modules.I_DONT_THINK_SO
        mocked_method.assert_not_called()

    @patch.object(BaseAppSettingsHelper, 'get_module')
    def test_with_valid_object_setting(self, mocked_method):
        self.appsettingshelper.modules.VALID_MODULE
        mocked_method.assert_called_with('VALID_MODULE', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_module')
    def test_with_invalid_object_setting(self, mocked_method):
        self.appsettingshelper.modules.MODULE_UNAVAILABLE_OBJECT
        mocked_method.assert_called_with('MODULE_UNAVAILABLE_OBJECT', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_module')
    def test_with_completely_different_types_of_setting(self, mocked_method):
        self.appsettingshelper.modules.INTEGER_SETTING
        mocked_method.assert_called_with('INTEGER_SETTING', warning_stacklevel=5)
        self.appsettingshelper.modules.TUPLES_SETTING
        mocked_method.assert_called_with('TUPLES_SETTING', warning_stacklevel=5)


class TestObjectsShortcut(AppSettingTestCase):
    """
    Each settings helper instance has a 'objects' attribute, which allows
    developers to access 'python objects' as attributes, instead of having to
    pass the setting name as a string to the 'get_object()' method.

    The 'get_object()' method is already well tested, so all we want to show
    is that request are always passed on to that method, unless there is no
    default value defined
    """
    @patch.object(BaseAppSettingsHelper, 'get_object')
    def test_raises_attributeerror_if_no_default_defined(self, mocked_method):
        expected_message = (
            "TestAppSettingsHelper object has no attribute "
            "'I_DONT_THINK_SO'")
        with self.assertRaisesRegex(AttributeError, expected_message):
            self.appsettingshelper.objects.I_DONT_THINK_SO
        mocked_method.assert_not_called()

    @patch.object(BaseAppSettingsHelper, 'get_object')
    def test_with_valid_object_setting(self, mocked_method):
        self.appsettingshelper.objects.VALID_OBJECT
        mocked_method.assert_called_with('VALID_OBJECT', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_object')
    def test_with_invalid_object_setting(self, mocked_method):
        self.appsettingshelper.objects.MODULE_UNAVAILABLE_OBJECT
        mocked_method.assert_called_with('MODULE_UNAVAILABLE_OBJECT', warning_stacklevel=5)

    @patch.object(BaseAppSettingsHelper, 'get_object')
    def test_with_completely_different_types_of_setting(self, mocked_method):
        self.appsettingshelper.objects.INTEGER_SETTING
        mocked_method.assert_called_with('INTEGER_SETTING', warning_stacklevel=5)
        self.appsettingshelper.objects.TUPLES_SETTING
        mocked_method.assert_called_with('TUPLES_SETTING', warning_stacklevel=5)
