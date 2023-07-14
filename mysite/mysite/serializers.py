from rest_framework import serializers
from blog.models import BlogIndexPage, BlogPage, BlogPageGalleryImage, BlogCategory, BlogPageTag
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from wagtail.images.models import Image


class BlogIndexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogIndexPage
        fields = ['intro']
        
class BlogIndexPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogIndexPage.objects.all()
    serializer_class = BlogIndexPageSerializer
    
###########################   
class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPageGalleryImage
        fields = ['image_url']  # Add any other fields you need

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.file.url
        return None

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('name',)  # Add any other fields you need    

class BlogPageListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    gallery_images = GalleryImageSerializer(source='gallery_images.all', many=True)
    categories = BlogCategorySerializer(many=True)

    class Meta:
        model = BlogPage
        fields = ['id', 'title', 'description', 'date_post', 'gallery_images', 'categories', 'author']
        
############################################
class BlogPageSerializer(serializers.ModelSerializer):
    categories = BlogCategorySerializer(many=True)
    tags = serializers.SerializerMethodField()
    
    def get_tags(self, obj):
        return list(obj.tagged_items.all().values_list('tag__name', flat=True))

    class Meta:
        model = BlogPage
        fields = ['title', 'description', 'date_post', 'body', 'categories', 'author', 'tags']