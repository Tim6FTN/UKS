# Generated by Django 3.1.5 on 2021-02-16 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('milestone', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('date_opened', models.DateTimeField()),
                ('date_closed', models.DateTimeField(null=True)),
                ('priority', models.CharField(choices=[('NotAssigned', 'NotAssigned'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='NotAssigned', max_length=20)),
                ('state', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=20)),
                ('task_status', models.CharField(choices=[('Backlog', 'Backlog'), ('ToDo', 'ToDo'), ('InProgress', 'InProgress'), ('Done', 'Done')], default='Backlog', max_length=20)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='')),
                ('assignees', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(blank=True, to='label.Label')),
                ('milestone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='milestone.milestone')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
    ]
