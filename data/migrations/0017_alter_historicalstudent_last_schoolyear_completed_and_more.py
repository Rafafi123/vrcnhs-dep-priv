# Generated by Django 4.1.7 on 2023-08-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_alter_historicalstudent_lrn_alter_student_lrn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstudent',
            name='last_schoolyear_completed',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_schoolyear_completed',
            field=models.CharField(max_length=12),
        ),
    ]