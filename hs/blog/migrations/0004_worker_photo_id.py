# Generated by Django 2.1.4 on 2019-02-05 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190205_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='photo_id',
            field=models.TextField(null=True),
        ),
    ]
