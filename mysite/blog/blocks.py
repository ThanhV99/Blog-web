from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from rest_framework import serializers

class SectionBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    caption = blocks.CharBlock(required=False)
     
    def get_api_representation(self, value, context=None):
        """ Recursively call get_api_representation on children and return as a plain dict """
        temp_dict = {
            'image_url': value.get("image").file.url,
            'caption': value.get("caption"),
            # any other relevant fields of your model...
        }

        return temp_dict
        