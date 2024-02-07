# Generated by Django 5.0 on 2024-02-07 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_alter_historicalstudent_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstudent',
            name='adviser_contact',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='general_average',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='health_bmi',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='household_income',
            field=models.CharField(blank=True, choices=[('above Php 35,000', 'above Php 35,000'), ('from Php 18,000 - Php 35,000', 'from Php 18,000 - Php 35,000'), ('from Php 9,000 - Php 18,000', 'from Php 9,000 - Php 18,000'), ('below Php 9,000', 'below Php 9,000')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='is_a_dropout',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='is_a_four_ps_scholar',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='is_a_working_student',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='is_returnee',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='last_grade_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='last_school_attended',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='last_schoolyear_completed',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='previous_adviser',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='strand',
            field=models.CharField(blank=True, choices=[('STEM', 'STEM'), ('BAM', 'BAM'), ('HESS', 'HESS'), ('SPORTS & ARTS', 'SPORTS & ARTS'), ('TVL', 'TVL'), ('GAS', 'GAS'), ('HE', 'HE'), ('ICT', 'ICT'), ('IA', 'IA'), ('Not Applicable (JHS)', 'Not Applicable (JHS)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='adviser_contact',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='general_average',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='health_bmi',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='household_income',
            field=models.CharField(blank=True, choices=[('above Php 35,000', 'above Php 35,000'), ('from Php 18,000 - Php 35,000', 'from Php 18,000 - Php 35,000'), ('from Php 9,000 - Php 18,000', 'from Php 9,000 - Php 18,000'), ('below Php 9,000', 'below Php 9,000')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_a_dropout',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_a_four_ps_scholar',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_a_working_student',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_returnee',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_grade_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_school_attended',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_schoolyear_completed',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='previous_adviser',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='strand',
            field=models.CharField(blank=True, choices=[('STEM', 'STEM'), ('BAM', 'BAM'), ('HESS', 'HESS'), ('SPORTS & ARTS', 'SPORTS & ARTS'), ('TVL', 'TVL'), ('GAS', 'GAS'), ('HE', 'HE'), ('ICT', 'ICT'), ('IA', 'IA'), ('Not Applicable (JHS)', 'Not Applicable (JHS)')], max_length=50, null=True),
        ),
    ]