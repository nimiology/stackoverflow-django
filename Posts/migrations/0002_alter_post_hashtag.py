# Generated by Django 3.2.7 on 2021-09-30 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='post', to='Posts.Hashtag'),
        ),
    ]
