import sys

from cogwheels import BaseAppSettingsHelper, DeprecatedAppSetting


class TestAppSettingsHelper(BaseAppSettingsHelper):

    COMPLEX_REPLACEMENT_GUIDANCE = (
        "The new setting offers much greater flexibility, whilst also allowing developers to "
        "change X without changing Z. Check out the version X.X release notes for further details: "
        "https://your-django-project.readthedocs.io/en/latest/releases/X.X.html"
    )

    deprecations = (
        DeprecatedAppSetting('DEPRECATED_SETTING', warning_category=DeprecationWarning),
        DeprecatedAppSetting(
            'RENAMED_SETTING_OLD',
            renamed_to='RENAMED_SETTING_NEW',
            warning_category=DeprecationWarning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING',
            replaced_by='REPLACEMENT_SETTING',
            warning_category=PendingDeprecationWarning,
            additional_guidance=COMPLEX_REPLACEMENT_GUIDANCE
        ),
        DeprecatedAppSetting(
            'REPLACED_MODEL_SETTING',
            replaced_by='REPLACEMENT_MODEL_SETTING',
            warning_category=PendingDeprecationWarning
        ),
        DeprecatedAppSetting(
            'REPLACED_MODULE_SETTING',
            replaced_by='REPLACEMENT_MODULE_SETTING',
            warning_category=PendingDeprecationWarning
        ),
        DeprecatedAppSetting(
            'REPLACED_OBJECT_SETTING',
            replaced_by='REPLACEMENT_OBJECT_SETTING',
            warning_category=PendingDeprecationWarning
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_ONE',
            replaced_by='REPLACES_MULTIPLE',
            warning_category=DeprecationWarning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_TWO',
            replaced_by='REPLACES_MULTIPLE',
            warning_category=DeprecationWarning,
        ),
        DeprecatedAppSetting(
            'REPLACED_SETTING_THREE',
            replaced_by='REPLACES_MULTIPLE',
            warning_category=DeprecationWarning,
        ),
    )


sys.modules[__name__] = TestAppSettingsHelper()
