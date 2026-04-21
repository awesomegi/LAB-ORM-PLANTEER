from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_edible', 'created_at')
    list_filter = ('category', 'is_edible')
    search_fields = ('name', 'about', 'used_for')
