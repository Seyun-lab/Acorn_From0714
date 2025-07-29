# Django의 URL 패턴 정의를 위한 path 함수를 가져옵니다
from django.urls import path

# 현재 디렉토리(blog 앱)의 views.py 파일에서 정의한 모든 뷰 함수들을 가져옵니다
# '.' 은 현재 디렉토리를 의미합니다 (blog/views.py)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('m_notice/', views.m_notice, name='m_notice'), # 게시글 메인 페이지
    path('in_notice/', views.in_notice, name='in_notice'), # 게시글 작성 페이지
    path('vi_notice/<str:title>/', views.vi_notice, name='vi_notice'), # 해당 게시글 상세 조회 페이지
    path('up_notice/', views.up_notice, name='up_notice'), # 게시글 수정 페이지
    path('delete_notice/', views.delete_notice, name='delete_notice'), # 게시글 삭제 페이지
    path('logout/', views.logout, name='logout'),
]