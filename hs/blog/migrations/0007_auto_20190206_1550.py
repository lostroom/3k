# Generated by Django 2.1.4 on 2019-02-06 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190206_1548'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Calls',
            new_name='Call',
        ),
    ]