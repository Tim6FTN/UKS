# Generated by Django 3.1.5 on 2021-02-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('', 'Backlog'), ('', 'ToDo'), ('', 'InProgress'), ('', 'Done')], default='', max_length=20),
        ),
    ]