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
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm, AbstractFormSubmission
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from account.forms import User
from wagtail.images.edit_handlers import ImageChooserPanel
from account.models import Profile, Program
from wagtail.images.models import Image, AbstractImage


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
    description =  RichTextField(blank=True)

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
    vertical_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='+')
    vertical_url = models.URLField(blank=True)
    announcements = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('ad_image'),
        FieldPanel('ad_url'),
        ImageChooserPanel('vertical_image'),
        FieldPanel('vertical_url'),
        FieldPanel('announcements', classname="full"),


    ]


class NutritionGame(Page):
    body = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    content_panels= Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('display_image')
    ]

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


class Fact(Page):
    intro = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    description = RichTextField(blank=True)
    body = RichTextField(blank=True)
    content_panels= Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
        FieldPanel('body', classname="full"),
        FieldPanel('description', classname="full")
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
        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])

class BonusQuestionFormField(AbstractFormField):
    page = ParentalKey('BonusQuestionPage', on_delete=models.CASCADE, related_name='form_fields')

class BonusQuestionPage(AbstractForm):
    intro = RichTextField(blank=True)
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    thank_you_text = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
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

    # def serve(self, request, *args, **kwargs):
    #     if self.get_submission_class().objects.filter(page=self, user__pk=request.user.pk).exists():
    #         return render(
    #             request,
    #             self.template,
    #             self.get_context(request)
    #         )
    #
    #     return super().serve(request, *args, **kwargs)
    #
    # def get_submission_class(self):
    #     return CustomFormSubmission

    def process_form_submission(self, form):
        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self)
        user1=User.objects.get(username=form.user.username)
        print(user1.profile.points)
        user1.profile.points += self.points_for_this_activity
        user1.profile.pre_assessment = "yes"
        user1.profile.save()

        log_activity(user1, self.points_for_this_activity, user1.profile.program, form.data['pageurl'])

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

    def get_context(self, request):
        context = super().get_context(request)
        context['user_data'] = User.objects.get(username=request.user.username)
        return context


class ExtrasIndexPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    additional = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),

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
    display_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    thank_you_text = RichTextField(blank=True)
    points_for_this_activity = models.IntegerField(blank=True, default=0)
    start_date = models.DateTimeField("Start Date", null=True, blank=True)
    end_date = models.DateTimeField("End Date", null=True, blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('display_image'),
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
        user1.profile.post_assessment = "yes"
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
    additional = RichTextField(blank=True)
    card_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='+')
    physical= RichTextField(blank=True)
    card_imageb = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    nutritional= RichTextField(blank=True)
    card_imagec = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    mental= RichTextField(blank=True)
    card_imaged = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')
    relational= RichTextField(blank=True)
    physicaldesc = RichTextField(blank=True)
    nutritionaldesc = RichTextField(blank=True)
    mentaldesc = RichTextField(blank=True)
    relationaldesc = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('additional', classname="full"),
        ImageChooserPanel('card_image'),
        FieldPanel('physical', classname="full"),
        ImageChooserPanel('card_imageb'),
        FieldPanel('nutritional', classname="full"),
        ImageChooserPanel('card_imagec'),
        FieldPanel('mental', classname="full"),
        ImageChooserPanel('card_imaged'),
        FieldPanel('relational', classname="full"),
        FieldPanel('physicaldesc', classname="full"),
        FieldPanel('nutritionaldesc', classname="full"),
        FieldPanel('mentaldesc', classname="full"),
        FieldPanel('relationaldesc', classname="full"),


    ]

class EmailTemplates(Page):
    subject_for_inactivity = models.CharField(max_length=10000, blank=True)
    subject_for_group = models.CharField(max_length=10000, blank=True)
    group_message = RichTextField(blank=True)
    inactivity_message = RichTextField(blank=True)
    subject_for_rewards_notification = models.CharField(max_length=10000, blank=True)
    rewards_message = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subject_for_group', classname="full"),
        FieldPanel('group_message', classname="full"),
        FieldPanel('subject_for_inactivity', classname="full"),
        FieldPanel('inactivity_message', classname="full"),
        FieldPanel('subject_for_rewards_notification', classname="full"),
        FieldPanel('rewards_message', classname="full"),

        ]

