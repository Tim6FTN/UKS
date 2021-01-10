from django.contrib import admin
from milestone.models import Milestone


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    pass
