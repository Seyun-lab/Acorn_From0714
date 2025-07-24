# Django의 URL 패턴 정의를 위한 path 함수를 가져옵니다
from django.urls import path

# 현재 디렉토리(blog 앱)의 views.py 파일에서 정의한 모든 뷰 함수들을 가져옵니다
# '.' 은 현재 디렉토리를 의미합니다 (blog/views.py)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('m_notice/', views.m_notice, name='m_notice'),
]