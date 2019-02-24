 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime, re

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm, AbstractFormSubmission
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from account.forms import User
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import RichTextBlock
from wagtail.core.blocks import PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from account.models import Profile, Program

class BlogPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('HTML', blocks.RawHTMLBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
        ('Page', blocks.PageChooserBlock()),
        ('Document', DocumentChooserBlock()),
        #('Snippet', SnippetChooserBlock(target_model= StreamField)),

        #('google_map', GoogleMapBlock()),
        #('image_carousel', blocks.ListBlock(ImageCarouselBlock(), template='yourapp/blocks/carousel.html', icon="image")),
        #('person', PersonBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]


class AboutUsIndexPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    ad_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    ad_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
		ImageChooserPanel('ad_image'),
        FieldPanel('ad_url'),
    ]

class ProgramIndexPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")

    ]
class WeekPage(Page):
    description = RichTextField(blank=True)
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)
    Page.show_in_menus_default = True


    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('start_date'),
        FieldPanel('end_date'),

    ]

class ModelIndexPage(Page):
    description = RichTextField(blank=True)
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
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])


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
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])


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
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])


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
#Added this for coloring app embedding_Kelley
class MentalArtPostPage(Page):
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

#Added this to convert HTML page into CMS - Brent
class ExtrasIndexPage(Page):
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
        user1.profile.save()
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])


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
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])

class DisclaimerPage(Page):
    disclaimer = RichTextField(blank=True)
    disclaimer2 = models.CharField(max_length=10000, blank=True, )
    disclaimer3 = models.CharField(max_length=10000, blank=True, )
    disclaimer4 = models.CharField(max_length=10000, blank=True, )
    disclaimer5 = models.CharField(max_length=10000, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('disclaimer', classname="full"),
        FieldPanel('disclaimer2', classname="full"),
        FieldPanel('disclaimer3', classname="full"),
        FieldPanel('disclaimer4', classname="full"),
        FieldPanel('disclaimer5', classname="full"),
    ]

class Disclaimerlink(Page):
    disclaimer = RichTextField(blank=True)
    disclaimer2 = models.CharField(max_length=10000, blank=True, )
    disclaimer3 = models.CharField(max_length=10000, blank=True, )
    disclaimer4 = models.CharField(max_length=10000, blank=True, )
    disclaimer5 = models.CharField(max_length=10000, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('disclaimer', classname="full"),
        FieldPanel('disclaimer2', classname="full"),
        FieldPanel('disclaimer3', classname="full"),
        FieldPanel('disclaimer4', classname="full"),
        FieldPanel('disclaimer5', classname="full"),
        ]

class LandingIndexPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    physical= RichTextField(blank=True)
    nutritional= RichTextField(blank=True)
    mental= RichTextField(blank=True)
    relational= RichTextField(blank=True)
    physicaldesc = RichTextField(blank=True)
    nutritionaldesc = RichTextField(blank=True)
    mentaldesc = RichTextField(blank=True)
    relationaldesc = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),

        FieldPanel('description', classname="full"),

        FieldPanel('physical', classname="full"),
        FieldPanel('nutritional', classname="full"),
        FieldPanel('mental', classname="full"),
        FieldPanel('relational', classname="full"),
        FieldPanel('physicaldesc', classname="full"),
        FieldPanel('nutritionaldesc', classname="full"),
        FieldPanel('mentaldesc', classname="full"),
        FieldPanel('relationaldesc', classname="full"),


    ]

class UserActivity(models.Model):
    program = models.ForeignKey(Program, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, name='Activity')
    week = models.IntegerField(name='Week', null=True)
    day = models.CharField(max_length=10, name='DayOfWeek')
    points_earned = models.IntegerField(null=True)
    creation_date = models.DateField()
    updated_date = models.DateField()

    def __str__(self):
        return("User " + self.user + " performed " + self.activity)

def log_activity(user, points, program, page_url):
    activity_log = UserActivity()
    activity_log.user = user
    activity_log.points_earned = points
    activity_log.creation_date = datetime.date.today()
    activity_log.updated_date = datetime.date.today()
    activity_log.program = program
    page_components = re.match('^.*\/week-(\d+)\/([\w-]+)\/.*$', page_url)
    week = 0
    activity = "nothing"
    if page_components:
        if type(page_components[1]) is str:
            week = page_components[1]
        if type(page_components[2]) is str:
            activity = page_components[2]
    if week:
        activity_log.Week = int(week)

    activity_log.DayOfWeek = datetime.date.today().strftime('%A')
    if activity:
        activity_log.Activity = activity

    activity_log.save()

#https://www.empoweruomaha.com/pages/spring-2019/week-1/bonus/teamwork/teamwork-quiz/
