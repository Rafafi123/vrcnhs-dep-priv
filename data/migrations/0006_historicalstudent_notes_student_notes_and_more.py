# Generated by Django 4.1.7 on 2023-11-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alter_gradelevel_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudent',
            name='notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='historicalstudent',
            name='is_a_dropout',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_a_dropout',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5),
        ),
    ]