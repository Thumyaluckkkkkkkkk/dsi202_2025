from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # ✅ ใช้ชื่อแอปที่คุณใช้จริง
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ สำคัญมาก! ต้องมีบรรทัดนี้
]

