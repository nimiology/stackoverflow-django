# Generated by Django 4.0.4 on 2022-07-30 21:00

from django.db import migrations, models
import posts.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('media', models.FileField(blank=True, null=True, upload_to=posts.utils.upload_file, validators=[posts.utils.PictureAndVideoValidator])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2048)),
                ('text', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('media', models.FileField(blank=True, null=True, upload_to=posts.utils.upload_file, validators=[posts.utils.PictureAndVideoValidator])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
