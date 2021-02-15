# Generated by Django 3.1.5 on 2021-02-15 10:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('change', '0002_auto_20210214_2231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentedit',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='commentedit',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='new_status',
            field=models.CharField(choices=[('', 'Backlog'), ('', 'ToDo'), ('', 'InProgress'), ('', 'Done')], max_length=20),
        ),
        migrations.AlterField(
            model_name='statuschange',
            name='old_status',
            field=models.CharField(choices=[('', 'Backlog'), ('', 'ToDo'), ('', 'InProgress'), ('', 'Done')], max_length=20),
        ),
    ]
