# Generated by Django 5.0.4 on 2024-05-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnes_club', '0012_clubcard_id_groupschedule_id_alter_clubcard_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='clients',
            field=models.ManyToManyField(blank=True, to='fitnes_club.client'),
        ),
    ]