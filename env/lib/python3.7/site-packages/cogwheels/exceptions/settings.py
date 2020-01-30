from django.core.exceptions import ImproperlyConfigured

"""Errors relating to a specific setting value"""


# -----------------------------------------------------------------------------
# Common setting value errors
# -----------------------------------------------------------------------------

class SettingValueError(ImproperlyConfigured, ValueError):
    """There is a problem with a setting value."""
    pass


class SettingValueTypeInvalid(SettingValueError):
    """The value of a setting is not the correct type."""
    pass


class SettingValueFormatInvalid(SettingValueError):
    """The value of a setting is the correct type, but is incorrectly
    formatted."""
    pass


class SettingValueNotImportable(ImportError, SettingValueError):
    """The value of a setting is the correct type, and correctly formatted,
    but the specified model, module or object could not be imported.
    """
    pass


# -----------------------------------------------------------------------------
# Errors relating to 'default' values (intended for app developers)
# -----------------------------------------------------------------------------

class DefaultValueError(SettingValueError):
    """A base class for all error classes concerning a 'default' value. Can
    also be used in cases where one of the more specific cases does not quite
    fit, such as a value not passing a custom validation rule."""
    pass


class DefaultValueTypeInvalid(SettingValueTypeInvalid, DefaultValueError):
    """As SettingValueTypeInvalid, but specifically for a 'default' value."""
    pass


class DefaultValueFormatInvalid(SettingValueFormatInvalid, DefaultValueError):
    """As SettingValueFormatInvalid, but specifically for a default value."""
    pass


class DefaultValueNotImportable(SettingValueNotImportable, DefaultValueError):
    """As SettingValueNotImportable, but specifically for a default value."""
    pass


# -----------------------------------------------------------------------------
# Errors relating to 'override' values (intended for app users)
# -----------------------------------------------------------------------------

class OverrideValueError(SettingValueError):
    """A base class for all error classes concerning a 'user-provided' value.
    Can also be used in cases where one of the more specific cases does not
    quite fit, such as a value not passing a custom validation rule."""
    pass


class OverrideValueTypeInvalid(SettingValueTypeInvalid, OverrideValueError):
    """As SettingValueTypeInvalid, but specifically for a 'user-provided' value."""
    pass


class OverrideValueFormatInvalid(SettingValueFormatInvalid, OverrideValueError):
    """As SettingValueFormatInvalid, but specifically for a 'user-provided' value."""
    pass


class OverrideValueNotImportable(SettingValueNotImportable, OverrideValueError):
    """As SettingValueNotImportable, but specifically for a 'user-provided' value."""
    pass
