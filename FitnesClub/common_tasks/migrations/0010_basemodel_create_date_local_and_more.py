# Generated by Django 5.0.4 on 2024-05-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_tasks', '0009_basemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='basemodel',
            name='create_date_local',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='update_date_local',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
