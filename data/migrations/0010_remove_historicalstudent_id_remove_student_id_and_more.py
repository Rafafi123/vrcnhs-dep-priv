# Generated by Django 5.0.1 on 2024-01-25 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_alter_gradelevel_grade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstudent',
            name='id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='LRN',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='LRN',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
