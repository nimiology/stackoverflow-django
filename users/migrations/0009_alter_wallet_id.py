# Generated by Django 3.2.7 on 2021-09-30 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_reported_wallet_ban'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]