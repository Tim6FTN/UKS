from django.contrib import admin

from change.models import MilestoneChange, TaskChange, DueDateChange, StartDateChange


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
