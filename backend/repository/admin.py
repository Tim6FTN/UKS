from django.contrib import admin
from repository.models import Repository, Invite


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass