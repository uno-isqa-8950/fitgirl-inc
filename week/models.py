 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm, AbstractFormSubmission
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from account.forms import User
from wagtail.images.edit_handlers import ImageChooserPanel

class ProgramIndexPage(Page):
    description = models.CharField(max_length=255, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")

    ]
class WeekPage(Page):
    description = models.CharField(max_length=255, blank=True,)
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)
    Page.show_in_menus_default = True


    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('end_date'),

    ]

class ModelIndexPage(Page):
    description = models.CharField(max_length=255, blank=True, )
    intro = models.CharField(max_length=255, blank=True, )
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    ad_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    ad_url = models.URLField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('ad_image'),
        FieldPanel('ad_url'),

    ]

# class FormField(AbstractFormField):
#     page = ParentalKey('NutritionPostPage', on_delete=models.CASCADE, related_name='custom_form_fields')

class NutritionPostPage(Page):
    body = RichTextField(blank=True)
    morecontent = RichTextField(blank=True)
    facts = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('body',classname="title"),
        FieldPanel('morecontent',classname='full'),
        FieldPanel('facts', classname="full" ),
    ]
    #
    # def get_form_fields(self):
    #     return self.custom_form_fields.all()

class Fact(Page):
    intro = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')

    body = RichTextField(blank=True)
    content_panels= Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('body', classname="full"),

    ]

class QuestionFormField(AbstractFormField):
    page = ParentalKey('QuestionPage', on_delete=models.CASCADE, related_name='form_fields')


class QuestionPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('points_for_this_activity', classname="title"),
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
            page=self, user=form.user)
        user1=User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity
        user1.profile.save()
        #print(form.user.username)
        #print(user1.profile.points)
        #user1.profile.bio = "yes"
        #print(user1.profile.bio)
        #user1.profile.save()


class CustomFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_form')

    class Meta:
        unique_together = ('page', 'user')

class PhysicalFormField(AbstractFormField):
    page = ParentalKey('PhysicalPostPage', on_delete=models.CASCADE, related_name='form_fields')

class PhysicalPostPage(AbstractForm):
    intro = RichTextField(blank=True)
    strength = RichTextField(blank=True)
    agility = RichTextField(blank=True)
    flexibility = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)
    timer_for_this_activity = models.CharField(max_length=20, blank=True, default=datetime.time(00, 11),
                                               help_text='Time format should be in MM:SS')
    thank_you_text = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FormSubmissionsPanel(),
        # InlinePanel('form_fields'),
        FieldPanel('strength', classname="full"),
        FieldPanel('agility', classname="full"),
        FieldPanel('flexibility', classname="flexibility"),
        FieldPanel('points_for_this_activity', classname="title"),
        FieldPanel('timer_for_this_activity', classname="timer"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
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
        user1 = User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity
        user1.profile.save()
        # print(form.user.username)
        print(user1.profile.points)


class PreassessmentFormField(AbstractFormField):
    page = ParentalKey('PreassessmentPage', on_delete=models.CASCADE, related_name='form_fields')


class PreassessmentPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Create your question"),
        FieldPanel('points_for_this_activity', classname="title"),
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
            page=self, user=form.user)
        user1=User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity
        #user1.profile.save()
        #print(form.user.username)
        #print(user1.profile.points)
        user1.profile.pre_assessment = "yes"
        #print(user1.profile.bio)
        user1.profile.save()


# class CustomFormSubmission(AbstractFormSubmission):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preassessment_form')
#
#     class Meta:
#         unique_together = ('page', 'user')

class Print(Page):
    body = RichTextField(blank=True)
    content_panels= Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class MentalPostPage(Page):
    body = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    content_panels= Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('display_image')
    ]

class RewardsIndexPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),

    ]

class RewardsPostPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    display_image =models.ForeignKey('wagtailimages.Image', null= True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('display_image')
    ]


class QuestionTextFormField(AbstractFormField):
    page = ParentalKey('QuestionPageText', on_delete=models.CASCADE, related_name='form_field')


class QuestionPageText(AbstractForm):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    points_for_this_activity = models.IntegerField(blank=True, default=0)


    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('description', classname="full"),
        InlinePanel('form_field', label="Form Fields"),
        FieldPanel('points_for_this_activity', classname="title"),
        FieldPanel('thank_you_text', classname="full"),
    ]

    def get_form_fields(self):
        return self.form_field.all()

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
            page=self, user=form.user)
        user1=User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity


class PostassessmentFormField(AbstractFormField):
    page = ParentalKey('PostassessmentPage', on_delete=models.CASCADE, related_name='form_fields')


class PostassessmentPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Create your question"),
        FieldPanel('points_for_this_activity', classname="title"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
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
            page=self, user=form.user)
        user1=User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity
        #user1.profile.save()
        #print(form.user.username)
        #print(user1.profile.points)
        user1.profile.post_assessment = "yes"
        #print(user1.profile.bio)
        user1.profile.save()



