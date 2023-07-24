from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet, BaseAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from rest_framework import routers
from blog.serializers import BlogCategorySerializer
from blog.models import BlogCategory, BlogPage
from rest_framework.views import APIView
from rest_framework.response import Response

api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
blog_router = routers.DefaultRouter() 

# co ham serializer cua model, dky router class ViewSet ke thua tu BaseAPIViewSet
class CategoryAPIViewSet(BaseAPIViewSet):
    base_serializer_class = BlogCategorySerializer
    filter_backends = []
    meta_fields = []
    body_fields = ['id', 'slug', 'name']
    listing_default_fields = ['id', 'slug', 'name']
    nested_default_fields = []
    model = BlogCategory
    
api_router.register_endpoint("category", CategoryAPIViewSet)

class TotalBlogPostsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        total_posts = BlogPage.objects.live().count()
        return Response({'total_posts': total_posts})
    