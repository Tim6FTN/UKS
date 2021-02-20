from django.contrib import admin

from change.models import AssignedMilestoneChange, AssigneeChange, CloseCommitReference, Comment, CommentEdit, CommitReference, LabelChange, MilestoneChange, PriorityChange, StateChange, StatusChange, TaskChange, DueDateChange, StartDateChange


@admin.register(MilestoneChange)
class MilestoneChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(DueDateChange)
class DueDateChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(StartDateChange)
class StartDateChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskChange)
class TaskChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(CloseCommitReference)
class CloseCommitReferenceAdmin(admin.ModelAdmin):
    pass

@admin.register(CommitReference)
class CommitReference(admin.ModelAdmin):
    pass

@admin.register(AssigneeChange)
class AssigneeChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(LabelChange)
class LabelChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(PriorityChange)
class PriorityChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(StateChange)
class StateChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(AssignedMilestoneChange)
class AssignedMilestoneChangeAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentEdit)
class CommentEditAdmin(admin.ModelAdmin):
    pass