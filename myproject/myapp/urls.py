from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('trees/', views.tree_list, name='tree_list'),
    path('trees/<int:tree_id>/', views.tree_detail, name='tree_detail'),
    path('planting-areas/', views.planting_area_list, name='planting_area_list'),
    path('planting-plans/', views.planting_plan_list, name='planting_plan_list'),
    path('shop/', views.shop_page, name='shop'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('upload-slip/', views.upload_slip, name='upload_slip'),
]
