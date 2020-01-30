class AttrReferToMethodHelper:
    """
    ``BaseAppSettingsHelper`` creates several instances of this class on
    initialisation to allow developers to neatly reference settings to get a
    value cast as a certain type of object. Behind the scenes, attribute
    requests on ``AttrReferToMethodHelper`` instance are forwarded on to
    one of the helper instance's 'get_x()' methods.

    For example, if you want the actual python module referenced by a setting,
    instead of doing this:

    ``appsettingshelper.get_module('MODULE_SETTING_NAME')``

    The 'modules' ``AttrReferToMethodHelper`` instance (set as an attribute
    on every setting helper) allows you to do this:

    ``appsettingshelper.modules.MODULE_SETTING_NAME``

    An 'objects' attribute also allows you to neatly access python objects from
    setting values too, like:

    ``appsettingshelper.objects.OBJECT_SETTING_NAME``

    And 'models' allows you to access Django models, like:

    ``appsettingshelper.models.MODEL_SETTING_NAME``

    """
    def __init__(self, settings_helper, getter_method_name):
        self.settings_helper = settings_helper
        self.getter_method_name = getter_method_name

    def __getattr__(self, name):
        if self.settings_helper.in_defaults(name):
            return self.get_value_via_helper_method(name)
        raise AttributeError("{} object has no attribute '{}'".format(
            self.settings_helper.__class__.__name__, name))

    def get_value_via_helper_method(self, setting_name):
        method = getattr(self.settings_helper, self.getter_method_name)
        return method(setting_name, warning_stacklevel=5)
