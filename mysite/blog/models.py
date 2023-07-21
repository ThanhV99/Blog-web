from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index

# tag
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import MultiFieldPanel

#catogory
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from blog.blocks import SectionBlock
from wagtail import blocks

from datetime import datetime
import locale
from django.utils import timezone

from wagtail.api import APIField
from rest_framework import serializers

class BlogIndexPage(Page):
    age_description = "Use this page for converting users"
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    @property
    def current_datetime(self):
        locale.setlocale(locale.LC_TIME, 'vi_VN')  # Set the locale to Vietnamese
        return datetime.now().strftime("%A, %d/%m/%Y")
    
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

from rest_framework .fields import Field
class ImageSerializedField(Field):
    def to_representation(self, value):
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height
        }
        
class BlogPage(Page):
    date = models.DateField("Post date", null=True, blank=True)
    date_post = models.CharField("Post date formatted", max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250)
    body = StreamField(
        [
            ('content', blocks.RichTextBlock(required=False)),
            ("image", SectionBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    author = models.CharField(max_length=100, default="Anonymous")
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True, related_name='categories')
    feed_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=False, related_name="+")
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    search_fields = Page.search_fields + [
        # index.SearchField('intro'),
        # index.SearchField('content'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        MultiFieldPanel([
            FieldPanel('description'),
            FieldPanel('body'),
            FieldPanel('author'),
        ], heading="Content News"),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel("feed_image")
    ]
    
    api_fields = [
        APIField("date_post"),
        APIField("description"),
        APIField("feed_image"),
        APIField('body'),
        APIField('categories'),
        APIField('author'),
    ]
    
    @property
    def current_datetime(self):
        locale.setlocale(locale.LC_TIME, 'vi_VN')  # Set the locale to Vietnamese
        return datetime.now().strftime("%A, %d/%m/%Y")
    
    def save(self, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'vi_VN')
        if not self.id:
            # Page is being published for the first time
            self.date = datetime.now()
        self.date_post = datetime.now().strftime("%A, %d/%m/%Y, %H:%M")
        super().save(*args, **kwargs)
    
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    
    
class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
    
from wagtail.snippets.models import register_snippet

@register_snippet
class BlogCategory(models.Model):
    class Meta:
        verbose_name_plural = 'blog categories'
        verbose_name = "blog categories",
        ordering = ["name"]
        
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
        default="a"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name
        
    api_fields = [
        APIField('name'),
    ]
        
class BlogPageAuthor(Orderable):
    page = models.ForeignKey('blog.BlogPage', on_delete=models.CASCADE, related_name='authors')
    name = models.CharField(max_length=255)

    api_fields = [
        APIField('name'),
    ]