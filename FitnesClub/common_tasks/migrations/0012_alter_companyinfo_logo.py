# Generated by Django 5.0.4 on 2024-09-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_tasks', '0011_delete_basemodel_delete_employee_article_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='logo',
            field=models.ImageField(default='', upload_to='company_logos'),
        ),
    ]