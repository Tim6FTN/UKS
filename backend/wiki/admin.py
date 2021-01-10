from django.contrib import admin
from wiki.models import Wiki


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    pass
