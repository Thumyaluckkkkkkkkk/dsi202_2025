from django.contrib import admin
from .models import Tree, PlantingArea, PlantingPlan, Equipment  # ✅ import รวม

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    fields = ('name', 'description', 'image', 'price')

@admin.register(PlantingArea)
class PlantingAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'user')
    search_fields = ('name', 'location')
    list_filter = ('user',)

@admin.register(PlantingPlan)
class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'user', 'start_date')
    list_filter = ('plan_type', 'start_date')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    fields = ('name', 'description', 'image', 'price')
