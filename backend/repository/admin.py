from django.contrib import admin

from repository.models import Repository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    pass
