# Generated by Django 4.0.4 on 2022-05-01 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0002_alter_student_lectures_attended_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='lectures_attended',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='prn',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='total_lectures',
            field=models.IntegerField(default=0),
        ),
    ]
