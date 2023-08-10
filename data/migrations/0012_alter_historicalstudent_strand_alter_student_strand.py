# Generated by Django 4.1.7 on 2023-08-10 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_remove_historicalstudent_previous_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstudent',
            name='strand',
            field=models.CharField(choices=[('A', 'STEM'), ('B', 'BAM'), ('C', 'HESS'), ('D', 'SPORTS & ARTS'), ('E', 'TVL'), ('GAS', 'GAS'), ('HE', 'HE'), ('ICT', 'ICT'), ('IA', 'IA'), ('N/A', 'Not Applicable (JHS)')], max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='strand',
            field=models.CharField(choices=[('A', 'STEM'), ('B', 'BAM'), ('C', 'HESS'), ('D', 'SPORTS & ARTS'), ('E', 'TVL'), ('GAS', 'GAS'), ('HE', 'HE'), ('ICT', 'ICT'), ('IA', 'IA'), ('N/A', 'Not Applicable (JHS)')], max_length=15),
        ),
    ]