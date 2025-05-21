from django.urls import path
from . import views

app_name = 'plantapp'  # ชื่อแอพ

urlpatterns = [
    path('', views.home, name='home'),
    path('trees/', views.tree_list, name='tree_list'),
    path('planting-areas/', views.planting_area_list, name='planting_area_list'),
    path('planting-plans/', views.planting_plan_list, name='planting_plan_list'),
]
