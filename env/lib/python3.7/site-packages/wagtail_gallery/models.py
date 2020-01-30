from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import RichTextField, FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render
from .managers import CategoryManager
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from wagtail.search import index
from django.utils.translation import ugettext_lazy as _
import django.http


# Create your models here.

class GalleryParentPage(RoutablePageMixin, Page):
    """
    Root page to which all galleries are attached
    """

    body = RichTextField(blank=True, help_text=_('Text to appear on gallery root page'), verbose_name=_('Body'))
    """ Text that accompanies that appears on root gallery page"""

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


    show_in_menus = True
    subpage_types = ['wagtail_gallery.GalleryPage']

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    class Meta:
        verbose_name = _("Gallery Root Page")

    def get_context(self, request: django.http.HttpRequest, *args, **kwargs: dict):
        """
        Overrides get_context of Page model and adds the archives and galleries to the context

        :param request: Django HttpRequest
        :param args: Request args
        :param kwargs: Request kwargs
        :return: Django context
        """
        context = super(GalleryParentPage, self).get_context(request)

        context['archives'] = self.get_archives()
        context['galleries'] = self.get_pagination(request, kwargs)

        return context

    def get_pagination(self, request: django.http.HttpRequest, kwargs) -> django.core.paginator.Paginator:
        """
        Get pagination for the galleries parent page

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: Pagination object
        """
        if ('year' in kwargs) and ('month' in kwargs):
            galleries = GalleryPage.objects.live().filter(first_published_at__year=kwargs['year'],
                                                          first_published_at__month=kwargs['month']).order_by(
                '-first_published_at')
        elif 'year' in kwargs:
            galleries = GalleryPage.objects.live().filter(first_published_at__year=kwargs['year']).order_by(
                '-first_published_at')
        else:
            galleries = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(galleries, 10)  # Show 10 resources per page

        page = request.GET.get('page')
        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            galleries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            galleries = paginator.page(paginator.num_pages)

        return galleries

    def get_pagination_category(self, request: django.http.HttpRequest, kwargs) -> django.core.paginator.Paginator:
        """
        Get pagination for the galleries parent page, but filtered by category

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: Pagination object
        """
        if ('year' in kwargs) and ('month' in kwargs):
            galleries = GalleryPage.objects.live().filter(categories__name__icontains=kwargs['category'])
            galleries = galleries.filter(first_published_at__year=kwargs['year'],
                                         first_published_at__month=kwargs['month']).order_by(
                '-first_published_at')
        elif 'year' in kwargs:
            galleries = GalleryPage.objects.live().filter(categories__name__icontains=kwargs['category'])
            galleries = galleries.filter(first_published_at__year=kwargs['year']).order_by(
                '-first_published_at')
        else:
            galleries = GalleryPage.objects.live().filter(categories__name__icontains=kwargs['category'])
            galleries = galleries.order_by('-first_published_at')
        paginator = Paginator(galleries, 10)  # Show 10 resources per page

        page = request.GET.get('page')
        try:
            galleries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            galleries = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            galleries = paginator.page(paginator.num_pages)

        return galleries

    @property
    def get_galleries(self) -> models.QuerySet:
        """
        Gets the galleries that are the children of a specific parent page

        :return: Queryset containing Gallery objects
        """
        galleries = GalleryParentPage.get_children().live()
        return galleries

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets the categories available

        :return: Queryset consisting of gallery objects
        """
        return Category.objects.all()

    @property
    def get_gallery_base_url(self) -> str:
        """
        URL of the base gallery parent page

        :return: URL string
        """
        return self.url

    def get_archives(self) -> list:
        """
        Gets the archives of the gallery page objects

        :return: List of dictionaries containing [{'date': <GalleryPage object>]}
        """
        archives = list(GalleryPage.objects.live().dates('first_published_at', 'month', order='DESC'))
        archives = [{'date': archive} for archive in archives]
        return archives

    def get_archives_category(self, kwargs: dict) -> list:
        """
       Gets the archives of the gallery page objects, but filtered for a specific category

       :return: List of dictionaries containing [{'date': <GalleryPage object>]}
       """
        archives = GalleryPage.objects.live().filter(categories__name__icontains=kwargs['category'])
        archives = list(archives.dates('first_published_at', 'month', order='DESC'))
        archives = [{'date': archive} for archive in archives]
        return archives

    @route(r"^(?P<year>(?:19|20)\d\d)/(?P<month>1[012]|0[1-9])/$")
    def archiveMonth(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that returns archive page for a given year and month that contains said year and months gallery
        pages

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: HttpResponse page that shows said archives
        """
        return render(request, "wagtail_gallery/gallery_parent_page.html",
                      {'self': self, 'page': self, 'galleries': self.get_pagination(request, kwargs),
                       'archives': self.get_archives()})

    @route(r"^(?P<year>(?:19|20)\d\d)/$")
    def archiveYear(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that returns archive page for a given year that contains said year and months
        gallery pages

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return:  HttpResponse page that shows said archives
        """
        return render(request, "wagtail_gallery/gallery_parent_page.html",
                      {'self': self, 'page': self, 'galleries': self.get_pagination(request, kwargs),
                       'archives': self.get_archives()})

    @route(r"^category/(?P<category>[\w\-]+)/$")
    def archive(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Routing for a particular category

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: HttpResponse
        """
        return render(request, "wagtail_gallery/gallery_parent_page.html",
                      {'self': self, 'page': self, 'galleries': self.get_pagination_category(request, kwargs),
                       'archives': self.get_archives_category(kwargs)})

    @route(r"^category/(?P<category>[\w\-]+)/(?P<year>(?:19|20)\d\d)/(?P<month>1[012]|0[1-9])/$")
    def archiveCategoryMonth(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Routing for a particular category filtered for a particular year and month

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: HttpResponse
        """
        return render(request, "wagtail_gallery/gallery_parent_page.html",
                      {'self': self, 'page': self, 'galleries': self.get_pagination_category(request, kwargs),
                       'archives': self.get_archives_category(kwargs)})

    @route(r"^category/(?P<category>[\w\-]+)/(?P<year>(?:19|20)\d\d)/$")
    def archiveCategoryYear(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Routing for a particular category filtered only by year

        :param request: Django HttpRequest
        :param kwargs: Request kwargs
        :return: HttpResponse
        """
        return render(request, "wagtail_gallery/gallery_parent_page.html",
                      {'self': self, 'page': self, 'galleries': self.get_pagination_category(request, kwargs),
                       'archives': self.get_archives_category(kwargs)})


class GalleryPage(Page):
    body = RichTextField(blank=True, help_text=_('Body of text on page'), verbose_name=_('Body'))
    """Optional body of text that is shown on a specifc gallery page"""

    description = models.TextField(blank=True, null=True, help_text=_('Short description of gallery'),
                                   verbose_name=_('Description'))
    """Optional short description of the gallery used when showing cards etc."""

    categories = models.ManyToManyField('wagtail_gallery.Category', through='wagtail_gallery.CategoryGalleryPage', blank=True,
                                        help_text=_('Categories relevant to gallery'), verbose_name=_('Categories'))
    """Categories to which a particular gallery belongs"""

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('description'),
        MultiFieldPanel([
            InlinePanel("gallery_categories", label=_("Categories"))
        ]),
        InlinePanel('gallery_image', label=_("Gallery image"),
                    panels=[
                        FieldPanel('description'),
                        ImageChooserPanel('image')]
                    )
    ]

    show_in_menus = False
    subpage_types = []
    parent_page_types = ["wagtail_gallery.GalleryParentPage"]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('description'),
        index.RelatedFields('categories', [
            index.SearchField('name'),
            index.SearchField('description'),
        ])
    ]

    class Meta:
        verbose_name = _("Gallery")

    def get_context(self, request: django.http.HttpRequest, *args, **kwargs: dict):
        """
        Gets the context for a specific gallery page

        :param request: Django HttpRequest
        :param args: Request args
        :param kwargs: Request kwargs
        :return: Context variable
        """
        context = super(GalleryPage, self).get_context(request)

        context['archives'] = self.get_archives()

        return context

    def get_archives(self) -> list:
        """
        Gets the archives for the gallery

        :return: List of dictionaries of the form: [{'date': <GalleryPage Queryset>}]
        """
        archives = list(GalleryPage.objects.live().dates('first_published_at', 'month', order='DESC'))
        archives = [{'date': archive} for archive in archives]
        return archives

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets the categories available to all galleries

        :return: Queryset containing Category objects
        """
        return Category.objects.all()

    @property
    def get_gallery_base_url(self) -> str:
        """
        Gets the url of the root gallery page to which this gallery is attached

        :return: URL string
        """
        return self.get_parent().url


class GalleryImage(Orderable):
    """
    A particular image that has an order component to it. Used to allow ordering of the gallery images on a specific gallery page
    """

    gallery = ParentalKey(GalleryPage, related_name='gallery_image')
    """Required. Not manually entered. A gallery to which to the object belongs"""

    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    """Optional description of a particular image. Used as a caption for said image."""

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image')
    )
    """Actual image to be used for said GalleryImage object"""

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('image')
    ]


class Category(models.Model):
    """
    Category to which a gallery page may belong
    """

    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    """Required. Name of the category."""

    slug = models.SlugField(unique=True, max_length=80)
    """Required. Not currently used. Slug of the category. I recommend making same as name."""

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_('Parent category'),
        on_delete=models.SET_NULL
    )
    """Optional. Parent of the category. Not currently used but allows for sub-categories."""

    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))
    """Description of a category. Not currently used."""

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        """
        Method that overrides models.Model clean method that ensures no circular references are made when it comes to the parent.
        """
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        """
        Method that overrides models.Model save method so as to deal with the slug
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Gallery Category")
        verbose_name_plural = _("Gallery Categories")


class CategoryGalleryPage(models.Model):
    """Used internally. Ignore"""

    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'), on_delete=models.CASCADE)
    page = ParentalKey('GalleryPage', related_name='gallery_categories')
    panels = [
        FieldPanel('category')
    ]

    def __str__(self):
        return str(self.category)
