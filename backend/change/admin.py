from django.contrib import admin
from change.models import MilestoneChange, TaskChange, Change


@admin.register(MilestoneChange)
class MilestoneChangeAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskChange)
class TaskChangeAdmin(admin.ModelAdmin):
    pass
