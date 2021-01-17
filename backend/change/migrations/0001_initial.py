# Generated by Django 3.1.5 on 2021-01-17 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('milestone', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskChange',
            fields=[
                ('change_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.change')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
            bases=('change.change',),
        ),
        migrations.CreateModel(
            name='MilestoneChange',
            fields=[
                ('change_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.change')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milestone.milestone')),
            ],
            bases=('change.change',),
        ),
    ]
