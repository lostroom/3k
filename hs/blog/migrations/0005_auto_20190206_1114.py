# Generated by Django 2.1.4 on 2019-02-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_worker_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='fio',
            field=models.CharField(max_length=50),
        ),
    ]
