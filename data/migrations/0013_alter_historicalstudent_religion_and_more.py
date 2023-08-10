# Generated by Django 4.1.7 on 2023-08-10 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_alter_historicalstudent_strand_alter_student_strand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstudent',
            name='religion',
            field=models.CharField(choices=[('Christianity', 'Christianity'), ('Roman catholic', 'Roman Catholic'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Judaism', 'Judaism'), ('Sikhism', 'Sikhism'), ('Other', 'Other')], default='other', max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='religion',
            field=models.CharField(choices=[('Christianity', 'Christianity'), ('Roman catholic', 'Roman Catholic'), ('Islam', 'Islam'), ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Judaism', 'Judaism'), ('Sikhism', 'Sikhism'), ('Other', 'Other')], default='other', max_length=30),
        ),
    ]