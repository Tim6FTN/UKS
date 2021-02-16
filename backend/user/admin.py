from django.contrib import admin

# Register your models here.
from user.models import GithubProfile


@admin.register(GithubProfile)
class GithubProfileAdmin(admin.ModelAdmin):
    pass