from rest_framework import serializers
from blog.models import BlogCategory

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name', 'slug']  # Add any other fields you need    