# Generated by Django 5.0.4 on 2024-05-09 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnes_club', '0010_alter_group_clients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='clients',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='fitnes_club.client'),
        ),
    ]