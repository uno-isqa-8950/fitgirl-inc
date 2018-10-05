# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm, AbstractFormSubmission


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

class NutritionPostPage(AbstractForm):
    body = RichTextField(blank=True)
    morecontent = models.CharField(max_length=255, blank=True, )
    #fact = models.CharField(max_length=255, blank=True, )
    content_panels = AbstractForm.content_panels + [
        FieldPanel('body',classname="title"),
        FieldPanel('morecontent',classname='full'),
        #FieldPanel('fact', classname="title" ),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()

class Fact(Page):
    body = RichTextField(blank=True)
    content_panels= Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class QuestionFormField(AbstractFormField):
    page = ParentalKey('QuestionPage', on_delete=models.CASCADE, related_name='form_fields')


class QuestionPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Create your question"),
        FieldPanel('thank_you_text', classname="full"),
    ]

    def serve(self, request, *args, **kwargs):
        if self.get_submission_class().objects.filter(page=self, user__pk=request.user.pk).exists():
            return render(
                request,
                self.template,
                self.get_context(request)
            )

        return super().serve(request, *args, **kwargs)

    def get_submission_class(self):
        return CustomFormSubmission

    def process_form_submission(self, form):
        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self, user=form.user
        )

class CustomFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_form')

    class Meta:
        unique_together = ('page', 'user')




