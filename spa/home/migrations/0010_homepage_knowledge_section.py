# Generated by Django 5.0.6 on 2024-05-25 21:53

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_homepage_about_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='knowledge_section',
            field=wagtail.fields.StreamField([('knowledge_section', wagtail.blocks.StructBlock([('main_title', wagtail.blocks.TextBlock(required=True)), ('knowledge_subsection', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('subtitle', wagtail.blocks.CharBlock(required=True)), ('subtitle_header', wagtail.blocks.TextBlock(required=True)), ('subtitle_pointers', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('main_title', wagtail.blocks.TextBlock(required=False)), ('pointers', wagtail.blocks.ListBlock(wagtail.blocks.TextBlock(required=True)))])))])))]))], blank=True, null=True),
        ),
    ]
