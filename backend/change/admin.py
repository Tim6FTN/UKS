from django.contrib import admin

from change.models import Comment, CommentEdit, MilestoneChange, TaskChange, DueDateChange, StartDateChange


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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentEdit)
class CommentEditAdmin(admin.ModelAdmin):
    pass