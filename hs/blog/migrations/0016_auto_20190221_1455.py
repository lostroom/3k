# Generated by Django 2.1.4 on 2019-02-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_meet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='meet_id',
            field=models.IntegerField(unique=True),
        ),
    ]
