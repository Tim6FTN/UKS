# Generated by Django 3.1.5 on 2021-02-20 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('milestone', '0001_initial'),
        ('commit', '0001_initial'),
        ('task', '0001_initial'),
        ('label', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_type', models.CharField(choices=[('Update', 'Update'), ('Create', 'Create'), ('Delete', 'Delete')], default='Update', max_length=20)),
                ('description', models.TextField(blank=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_change.change_set+', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'base_manager_name': 'non_polymorphic',
            },
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneChange',
            fields=[
                ('change_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.change')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milestone.milestone')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.change',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TaskChange',
            fields=[
                ('change_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.change')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.change',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('text', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DescriptionChange',
            fields=[
                ('milestonechange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.milestonechange')),
                ('old_description', models.TextField(blank=True, default='')),
                ('new_description', models.TextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.milestonechange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DueDateChange',
            fields=[
                ('milestonechange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.milestonechange')),
                ('old_due_date', models.DateField()),
                ('new_due_date', models.DateField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.milestonechange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PriorityChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('old_priority', models.CharField(choices=[('NotAssigned', 'NotAssigned'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('new_priority', models.CharField(choices=[('NotAssigned', 'NotAssigned'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StartDateChange',
            fields=[
                ('milestonechange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.milestonechange')),
                ('old_start_date', models.DateField()),
                ('new_start_date', models.DateField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.milestonechange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StateChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('new_state', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], max_length=20)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StatusChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('old_status', models.CharField(choices=[('Backlog', 'Backlog'), ('ToDo', 'ToDo'), ('InProgress', 'InProgress'), ('Done', 'Done')], max_length=20)),
                ('new_status', models.CharField(choices=[('Backlog', 'Backlog'), ('ToDo', 'ToDo'), ('InProgress', 'InProgress'), ('Done', 'Done')], max_length=20)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='LabelChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('labels', models.ManyToManyField(to='label.Label')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CommitReference',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('referenced_commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commit.commit')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CommentEdit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_text', models.TextField(blank=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='change.comment')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CloseCommitReference',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('referenced_commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commit.commit')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AssigneeChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AssignedMilestoneChange',
            fields=[
                ('taskchange_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='change.taskchange')),
                ('milestone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='milestone.milestone')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('change.taskchange',),
            managers=[
                ('non_polymorphic', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