class KindnessCardPage(Page):
    KindnessCard = models.CharField(max_length=10000, blank=True, )
    KindnessCard2 = models.CharField(max_length=10000, blank=True, )
    KindnessCard3 = models.CharField(max_length=10000, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('KindnessCard', classname="full"),
        FieldPanel('KindnessCard2', classname="full"),
        FieldPanel('KindnessCard3', classname="full"),

    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['user_data'] = User.objects.filter(is_superuser=False).filter(is_active=True).exclude(username=request.user.username)
        return context



class UserActivity(models.Model):
    program = models.ForeignKey(Program, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, name='Activity')
    week = models.IntegerField(name='Week', null=True)
    day = models.CharField(max_length=10, name='DayOfWeek')
    points_earned = models.IntegerField(null=True)
    creation_date = models.DateField()
    updated_date = models.DateField()



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



class SidebarContentPage(Page):
    subject_for_announcement1 = models.CharField(max_length=10000, blank=True)
    message_announcement1 = RichTextField(blank=True)
    subject_for_announcement2 = models.CharField(max_length=10000,blank=True)
    message_announcement2 = RichTextField(blank=True)
    subject_for_announcement3 = models.CharField(max_length=10000, blank=True)
    message_announcement3 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subject_for_announcement1', classname="full"),
        FieldPanel('message_announcement1', classname="full"),
        FieldPanel('subject_for_announcement2', classname="full"),
        FieldPanel('message_announcement2', classname="full"),
        FieldPanel('subject_for_announcement3', classname="full"),
        FieldPanel('message_announcement3', classname="full"),
    ]


class AnnouncementAlertPage(Page):
    announcements = RichTextField(blank=True)
    display_warning = models.BooleanField(
        default=False, help_text='Check this box to display warning announcement on the website'
    )

    content_panels = Page.content_panels + [
        FieldPanel('announcements', classname="full"),
        FieldPanel('display_warning'),

    ]



class SidebarImagePage(Page):
    subject_for_advertisement = models.CharField(max_length=10000, blank=True)
    advertisement_image = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('subject_for_advertisement', classname="full"),
        FieldPanel('advertisement_image', classname="full"),

    ]


class StatementsPage(Page):
    mission = models.CharField(max_length=200, blank=True, )
    vision = models.CharField(max_length=200, blank=True, )
    values = models.CharField(max_length=200, blank=True, )

    content_panels = Page.content_panels + [
        FieldPanel('mission'),
        FieldPanel('vision'),
        FieldPanel('values'),
    ]

class howitworks(Page):
    text1 = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('text1', classname="full"),

    ]


class addstudentoftheweek(Page):
    intro=RichTextField(blank=True)
    student_name = models.CharField(max_length=200, blank=True,)
    my_favorite_color = models.CharField(max_length=200, blank=True,)
    my_favorite_healthy_snack = models.CharField(max_length=200, blank=True,)
    my_favorite_sport =models.CharField(max_length=200, blank=True,)
    my_favorite_athlete = models.CharField(max_length=200, blank=True,)
    my_friends_would_describe_me_as = models.CharField(max_length=300, blank=True,)
    am_good_at = models.CharField(max_length=300, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('student_name'),
        FieldPanel('my_favorite_color'),
        FieldPanel('my_favorite_healthy_snack'),
        FieldPanel('my_favorite_sport'),
        FieldPanel('my_favorite_athlete'),
        FieldPanel('my_friends_would_describe_me_as'),
        FieldPanel('am_good_at'),
    ]


class PrivacyPolicyLink(Page):
    policy = RichTextField(blank=True)
    policy2 = models.CharField(max_length=10000, blank=True, )
    attach_file = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('policy', classname="full"),
        FieldPanel('policy2', classname="full"),
        FieldPanel('attach_file', classname="full"),
    ]