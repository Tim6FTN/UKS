from django.contrib import admin
from django.utils.html import format_html

from label.form import LabelForm
from label.models import Label


# Register your models here.

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    form = LabelForm
    fieldsets = (
        (None, {
            'fields': ('project', 'name', 'color')
        }),
    )

    def label(self, obj):
        def complementaryColor(my_hex):
            if my_hex[0] == '#':
                my_hex = my_hex[1:]
            try:

                rgb = tuple(int(my_hex[i:i + 2], 16) for i in (0, 2, 4))
                if (rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114) > 127:
                    return '#000000'
                return '#ffffff'
            except:
                return "#000000"

        return format_html(
            '<span style="padding: 2px 5px;border-radius: 50px;background-color:{}; color:{}">{}</span>',
            obj.color,
            complementaryColor(obj.color),
            obj.name)

    list_display = ('label',)
