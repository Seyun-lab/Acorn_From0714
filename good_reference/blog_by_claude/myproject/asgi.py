"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# os 모듈: 운영체제와 상호작용하기 위한 Python 표준 라이브러리
# 환경 변수 설정, 파일 시스템 접근 등에 사용
import os

# Django의 ASGI 애플리케이션을 생성하는 함수를 가져옵니다
# ASGI: Asynchronous Server Gateway Interface
# - 비동기 웹 서버와 Python 웹 애플리케이션 간의 표준 인터페이스
# - WebSocket, HTTP/2, Server-Sent Events 등 실시간 통신 지원
# - WSGI의 후속 버전으로 더 현대적이고 강력함
from django.core.asgi import get_asgi_application

# 환경 변수 'DJANGO_SETTINGS_MODULE' 설정
# os.environ.setdefault(): 환경 변수가 이미 설정되어 있지 않은 경우에만 기본값 설정
# 'DJANGO_SETTINGS_MODULE': Django가 어떤 설정 파일을 사용할지 지정하는 환경 변수
# 'myproject.settings': myproject/settings.py 파일을 사용하도록 지정
# 
# 용도:
# - Django가 시작될 때 어떤 설정을 로드할지 알려줌
# - 개발/테스트/배포 환경별로 다른 설정 파일 사용 가능
# - 예: 'myproject.settings.production', 'myproject.settings.development'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Django ASGI 애플리케이션 인스턴스 생성
# get_asgi_application(): Django 프로젝트를 ASGI 호환 애플리케이션으로 변환
# application: ASGI 서버(Daphne, Uvicorn 등)에서 호출할 수 있는 애플리케이션 객체
# 
# 역할:
# 1. HTTP 요청을 Django로 전달
# 2. WebSocket 연결 처리 (Django Channels 사용시)
# 3. 비동기 처리 지원
# 4. 여러 프로토콜 동시 지원 (HTTP, WebSocket 등)
application = get_asgi_application()

# ASGI vs WSGI 비교:
# 
# WSGI (Web Server Gateway Interface):
# - 동기식 처리만 지원
# - HTTP 요청/응답만 처리
# - Apache, Gunicorn 등에서 사용
# - 기존의 전통적인 웹 애플리케이션에 적합
# 
# ASGI (Asynchronous Server Gateway Interface):
# - 비동기 처리 지원
# - HTTP, WebSocket, HTTP/2 등 다양한 프로토콜 지원
# - 실시간 기능 구현 가능 (채팅, 알림 등)
# - Daphne, Uvicorn, Hypercorn 등에서 사용
# - 현대적인 웹 애플리케이션에 적합

# 배포시 ASGI 서버 사용 예시:
# 1. Daphne (Django Channels의 기본 서버):
#    daphne myproject.asgi:application
# 
# 2. Uvicorn (FastAPI에서도 사용):
#    uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000
# 
# 3. Hypercorn:
#    hypercorn myproject.asgi:application

# asgi.py 파일의 사용 시나리오:
# 
# 1. 일반 웹사이트 (HTTP만 사용):
#    - WSGI나 ASGI 둘 다 사용 가능
#    - 성능상 큰 차이 없음
# 
# 2. 실시간 기능이 필요한 사이트:
#    - 채팅 애플리케이션
#    - 실시간 알림 시스템
#    - 라이브 업데이트 대시보드
#    - 협업 도구 (구글 독스 같은)
#    → ASGI 필수 사용

# Django Channels와의 연관성:
# - Django Channels: Django에서 WebSocket 등을 지원하는 확장 패키지
# - Channels 사용시 routing.py 파일이 추가로 필요
# - asgi.py에서 HTTP와 WebSocket 라우팅을 모두 처리
# 
# Channels 사용시 asgi.py 예시:
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import myproject.routing
# 
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             myproject.routing.websocket_urlpatterns
#         )
#     ),
# })

# 개발 환경에서의 역할:
# - 개발 서버(python manage.py runserver) 실행시에는 직접 사용되지 않음
# - Django의 개발 서버가 내부적으로 ASGI/WSGI 처리
# - 배포시에만 이 파일이 직접 사용됨

# 환경 변수 설정의 중요성:
# - DJANGO_SETTINGS_MODULE이 설정되지 않으면 Django 실행 불가
# - 서로 다른 환경(개발/스테이징/프로덕션)에서 다른 설정 사용 가능
# - 도커 컨테이너, 클라우드 배포시 환경 변수로 설정 변경 가능