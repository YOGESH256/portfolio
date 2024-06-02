from django.db import models


from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel,MultiFieldPanel , InlinePanel
from wagtail.fields import RichTextField ,StreamField
from modelcluster.fields import ParentalKey
from wagtail.api import APIField
from wagtail import blocks
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock

from django.utils.translation import gettext_lazy as _



class HeaderRightBlock(blocks.StructBlock):
    card_title = blocks.CharBlock(max_length=10000, required=False)
    links = blocks.TextBlock(required=False , help_text='Please provide Links',)

    api_fields = [
        APIField("card_title"),
        APIField("links"),
    ]

    # def get_api_representation(self, value, context=None):
    #     return {
    #         "title": value.get("card_title"),
    #         "links": [val.get("card_title").source for val in value.get("links") if val.get("title")],
    #     }
    
class HeaderStruct(blocks.StructBlock):
    title = blocks.CharBlock(max_length=10000, required=False)
    subheaders = blocks.ListBlock(HeaderRightBlock())

class FooterStruct(blocks.StructBlock):
    rightText= blocks.CharBlock(max_length=10000, required=False)
    leftText = blocks.CharBlock(max_length=10000, required=False)

class ImagesBlock(blocks.StructBlock):
     image_url = blocks.URLBlock(required=False)
     images = ImageChooserBlock()

     api_fields = [
        APIField("image_url"),
        APIField("images"),
    ]
     def get_api_representation(self, value, context=None):

        return {
            "image_url": value.get("image_url"),
            "images": value.get("images").file.url if value.get("images", None) else "",
        }
    

class CTABlock(blocks.StructBlock):
    """A simple call to action section."""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    api_fields = [
        APIField("title"),
        APIField("text"),
        APIField("button_page"),
        APIField("button_url"),
        APIField("button_text"),
    ]

   
    

class HeroSection(blocks.StructBlock):
    hero_section_title = blocks.RichTextBlock(required=False)
    hero_words = blocks.ListBlock(blocks.TextBlock(max_length=100))
    hero_image = ImagesBlock()
    hero_section_subttitle = blocks.TextBlock(max_length=1000 , default = 'hi there')
    hero_buttons= blocks.ListBlock(CTABlock())
    hero_images = blocks.ListBlock(ImagesBlock())
   

    api_fields = [
        APIField("hero_section_title"),
        APIField("hero_words"),
        APIField("hero_image"),
        APIField("hero_section_subttitle"),
        APIField("hero_buttons"),
        APIField("hero_images"),
    ]
    

class PointersBlock(blocks.StructBlock):
    main_title =  blocks.TextBlock(required=False)
    pointers = blocks.ListBlock(blocks.TextBlock(required=True))


    

class AboutSection(blocks.StructBlock):
    about_main_image = ImageChooserBlock(required=True)
    about_title = blocks.TextBlock(required=True , help_text='about title')
    about_description = blocks.TextBlock(required=True , help_text='about description')
    pointers_block = blocks.ListBlock(PointersBlock())

    api_fields = [
        APIField('about_main_image'),
        APIField('about_title'),
        APIField('about_description'),
        APIField('pointers_block'),
    ]

    def get_api_representation(self, value, context=None):
        print(value)
        return {
            "about_main_image": value.get("about_main_image").file.url if value.get("about_main_image", None) else "",
            "about_title": value.get("about_title"),
            "about_description": value.get("about_description"),
            "pointers_block": [
                {
                    "main_title": pointers["main_title"],
                    "pointers": list(pointers["pointers"]),
                } for pointers in value.get("pointers_block")
            ]
        }



# class AchievementSection(blocks.StructBlock):

class KnowLedgeSubsection(blocks.StructBlock):
    subtitle = blocks.CharBlock(required=True)
    subtitle_image = ImageChooserBlock()
    subtitle_header = blocks.TextBlock(required=True)
    subtitle_pointers = blocks.ListBlock(PointersBlock())

    api_fields = [
        APIField('subtitle'),
        APIField('subtitle_image'),
        APIField('subtitle_header'),
        APIField('subtitle_pointers'),

    ]


