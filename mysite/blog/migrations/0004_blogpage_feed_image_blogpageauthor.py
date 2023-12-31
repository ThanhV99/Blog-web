# Generated by Django 4.2.3 on 2023-07-17 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('blog', '0003_alter_blogcategory_options_remove_blogcategory_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='feed_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.CreateModel(
            name='BlogPageAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='blog.blogpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
