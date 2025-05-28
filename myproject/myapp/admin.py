from django.contrib import admin
from .models import Tree, PlantingArea, PlantingPlan

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # ✅ แสดงชื่อและราคาในตาราง
    search_fields = ('name',)
    fields = ('name', 'description', 'image', 'price')  # ✅ ให้กรอกได้ในฟอร์ม

@admin.register(PlantingArea)
class PlantingAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'user')
    search_fields = ('name', 'location')
    list_filter = ('user',)

@admin.register(PlantingPlan)
class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'user', 'start_date')
    list_filter = ('plan_type', 'start_date')
