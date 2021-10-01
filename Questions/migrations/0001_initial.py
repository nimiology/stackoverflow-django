# Generated by Django 3.2.7 on 2021-09-30 13:11

import Posts.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2048)),
                ('text', models.TextField()),
                ('pic', models.ImageField(blank=True, upload_to=Posts.utils.upload_image_Question)),
                ('slug', models.SlugField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(blank=True, related_name='question', to='users.Category')),
                ('downVote', models.ManyToManyField(blank=True, related_name='questionDownVote', to='users.Wallet')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='users.wallet')),
                ('tech', models.ManyToManyField(blank=True, related_name='question', to='users.Tech')),
                ('upVote', models.ManyToManyField(blank=True, related_name='questionUpVote', to='users.Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pic', models.ImageField(blank=True, upload_to=Posts.utils.upload_image_Answer)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('downVote', models.ManyToManyField(blank=True, related_name='answerDownVote', to='users.Wallet')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='users.wallet')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='Questions.question')),
                ('upVote', models.ManyToManyField(blank=True, related_name='answerUpVote', to='users.Wallet')),
            ],
        ),
    ]