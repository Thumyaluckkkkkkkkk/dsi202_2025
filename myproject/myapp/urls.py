from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('trees/', views.tree_list, name='tree_list'),
    path('trees/<int:tree_id>/', views.tree_detail, name='tree_detail'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm-cart/', views.confirm_cart, name='confirm_cart'),
    path('tree-locations/', views.tree_location_list, name='tree_location_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop_page, name='shop'),

    # ✅ รองรับการเลือกพื้นที่ปลูกต้นไม้
    path('select-tree/', views.select_location_for_tree, name='select_tree'),
    path('select-location/', views.select_location_for_tree, name='select_location_for_tree'),

    # ✅ ไปยังหน้า My Orders
    path('my-orders/', views.my_orders, name='my_orders'),

    # ✅ เพิ่มใหม่: ยืนยันการชำระเงิน
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),

    path('notifications/', views.notifications, name='notifications'),

]

