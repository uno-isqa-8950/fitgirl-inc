import warnings


COMMON_REQUESTED_WARNING_FORMAT = (
    "Please update your code to reference the new setting, as continuing to "
    "reference {setting_name} will cause an exception to be raised once support "
    "is removed in {removed_in_version}."
)
RENAMED_SETTING_REQUESTED_WARNING_FORMAT = (
    "The {setting_name} app setting has been renamed to {replacement_name}. "
) + COMMON_REQUESTED_WARNING_FORMAT

REPLACED_SETTING_REQUESTED_WARNING_FORMAT = (
    "The {setting_name} app setting is deprecated in favour "
    "of using {replacement_name}. "
) + COMMON_REQUESTED_WARNING_FORMAT

SIMPLE_DEPRECATION_WARNING_FORMAT = (
    "The {setting_name} app setting is deprecated. Please remove any "
    "references to it from your project, as continuing to reference it will "
    "cause an exception to be raised once support is removed in "
    "{removed_in_version}."
)

COMMON_OLD_SETTING_USED_WARNING_FORMAT = (
    "Please update your Django settings to use the new setting, otherwise the "
    "app will revert to it's default behaviour once support for "
    "{prefix}_{setting_name} is removed in {removed_in_version}."
)

RENAMED_OLD_SETTING_USED_WARNING_FORMAT = (
    "The {prefix}_{setting_name} setting has been renamed to "
    "{prefix}_{replacement_name}. "
) + COMMON_OLD_SETTING_USED_WARNING_FORMAT

REPLACED_OLD_SETTING_USER_WARNING_FORMAT = (
    "The {prefix}_{setting_name} setting is deprecated in favour of using "
    "{prefix}_{replacement_name}. "
) + COMMON_OLD_SETTING_USED_WARNING_FORMAT


class DeprecatedAppSetting:
    """
    An instance of ``DeprecatedAppSetting`` stores details about a deprecated
    app setting, and helps to raise warnings related with that deprecation.
    """
    def __init__(
        self, setting_name, renamed_to=None, replaced_by=None,
        warning_category=None, additional_guidance=None
    ):
        self.setting_name = setting_name
        self.replacement_name = renamed_to or replaced_by
        self.is_renamed = renamed_to is not None
        self.warning_category = warning_category or DeprecationWarning
        self.additional_guidance = additional_guidance
        self._prefix = ''
        self.is_imminent = not issubclass(
            self.warning_category, PendingDeprecationWarning)

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    def get_removed_in_version_text(self):
        if self.is_imminent:
            return 'the next version'
        return 'two versions time'

    def _make_warning_message(self, message_format):
        if self.additional_guidance:
            message_format += ' ' + self.additional_guidance
        return message_format.format(
            prefix=self.prefix,
            setting_name=self.setting_name,
            replacement_name=self.replacement_name,
            removed_in_version=self.get_removed_in_version_text(),
        )

    def warn_if_deprecated_setting_value_requested(self, stacklevel=2):
        message_format = SIMPLE_DEPRECATION_WARNING_FORMAT
        if self.replacement_name is not None:
            message_format = REPLACED_SETTING_REQUESTED_WARNING_FORMAT
            if self.is_renamed:
                message_format = RENAMED_SETTING_REQUESTED_WARNING_FORMAT
        warnings.warn(
            self._make_warning_message(message_format),
            category=self.warning_category,
            stacklevel=stacklevel,
        )

    def warn_if_user_using_old_setting_name(self, stacklevel=2):
        warnings.warn(
            self._make_warning_message(
                RENAMED_OLD_SETTING_USED_WARNING_FORMAT if self.is_renamed
                else REPLACED_OLD_SETTING_USER_WARNING_FORMAT
            ),
            category=self.warning_category,
            stacklevel=stacklevel,
        )
