from wagtail.core import hooks
import re

@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    menu_items[:] = [item for item in menu_items ]

@hooks.register('after_copy_page')
def after_copy_page(request, page_class, new_page_class):
    if re.match(str(page_class), 'Week '):
        print("After copy page " + str(page_class) + str(new_page_class))
    return True
