# -----------------------------------------------------------------------------
# Standard type settings
# -----------------------------------------------------------------------------

INTEGER_SETTING = 1

BOOLEAN_SETTING = False

STRING_SETTING = 'stringy'

TUPLES_SETTING = (
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
)


# -----------------------------------------------------------------------------
# Model/class and module settings
# -----------------------------------------------------------------------------

VALID_MODEL = 'tests.DefaultModel'

INCORRECT_FORMAT_MODEL = 'cogwheels.tests.DefaultModel'

UNAVAILABLE_MODEL = 'cogwheels.UnavailableModel'

VALID_MODULE = 'cogwheels.tests.modules.default_module'

UNAVAILABLE_MODULE = 'cogwheels.tests.modules.imaginary_module'

VALID_OBJECT = 'cogwheels.tests.classes.DefaultClass'

INCORRECT_FORMAT_OBJECT = 'DefaultClass'

MODULE_UNAVAILABLE_OBJECT = 'cogwheels.imaginary_module.Class'

OBJECT_UNAVAILABLE_OBJECT = 'cogwheels.tests.classes.NonExistent'


# -----------------------------------------------------------------------------
# Deprecations
# -----------------------------------------------------------------------------

DEPRECATED_SETTING = 'deprecated'

REPLACED_MODEL_SETTING = VALID_MODEL

REPLACEMENT_MODEL_SETTING = VALID_MODEL

REPLACED_MODULE_SETTING = VALID_MODULE

REPLACEMENT_MODULE_SETTING = VALID_MODULE

REPLACED_OBJECT_SETTING = VALID_OBJECT

REPLACEMENT_OBJECT_SETTING = VALID_OBJECT

RENAMED_SETTING_OLD = 'renamed_old'

RENAMED_SETTING_NEW = 'renamed_new'

REPLACED_SETTING = 'replaced_old'

REPLACEMENT_SETTING = 'replaced_new'

REPLACED_SETTING_ONE = 'replaced_one'

REPLACED_SETTING_TWO = 'replaced_two'

REPLACED_SETTING_THREE = 'replaced_three'

REPLACES_MULTIPLE = 'replaces_multiple'
