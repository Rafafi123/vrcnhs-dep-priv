# Generated by Django 4.1.7 on 2023-08-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_alter_historicalstudent_religion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstudent',
            name='father_contact',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_contact',
            field=models.CharField(max_length=15),
        ),
    ]
