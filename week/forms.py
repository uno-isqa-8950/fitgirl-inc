from django import forms
import wagtail
from week.models import EmailTemplates

def my_choices():
    names = []
    count = 0
    d = {}
    for field in EmailTemplates._meta.get_fields():
        if type(field) is wagtail.core.fields.RichTextField:
            d[field] = str(field).replace('week.EmailTemplates.', '').replace('_', ' ').capitalize()
    print(d)
    return d.items()


class TemplateForm(forms.Form):
    def __init__(self, *args,**kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['templates'] = forms.ChoiceField(
            choices=my_choices())