
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('aiga.urls', 'aaa'), namespace='aiga')),  # namespace 추가
]