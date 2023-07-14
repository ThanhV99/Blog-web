from rest_framework.generics import ListAPIView
from blog.models import BlogPage
from mysite.serializers import BlogPageListSerializer, BlogPageSerializer
from rest_framework.generics import RetrieveAPIView

class BlogPageListAPIView(ListAPIView):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageListSerializer
    
class BlogPageDetailAPIView(RetrieveAPIView):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer