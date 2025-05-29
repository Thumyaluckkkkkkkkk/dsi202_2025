from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),                 # 👈 เส้นทางหลักของแอป
    path('accounts/', include('allauth.urls')),      # ✅ เปลี่ยนเป็น allauth สำหรับ login/signup
]

# ✅ แสดงไฟล์ media เช่น รูปภาพตอน dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

