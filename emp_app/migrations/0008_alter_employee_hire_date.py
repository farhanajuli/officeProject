# Generated by Django 3.2 on 2023-12-04 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0007_remove_project_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]