from django.contrib import admin

# Register your models here.
from commit.models import Commit


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    pass