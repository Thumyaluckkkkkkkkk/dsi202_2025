from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # 👈 เส้นทางหลักของแอปคุณ
    path('accounts/', include('django.contrib.auth.urls')),  # ระบบ login/logout
]

# ✅ เพิ่มบรรทัดนี้เพื่อให้ Django แสดงรูปจาก MEDIA_URL ได้ตอน dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
