from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel

from commit.models import Commit
from label.models import Label
from milestone.models import Milestone
from task.models import Task, PRIORITIES, TASK_STATUSES, STATES

UPDATE = "Update"
CREATE = "Create"
DELETE = "Delete"
CHANGE_TYPES = [
    (UPDATE, "Update"),
    (CREATE, "Create"),
    (DELETE, "Delete")
]


class Change(PolymorphicModel):
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, default=UPDATE)
    description = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.timestamp} | {self.change_type} | {self.description}'

    non_polymorphic = models.Manager()

    class Meta:
        ordering = ['-timestamp']
        base_manager_name = 'non_polymorphic'


class MilestoneChange(Change):
    milestone = models.ForeignKey(to=Milestone, null=False, on_delete=models.CASCADE)


class DescriptionChange(MilestoneChange):
    old_description = models.TextField(default='', blank=True)
    new_description = models.TextField(default='', blank=True)


class StartDateChange(MilestoneChange):
    old_start_date = models.DateField()
    new_start_date = models.DateField()


class DueDateChange(MilestoneChange):
    old_due_date = models.DateField()
    new_due_date = models.DateField()


class TaskChange(Change):
    task = models.ForeignKey(to=Task, null=False, on_delete=models.CASCADE)


class CloseCommitReference(TaskChange):
    referenced_commit = models.ForeignKey(to=Commit, null=False, on_delete=models.CASCADE)


class CommitReference(TaskChange):
    referenced_commit = models.ForeignKey(to=Commit, null=False, on_delete=models.CASCADE)


class AssigneeChange(TaskChange):
    assignees = models.ManyToManyField(to=User)


class LabelChange(TaskChange):
    labels = models.ManyToManyField(to=Label)


class PriorityChange(TaskChange):
    old_priority = models.CharField(max_length=20, choices=PRIORITIES)
    new_priority = models.CharField(max_length=20, choices=PRIORITIES)


class StatusChange(TaskChange):
    old_status = models.CharField(max_length=20, choices=TASK_STATUSES)
    new_status = models.CharField(max_length=20, choices=TASK_STATUSES)


class StateChange(TaskChange):
    new_state = models.CharField(max_length=20, choices=STATES)


class AssignedMilestoneChange(TaskChange):
    milestone = models.ForeignKey(to=Milestone, on_delete=models.CASCADE, null=True)


class Comment(TaskChange):
    text = models.TextField()
    attachment = models.FileField(null=True, blank=True)


class CommentEdit(models.Model):
    new_text = models.TextField(default='', blank=True)
    comment = models.ForeignKey(to=Comment, null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp} | {self.new_text}'

    class Meta:
        ordering = ['-timestamp']
