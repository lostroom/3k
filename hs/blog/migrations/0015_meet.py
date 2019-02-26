# Generated by Django 2.1.4 on 2019-02-21 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190221_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_id', models.IntegerField()),
                ('meet_theme', models.TextField()),
                ('meet_subject', models.TextField()),
                ('meet_time', models.TimeField()),
                ('meet_date', models.DateField()),
                ('meet_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meet_participant', to='blog.Worker')),
            ],
        ),
    ]