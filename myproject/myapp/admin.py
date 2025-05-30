from django.contrib import admin
from .models import Tree, PlantingArea, PlantingPlan, Equipment

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    fields = ('name', 'description', 'image', 'price')

# ✅ ปรับ PlantingArea ให้เป็น Tree Location (ไม่ใช้ image)
@admin.register(PlantingArea)
class TreeLocationAdmin(admin.ModelAdmin):
    list_display = ('province',)
    search_fields = ('province',)
    fields = ('province', 'description')  # เอา image ออกแล้ว

@admin.register(PlantingPlan)
class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'user', 'start_date')
    list_filter = ('plan_type', 'start_date')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    fields = ('name', 'description', 'image', 'price')


