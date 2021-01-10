from django.contrib import admin
from branch.models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass
