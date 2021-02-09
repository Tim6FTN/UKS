# Generated by Django 3.1.5 on 2021-02-08 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='project.project'),
        ),
    ]
