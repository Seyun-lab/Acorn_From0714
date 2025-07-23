# Django의 앱 설정을 관리하는 AppConfig 클래스를 가져옵니다
# AppConfig는 Django 앱의 메타데이터와 설정을 정의하는 기본 클래스입니다
from django.apps import AppConfig

# BlogConfig 클래스는 'blog' 앱의 설정을 정의하는 클래스입니다
# AppConfig를 상속받아서 이 앱에 대한 다양한 설정을 커스터마이징할 수 있습니다
class BlogConfig(AppConfig):
    
    # default_auto_field: 모델에서 Primary Key(기본 키)를 자동으로 생성할 때 사용할 필드 타입을 지정
    # 'django.db.models.BigAutoField': 64비트 정수를 사용하는 자동 증가 필드
    #   - 일반 AutoField는 32비트 (최대 약 21억개 레코드)
    #   - BigAutoField는 64비트 (최대 약 922경개 레코드)
    #   - Django 3.2부터 기본값으로 BigAutoField 권장 (더 많은 데이터 저장 가능)
    # 
    # 실제 효과: models.py에서 id 필드를 명시적으로 정의하지 않으면
    # Django가 자동으로 다음과 같은 필드를 생성합니다:
    # id = models.BigAutoField(primary_key=True)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # name: 이 앱의 이름을 지정합니다
    # 'blog': 앱의 디렉토리 이름과 일치해야 합니다
    # Django는 이 이름을 사용해서:
    #   - INSTALLED_APPS에서 앱을 식별
    #   - 마이그레이션 파일 생성시 앱 구분
    #   - 템플릿, 정적 파일 경로 구성
    #   - 관리자 페이지에서 앱 그룹핑
    name = 'blog'

# apps.py 파일의 역할과 중요성:

# 1. 앱 식별 및 설정
#    - Django 프로젝트에서 이 앱을 구분하고 설정을 관리
#    - settings.py의 INSTALLED_APPS에서 'blog.apps.BlogConfig' 또는 'blog'로 등록

# 2. 앱 초기화 설정
#    - ready() 메서드를 오버라이드하여 앱 시작시 실행할 코드 정의 가능
#    - 시그널 연결, 초기 데이터 로드 등에 활용

# 3. 메타데이터 정의
#    - 앱의 기본 설정들을 중앙에서 관리
#    - verbose_name으로 관리자 페이지에서 보여질 앱 이름 커스터마이징 가능

# 4. Django 프로젝트 구조에서의 위치:
#    blog/
#    ├── __init__.py
#    ├── apps.py          ← 현재 파일 (앱 설정)
#    ├── models.py        ← 데이터베이스 모델
#    ├── views.py         ← 비즈니스 로직
#    ├── urls.py          ← URL 라우팅
#    ├── forms.py         ← 폼 정의
#    └── admin.py         ← 관리자 설정

# settings.py에서 앱 등록 방법:
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     # ... 기타 Django 기본 앱들
#     'blog',                    # 간단한 방법
#     # 또는
#     'blog.apps.BlogConfig',    # 명시적 방법 (권장)
# ]

# BlogConfig 클래스를 확장하는 예시:
# class BlogConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'blog'
#     verbose_name = '블로그'  # 관리자 페이지에서 표시될 이름
#     
#     def ready(self):
#         # 앱이 완전히 로드된 후 실행되는 코드
#         import blog.signals  # 시그널 등록
#         print("블로그