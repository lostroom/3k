# Generated by Django 2.1.4 on 2019-02-21 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190221_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meet',
            name='meet_participant',
        ),
        migrations.DeleteModel(
            name='Meet',
        ),
    ]
