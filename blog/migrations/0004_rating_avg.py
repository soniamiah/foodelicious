# Generated by Django 2.1.3 on 2019-03-13 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='avg',
            field=models.IntegerField(),
            preserve_default=False,
        ),
    ]
