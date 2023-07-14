from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class SectionBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    caption = blocks.RichTextBlock(required=False)