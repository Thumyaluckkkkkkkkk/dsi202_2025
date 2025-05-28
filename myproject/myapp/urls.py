from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('trees/', views.tree_list, name='tree_list'),
    path('trees/<int:tree_id>/', views.tree_detail, name='tree_detail'),  # ✅ เพิ่ม: รายละเอียดต้นไม้
    path('planting-areas/', views.planting_area_list, name='planting_area_list'),
    path('planting-plans/', views.planting_plan_list, name='planting_plan_list'),
    path('shop/', views.shop_page, name='shop'),
    path('equipment/', views.equipment_list, name='equipment_list'),  # ✅ เพิ่ม: หน้าอุปกรณ์ (ถ้ามี)
]
