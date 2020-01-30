from django.core.exceptions import ImproperlyConfigured

# -----------------------------------------------------------------------------
# Errors relating to a settings heleper's 'deprecation' value
# -----------------------------------------------------------------------------


class DeprecationsError(ImproperlyConfigured):
    """There is a problem with a settings helper's 'deprecations' value."""
    pass


class IncorrectDeprecationsValueType(DeprecationsError):
    """The 'deprecations' value is not a list or tuple."""


class InvalidDeprecationDefinition(DeprecationsError):
    """There is a problem with a one or more AppSettingDeprecation definitions
    in a settings helper's 'deprecations' list."""
    pass


class DuplicateDeprecationError(InvalidDeprecationDefinition):
    """The same setting name has been used for more than one
    AppSettingDeprecation definitions in a setting helper's 'deprecations' "
    "list."""
    pass
