"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django 관리자 사이트를 위한 admin 모듈을 가져옵니다
# admin.site.urls를 통해 /admin/ 경로에 관리자 페이지 접근 가능
from django.contrib import admin

# Django의 URL 패턴 정의를 위한 함수들을 가져옵니다
# path: 개별 URL 패턴을 정의하는 함수
# include: 다른 앱의 urls.py 파일을 포함시키는 함수 (URL 분산 관리)
from django.urls import path, include

# Django에서 제공하는 기본 인증 뷰들을 가져옵니다
# views as auth_views: 이름 충돌을 피하기 위해 별칭 사용
# LoginView, LogoutView 등 로그인/로그아웃 관련 기본 뷰 제공
from django.contrib.auth import views as auth_views

# blog 앱의 views.py에서 정의한 뷰 함수들을 가져옵니다
# views as blog_views: auth_views와 구분하기 위해 별칭 사용
# signup_view 등 커스텀 뷰 함수들 사용
from blog import views as blog_views

# urlpatterns: Django가 URL을 매칭할 때 참조하는 패턴 리스트
# Django는 요청된 URL을 이 리스트의 위에서부터 아래로 순서대로 확인합니다
# 첫 번째로 매칭되는 패턴을 찾으면 해당 뷰를 실행합니다
urlpatterns = [
    
    # 관리자 페이지 URL 패턴
    # URL: http://도메인/admin/ (예: http://127.0.0.1:8000/admin/)
    # 기능: Django 관리자 인터페이스 접근
    # 실행: Django의 기본 관리자 사이트 표시
    # 용도: 
    #   - 데이터베이스 데이터 관리 (게시글, 사용자 등)
    #   - 슈퍼유저 계정으로 로그인 필요
    #   - 개발 및 관리 목적으로 사용
    path('admin/', admin.site.urls),
    
    # 블로그 앱의 모든 URL을 루트 경로에 포함
    # URL: http://도메인/ (루트 경로부터 시작)
    # include('blog.urls'): blog/urls.py 파일의 모든 URL 패턴을 현재 위치에 포함
    # 예시:
    #   - blog/urls.py에 path('posts/', ...)가 있으면
    #   - 실제 URL은 http://도메인/posts/가 됨
    # 장점: URL 관리를 각 앱별로 분산하여 코드 정리 및 유지보수 용이
    path('', include('blog.urls')),
    
    # 로그인 페이지 URL 패턴
    # URL: http://도메인/login/ (예: http://127.0.0.1:8000/login/)
    # 실행: Django에서 제공하는 기본 LoginView 클래스 기반 뷰
    # 기능:
    #   - GET 요청: 로그인 폼 페이지 표시
    #   - POST 요청: 사용자 인증 처리
    # 템플릿: registration/login.html (Django 기본 경로)
    # 성공시: settings.py의 LOGIN_REDIRECT_URL로 이동 ('/')
    # 별명: 'login' (템플릿에서 {% url 'login' %}으로 참조 가능)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    # 로그아웃 URL 패턴
    # URL: http://도메인/logout/ (예: http://127.0.0.1:8000/logout/)
    # 실행: Django에서 제공하는 기본 LogoutView 클래스 기반 뷰
    # 기능:
    #   - 현재 로그인된 사용자의 세션 종료
    #   - 로그아웃 처리 후 자동으로 다른 페이지로 이동
    # 이동: settings.py의 LOGOUT_REDIRECT_URL로 이동 ('/')
    # 별명: 'logout' (템플릿에서 {% url 'logout' %}으로 참조 가능)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 회원가입 페이지 URL 패턴
    # URL: http://도메인/signup/ (예: http://127.0.0.1:8000/signup/)
    # 실행: blog/views.py에서 정의한 signup_view 함수
    # 기능:
    #   - GET 요청: 회원가입 폼 페이지 표시
    #   - POST 요청: 새로운 사용자 계정 생성 처리
    # 이유: Django는 기본 SignupView를 제공하지 않아서 직접 구현 필요
    # 별명: 'signup' (템플릿에서 {% url 'signup' %}으로 참조 가능)
    path('signup/', blog_views.signup_view, name='signup'),
]

# URL 매칭 과정 예시:
# 1. 사용자가 'http://127.0.0.1:8000/posts/'에 접속
# 2. Django가 urlpatterns 리스트를 위에서부터 확인
# 3. 'admin/' → 매칭 안됨
# 4. '' (빈 문자열) → 매칭됨! include('blog.urls') 실행
# 5. blog/urls.py에서 'posts/' 패턴 찾아서 해당 뷰 실행

# 프로젝트 구조에서의 역할:
# myproject/urls.py (현재 파일) - 메인 URL 라우터 (교통 허브 역할)
# ├── admin/          → Django 관리자
# ├── login/          → 로그인 처리
# ├── logout/         → 로그아웃 처리  
# ├── signup/         → 회원가입 처리
# └── (나머지 모든 URL) → blog/urls.py로 전달

# 장점:
# 1. URL 관리의 모듈화: 각 앱별로 URL을 분리하여 관리
# 2. 코드 재사용성: 인증 관련 URL은 Django 기본 뷰 활용
# 3. 확장성: 새로운 앱 추가시 include()만 추가하면 됨
# 4. 유지보수성: 각 앱의 URL 변경이 다른 앱에 영향 없음

# as_view() 메서드 설명:
# - 클래스 기반 뷰를 함수 기반 뷰로 변환하는 메서드
# - Django의 URL 패턴은 함수만 받을 수 있어서 변환 필요
# - LoginView.as_view() → 실제로는 함수가 반환됨

# name 매개변수의 중요성:
# - 템플릿에서 URL 하드코딩 방지
# - 나쁜 예: <a href="/login/">로그인</a>
# - 좋은 예: <a href="{% url 'login' %}">로그인</a>
# - URL 구조 변경시 name만 유지하면 템플릿 수정 불필요