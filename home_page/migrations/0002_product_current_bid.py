# Generated by Django 3.2.5 on 2021-07-06 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='current_bid',
            field=models.IntegerField(default=15),
        ),
    ]