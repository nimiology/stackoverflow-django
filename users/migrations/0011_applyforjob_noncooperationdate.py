# Generated by Django 3.2.7 on 2021-09-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_wallet_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyforjob',
            name='nonCooperationDate',
            field=models.BooleanField(default=False),
        ),
    ]
