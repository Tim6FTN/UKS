from django.contrib import admin
from label.models import Label


# Register your models here.

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    pass
