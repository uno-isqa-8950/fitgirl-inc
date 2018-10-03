# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

class ProgramIndexPage(Page):
    description = models.CharField(max_length=255, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")

    ]
class WeekPage(Page):
    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

class ModelIndexPage(Page):
    description = models.CharField(max_length=255, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]


class FormField(AbstractFormField):
    page = ParentalKey('NutritionPostPage', on_delete=models.CASCADE, related_name='custom_form_fields')

class NutritionPostPage(Page):
    body = RichTextField(blank=True)
    #whatyouneed = models.CharField(max_length=255, blank=True, )
    #directions = models.CharField(max_length=255, blank=True, )
    #healthytip = models.CharField(max_length=255, blank=True, )
    content_panels = Page.content_panels + [
        #InlinePanel('custom_form_fields',label="Form fields"),
        #FieldPanel('whatyouneed', classname="full"),
        #FieldPanel('directions', classname="full"),
        FieldPanel('body',classname="title"),
        #FieldPanel('healthytip', classname="title", ),
    ]