class KnowledgeSection(blocks.StructBlock):
    main_title = blocks.TextBlock(required=True)
    knowledge_subsection = blocks.ListBlock(KnowLedgeSubsection())

    api_fields = [
        APIField('main_title'),
        APIField('knowledge_subsection'),
    ]

    def get_api_representation(self, value, context=None):
        return {
            "main_title": value.get("main_title"),
            "knowledge_subsection": [
                {
                    "subtitle": subsection['subtitle'],
                    "subtitle_image": subsection['subtitle_image'].file.url if subsection['subtitle_image'] else "",
                    "subtitle_header": subsection['subtitle_header'],
                    "subtitle_pointers": [{
                        "main_title": pointer["main_title"],
                        "pointers": list(pointer["pointers"])
                    } for pointer in subsection["subtitle_pointers"]
                    ],
                    
                }  for subsection in value.get("knowledge_subsection")
            ]
        }


class ProjectSubsection(blocks.StructBlock):
    main_image = ImageChooserBlock(required=True)
    tags = blocks.ListBlock(blocks.TextBlock(required=True))
    pointers = PointersBlock()
    
    def get_api_representation(self, value, context=None):
        print(value)
        return {
            "about_main_image": value.get("main_image").file.url if value.get("main_image", None) else "",
            "tags": list(value.get("tags")),
            "pointers": {
                "main_title" : value.get("pointers")["main_title"],
                "pointers": list(value.get("pointers")["pointers"])
            }
        }
    

class AcheieveBlock(blocks.StructBlock):
    value = blocks.IntegerBlock(required=True)
    metric = blocks.TextBlock(required=True)
    postfix = blocks.BooleanBlock(required=False)
    prefix = blocks.BooleanBlock(required=False)

class AchievementsSection(blocks.StructBlock):
    subblocks = blocks.ListBlock(AcheieveBlock())
    api_fields = [
        APIField('subblocks'),
    ]


class EmailSection(blocks.StructBlock):
    email_section_title = blocks.TextBlock(required=True)
    email_section_desc = blocks.TextBlock(required=True)
    email_images = blocks.ListBlock(ImagesBlock())

    api_fields = [
        APIField('email_section_title'),
        APIField('email_section_desc'),
        APIField('email_images'),
    ]

    

class ProjectSection(blocks.StructBlock):
    main_title = blocks.TextBlock(required=True)
    tags = blocks.ListBlock(blocks.TextBlock(required=True))
    project_subsection = blocks.ListBlock(ProjectSubsection)

    api_fields = [
        APIField('main_title'),
        APIField('tags'),
        APIField('project_subsection'),
    ]

class HomePage(Page):
    header = StreamField(
        [("header", HeaderStruct())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    footer = StreamField(
        [("footer", FooterStruct())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    hero_section = StreamField(
        [("hero_section", HeroSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    about_section = StreamField(
        [("about_section", AboutSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    knowledge_section = StreamField(
        [("knowledge_section", KnowledgeSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    project_section = StreamField(
        [("project_section", ProjectSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )
    achieve_section = StreamField(
        [("achieve_section", AchievementsSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )

    email_section = StreamField(
        [("email_section", EmailSection())],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )


    content_panels = Page.content_panels +[
                FieldPanel("header"),
                MultiFieldPanel([
                  FieldPanel("hero_section")],
                  heading="hero_section"
                ),
                MultiFieldPanel([
                  FieldPanel("achieve_section")],
                  heading="achieve_section"
                ),
                MultiFieldPanel([
                  FieldPanel("about_section")],
                  heading="about_section"
                ),
                 MultiFieldPanel([
                  FieldPanel("knowledge_section")],
                  heading="knowledge_section"
                ),
                MultiFieldPanel([
                  FieldPanel("project_section")],
                  heading="project_section"
                ),
                MultiFieldPanel([
                  FieldPanel("email_section")],
                  heading="email_section"
                ),
                
                FieldPanel("footer"),
                
            
        
     ]
    
    api_fields = [
        APIField("header"),
        APIField("hero_section"),
        APIField("achieve_section"),
        APIField("about_section"),
        APIField("knowledge_section"),
        APIField("project_section"),
        APIField("email_section"),
        APIField("footer"),
    ]











