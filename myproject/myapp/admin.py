# myapp/admin.py
from django.contrib import admin
from .models import Tree, PlantingArea, PlantingPlan  # นำเข้า models ที่ต้องการลงทะเบียนใน admin

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name',)         # แสดงชื่อ field 'name' ใน list ของ admin
    search_fields = ('name',)        # เพิ่มช่องค้นหาโดยใช้ field 'name'

@admin.register(PlantingArea)
class PlantingAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'user')  # แสดง name, location, user
    search_fields = ('name', 'location')         # ช่องค้นหา name กับ location
    list_filter = ('user',)                       # เพิ่มตัวกรอง user ด้านข้าง

@admin.register(PlantingPlan)
class PlantingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'user', 'start_date')  # แสดงข้อมูลที่สำคัญ
    list_filter = ('plan_type', 'start_date')           # ตัวกรอง plan_type และ start_date
