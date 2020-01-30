from collections import defaultdict
from importlib import import_module
from django.conf import settings as django_settings
from django.core.signals import setting_changed
from cogwheels import (
    OverrideValueError, OverrideValueTypeInvalid,
    OverrideValueFormatInvalid, OverrideValueNotImportable,
    DefaultValueError, DefaultValueTypeInvalid,
    DefaultValueFormatInvalid, DefaultValueNotImportable,
)
from cogwheels.exceptions.deprecations import (
    ImproperlyConfigured,
    IncorrectDeprecationsValueType, InvalidDeprecationDefinition,
    DuplicateDeprecationError,
)
from .utils import AttrReferToMethodHelper


class BaseAppSettingsHelper:

    prefix = None
    defaults_path = None
    deprecations = ()

    def __init__(self, prefix=None, defaults_path=None, deprecations=None):
        self.__module_path_split = self.__class__.__module__.split('.')
        self._set_prefix(prefix)

        # Load values from defaults module
        self._set_defaults_module_path(defaults_path)
        self._load_defaults()

        # Load deprecation data
        if deprecations is not None:
            self._deprecations = deprecations
        else:
            self._deprecations = self.__class__.deprecations
        self._perepare_deprecation_data()

        # This will create the dictionaries if they don't already exist
        self.reset_caches()

        # Define 'attribute reference' shortcuts
        self.models = AttrReferToMethodHelper(self, 'get_model')
        self.modules = AttrReferToMethodHelper(self, 'get_module')
        self.objects = AttrReferToMethodHelper(self, 'get_object')

        setting_changed.connect(self.reset_caches, dispatch_uid=id(self))

    def __getattr__(self, name):
        """
        If the requested attribute wasn't found, it's assumed that the caller
        wants the value of a setting matching 'name'. So, if 'name' looks like
        a valid setting name, refer the request to 'self.get()', otherwise
        raise an ``AttributeError``, so that the caller knows the request is
        invalid.
        """
        if not self.in_defaults(name):
            raise AttributeError("{} object has no attribute '{}'".format(
                self.__class__.__name__, name))
        return self.get(name, warning_stacklevel=4)

    def _set_prefix(self, init_supplied_val):
        """
        Sets this object's ``_prefix`` attribute to a sensible value. If no
        value was provided to __init__(), and no value has been set using the
        ``prefix`` class attribute, a default value will be used, based on
        where the helper class is defined.

        For example:

        If the class is defined in ``myapp/conf/settings.py`` or
        ``myapp/settings.py``, the value ``"MYAPP"`` would be used.

        If the class is defined in ``myapp/subapp/conf/settings.py`` or
        ``myapp/subapps/settings.py`` the value ``"MYAPP_SUBAPP"`` would be
        used.
        """
        if init_supplied_val is not None:
            value = init_supplied_val.rstrip('_')
        elif self.__class__.prefix is not None:
            value = self.__class__.prefix.rstrip('_')
        else:
            module_path_parts = self.__module_path_split[:-1]
            try:
                module_path_parts.remove('conf')
            except ValueError:
                pass
            value = '_'.join(module_path_parts).upper()
        self._prefix = value

    def _set_defaults_module_path(self, init_supplied_val):
        """
        Sets this object's ``_defaults_module_path`` attribute to a sensible
        value. If no value was provided to __init__(), and no value has been
        set using the ``defaults_path`` class attribute, a default value will
        be used, based on where the helper class is defined.

        It is assumed that the defaults module is defined in the same directory
        as the settings helper. For example:

        If the settings helper is defined in ``myapp/config/settings.py``, the
        defaults module is assumed to be at ``myapp/config/defaults.py``.

        If the settings helper is defined in ``myapp/some_other_directory/settings.py``,
        the defaults module is assumed to be at ``myapp/some_other_directory/defaults.py``.
        """
        if init_supplied_val is not None:
            value = init_supplied_val
        elif self.__class__.defaults_path is not None:
            value = self.__class__.defaults_path
        else:
            value = '.'.join(self.__module_path_split[:-1]) + ".defaults"
        self._defaults_module_path = value

    @staticmethod
    def _do_import(module_path):
        """A simple wrapper for importlib.import_module()."""
        return import_module(module_path)

    @staticmethod
    def _make_cache_key(setting_name, accept_deprecated):
        key = setting_name
        if accept_deprecated:
            key += '_accepting_' + str(accept_deprecated)
        return key

    def _load_defaults(self):
        """
        Sets the object's ``_defaults`` attibute value to a dictionary for
        optimal lookup performance. Items are loaded from the relevant
        ``defaults.py`` module on initialisation.
        """
        module = self._do_import(self._defaults_module_path)
        self._defaults = {
            k: v for k, v in module.__dict__.items()
            if k.isupper()  # ignore anything that doesn't look like a setting
        }

    def _perepare_deprecation_data(self):
        """
        Cycles through the list of AppSettingDeprecation instances set on
        ``self._deprecations`` and propulates two new dictionary attributes:

        ``self._deprecated_settings``:
            Uses the deprecated setting names as keys, and will be
            used to identify if a requested setting value if for a deprecated
            setting.

        ``self._renamed_settings``:
            Uses the 'replacement setting' names as keys (if supplied), and
            allows us to temporarily support user-defined settings using the
            old name when the new setting is requested.
        """
        if not isinstance(self._deprecations, (list, tuple)):
            raise IncorrectDeprecationsValueType(
                "'deprecations' must be a list or tuple, not a {}."
                .format(type(self._deprecations).__name__)
            )

        self._deprecated_settings = {}
        self._replacement_settings = defaultdict(list)

        for item in self._deprecations:
            item.prefix = self._prefix

            if not self.in_defaults(item.setting_name):
                raise InvalidDeprecationDefinition(
                    "There is an issue with one of your setting deprecation "
                    "definitions. '{setting_name}' could not be found in "
                    "{defaults_module_path}. Please ensure a default value "
                    "remains there until the end of the setting's deprecation "
                    "period."
                    .format(
                        setting_name=item.setting_name,
                        defaults_module_path=self._defaults_module_path,
                    )
                )

            if item.setting_name in self._deprecated_settings:
                raise DuplicateDeprecationError(
                    "The setting name for each deprecation definition "
                    "must be unique, but '{setting_name}' has been used more "
                    "than once for {helper_class}. "
                    .format(
                        setting_name=item.setting_name,
                        helper_class=self.__class__.__name__,
                    )
                )

            self._deprecated_settings[item.setting_name] = item

            if item.replacement_name:

                if not self.in_defaults(item.replacement_name):
                    raise InvalidDeprecationDefinition(
                        "There is an issue with one of your settings "
                        "deprecation definitions. '{replacement_name}' is not "
                        "a valid replacement for '{setting_name}', as no such "
                        "value can be found in {defaults_module_path}."
                        .format(
                            replacement_name=item.replacement_name,
                            setting_name=item.setting_name,
                            defaults_module_path=self._defaults_module_path,
                        )
                    )

                self._replacement_settings[item.replacement_name].append(item)

    def reset_caches(self, **kwargs):
        self._raw_cache = {}
        self._models_cache = {}
        self._modules_cache = {}
        self._objects_cache = {}

    def in_defaults(self, setting_name):
        return setting_name in self._defaults

    def get_default_value(self, setting_name):
        try:
            return self._defaults[setting_name]
        except KeyError:
            pass
        raise ImproperlyConfigured(
            "No default value could be found in {default_module} with the "
            "name '{setting_name}'."
            .format(
                setting_name=setting_name,
                default_module=self._defaults_module_path,
            )
        )

    def get_prefix(self):
        return self._prefix + '_'

    def get_prefixed_setting_name(self, setting_name):
        return self.get_prefix() + setting_name

    def get_user_defined_value(self, setting_name):
        attr_name = self.get_prefixed_setting_name(setting_name)
        return getattr(django_settings, attr_name)

    def is_overridden(self, setting_name):
        attr_name = self.get_prefixed_setting_name(setting_name)
        return hasattr(django_settings, attr_name)

    def raise_setting_error(
        self, setting_name, additional_text,
        user_value_error_class=None, default_value_error_class=None,
        **text_format_kwargs
    ):
        if self.is_overridden(setting_name):
            error_class = user_value_error_class or OverrideValueError
            message = (
                "There is an issue with the value specified for "
                "{setting_name} in your project's Django settings."
            ).format(setting_name=self.get_prefixed_setting_name(setting_name))
        else:
            error_class = default_value_error_class or DefaultValueError
            message = (
                "There is an issue with the default value specified for "
                "{setting_name} in {defaults_module}."
            ).format(
                setting_name=setting_name,
                defaults_module=self._defaults_module_path,
            )

        message += ' ' + additional_text.format(**text_format_kwargs)
        raise error_class(message)

    def _get_raw_value(self, setting_name, accept_deprecated='',
                       suppress_warnings=False, warning_stacklevel=3):
        """
        Returns the value of the app setting named by ``setting_name``,
        exactly as it has been defined in the defaults module or a user's
        Django settings.

        If the requested setting is deprecated, a suitable deprecation
        warning is raised to help inform developers of the change.

        If the requested setting replaces a single deprecated setting, and no
        user defined setting name is defined using the new name, the method
        will look for a user defined setting value using the deprecated setting
        name, and return that if found. A deprecation warning will also be
        raised.

        If the requested setting replaces multiple deprecated settings, the
        ``accept_deprecated`` keyword argument can be used to specify which of
        those deprecated settings to accept as the value if defined by a user.

        If no override value was found in the Django setting, then the
        relevant value from the defaults module is returned.
        """
        if self.is_overridden(setting_name):
            return self.get_user_defined_value(setting_name)

        if setting_name in self._replacement_settings:
            deprecations = self._replacement_settings[setting_name]
            for item in deprecations:
                if(
                    (len(deprecations) == 1 or item.setting_name == accept_deprecated) and
                    self.is_overridden(item.setting_name)
                ):
                    if not suppress_warnings:
                        item.warn_if_user_using_old_setting_name(warning_stacklevel)
                    return self.get_user_defined_value(item.setting_name)
        return self.get_default_value(setting_name)

    def is_value_from_deprecated_setting(self, setting_name, deprecated_setting_name):
        """
        Help developers determine where the settings helper got it's value from
        when dealing settings that replace deprecated settings.

        Returns ``True`` when the new setting (with the name ``setting_name``)
        is a replacement for a deprecated setting (with the name
        ``deprecated_setting_name``) and the user is still using the deprecated
        setting in their Django settings to override behaviour.
        """
        if not self.in_defaults(setting_name):
            raise ValueError("'%s' is not a valid setting name" % setting_name)
        if not self.in_defaults(deprecated_setting_name):
            raise ValueError("'%s' is not a valid setting name" % deprecated_setting_name)
        if deprecated_setting_name not in self._deprecated_settings:
            raise ValueError(
                "The '%s' setting is not deprecated. When using "
                "settings.is_value_from_deprecated_setting(), the deprecated "
                "setting name should be supplied as the second argument." %
                deprecated_setting_name
            )
        if(
            not self.is_overridden(setting_name) and
            setting_name in self._replacement_settings
        ):
            deprecations = self._replacement_settings[setting_name]
            for item in deprecations:
                if(
                    item.setting_name == deprecated_setting_name and
                    self.is_overridden(item.setting_name)
                ):
                    return True
        return False

    def get(self, setting_name, accept_deprecated='', enforce_type=None,
            check_if_setting_deprecated=True, suppress_warnings=False,
            warning_stacklevel=3):
        """
        A wrapper for self._get_raw_value(), that caches the raw setting value
        for faster future access, and (if ``enforce_type`` is supplied) checks
        that the raw value is the required type.

        In situations where the named setting replaces multiple deprecated
        settings, the ``accept_deprecated`` keyword argument can be used to
        specify which of those deprecated settings to accept as the value.
        """
        if(
            check_if_setting_deprecated and not suppress_warnings and
            setting_name in self._deprecated_settings
        ):
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_deprecated_setting_value_requested(warning_stacklevel)

        cache_key = self._make_cache_key(setting_name, accept_deprecated)
        if cache_key in self._raw_cache:
            return self._raw_cache[cache_key]

        result = self._get_raw_value(
            setting_name,
            accept_deprecated=accept_deprecated,
            suppress_warnings=suppress_warnings,
            warning_stacklevel=warning_stacklevel + 1,
        )

        if enforce_type and not isinstance(result, enforce_type):
            if isinstance(enforce_type, tuple):
                msg = (
                    "The value is expected to be one of the following types, "
                    "but a value of type '{current_type}' was found: "
                    "{required_types}."
                )
                text_format_kwargs = dict(
                    current_type=type(result).__name__,
                    required_types=enforce_type,
                )
            else:
                msg = (
                    "The value is expected to be a '{required_type}', but a "
                    "value of type '{current_type}' was found."
                )
                text_format_kwargs = dict(
                    current_type=type(result).__name__,
                    required_type=enforce_type.__name__,
                )
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueTypeInvalid,
                default_value_error_class=DefaultValueTypeInvalid,
                additional_text=msg,
                **text_format_kwargs
            )
        self._raw_cache[cache_key] = result
        return result

    def get_model(self, setting_name, accept_deprecated='',
                  suppress_warnings=False, warning_stacklevel=3):
        """
        Returns a Django model referenced by an app setting where the value is
        expected to be a 'model string' in the format 'app_label.model_name'.

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        in the correct format, or refers to a model that is not available.

        In situations where the named setting replaces multiple deprecated
        settings, the ``accept_deprecated`` keyword argument can be used to
        specify which of those deprecated settings to accept as the raw value.
        """
        if not suppress_warnings and setting_name in self._deprecated_settings:
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_deprecated_setting_value_requested(warning_stacklevel)

        cache_key = self._make_cache_key(setting_name, accept_deprecated)
        if cache_key in self._models_cache:
            return self._models_cache[cache_key]

        raw_value = self.get(
            setting_name,
            enforce_type=str,
            accept_deprecated=accept_deprecated,
            check_if_setting_deprecated=False,
            suppress_warnings=suppress_warnings,
            warning_stacklevel=warning_stacklevel + 1,
        )

        try:
            from django.apps import apps  # delay import until needed
            result = apps.get_model(raw_value)
            self._models_cache[cache_key] = result
            return result
        except ValueError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueFormatInvalid,
                default_value_error_class=DefaultValueFormatInvalid,
                additional_text=(
                    "Model strings should match the format 'app_label.Model', "
                    "which '{value}' does not adhere to."
                ),
                value=raw_value,
            )
        except LookupError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "The model '{value}' does not appear to be installed."
                ),
                value=raw_value
            )

    def get_module(self, setting_name, accept_deprecated='',
                   suppress_warnings=False, warning_stacklevel=3):
        """
        Returns a Python module referenced by an app setting where the value is
        expected to be a valid, absolute Python import path, defined as a
        string (e.g. "myproject.app.custom_module").

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path.
        """
        if not suppress_warnings and setting_name in self._deprecated_settings:
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_deprecated_setting_value_requested(warning_stacklevel)

        cache_key = self._make_cache_key(setting_name, accept_deprecated)
        if cache_key in self._modules_cache:
            return self._modules_cache[cache_key]

        raw_value = self.get(
            setting_name,
            enforce_type=str,
            accept_deprecated=accept_deprecated,
            check_if_setting_deprecated=False,
            suppress_warnings=suppress_warnings,
            warning_stacklevel=warning_stacklevel + 1,
        )

        try:
            result = self._do_import(raw_value)
            self._modules_cache[cache_key] = result
            return result
        except ImportError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No module could be found matching the path '{value}'. "
                    "Please use a full (not relative) import path in the "
                    "format: 'project.app.module'."
                ),
                value=raw_value
            )

    def get_object(self, setting_name, accept_deprecated='',
                   suppress_warnings=False, warning_stacklevel=3):
        """
        Returns a python class, method, or other object referenced by an app
        setting where the value is expected to be a valid, absolute Python
        import path, defined as a string (e.g. "myproject.app.module.MyClass").

        Raises an ``ImproperlyConfigured`` error if the setting value is not
        a valid import path, or the object cannot be found in the specified
        module.
        """
        if not suppress_warnings and setting_name in self._deprecated_settings:
            depr = self._deprecated_settings[setting_name]
            depr.warn_if_deprecated_setting_value_requested(warning_stacklevel)

        cache_key = self._make_cache_key(setting_name, accept_deprecated)
        if cache_key in self._objects_cache:
            return self._objects_cache[cache_key]

        raw_value = self.get(
            setting_name,
            enforce_type=str,
            accept_deprecated=accept_deprecated,
            check_if_setting_deprecated=False,
            suppress_warnings=suppress_warnings,
            warning_stacklevel=warning_stacklevel + 1,
        )
        try:
            module_path, object_name = raw_value.rsplit(".", 1)
        except ValueError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueFormatInvalid,
                default_value_error_class=DefaultValueFormatInvalid,
                additional_text=(
                    "'{value}' is not a valid object import path. Please use "
                    "a full (not relative) import path with the object name "
                    "at the end, for example: 'project.app.module.object'."
                ),
                value=raw_value
            )
        try:
            result = getattr(self._do_import(module_path), object_name)
            self._objects_cache[cache_key] = result
            return result
        except ImportError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No module could be found matching the path "
                    "'{module_path}'. Please use a full (not relative) import "
                    "path with the object name at the end, for example: "
                    "'project.app.module.object'."
                ),
                module_path=module_path,
            )
        except AttributeError:
            self.raise_setting_error(
                setting_name=setting_name,
                user_value_error_class=OverrideValueNotImportable,
                default_value_error_class=DefaultValueNotImportable,
                additional_text=(
                    "No object could be found in {module_path} matching the "
                    "name '{object_name}'."
                ),
                module_path=module_path,
                object_name=object_name,
            )
