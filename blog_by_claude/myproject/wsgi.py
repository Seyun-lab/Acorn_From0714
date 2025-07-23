"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# os 모듈: 운영체제와 상호작용하기 위한 Python 표준 라이브러리
# 환경 변수 설정, 파일 시스템 접근 등에 사용
import os

# Django의 WSGI 애플리케이션을 생성하는 함수를 가져옵니다
# WSGI: Web Server Gateway Interface
# - 웹 서버와 Python 웹 애플리케이션 간의 표준 인터페이스
# - 동기식 처리 방식 (한 번에 하나의 요청만 처리)
# - HTTP 요청/응답만 처리 가능
# - 전통적인 웹 애플리케이션의 표준 방식
from django.core.wsgi import get_wsgi_application

# 환경 변수 'DJANGO_SETTINGS_MODULE' 설정
# os.environ.setdefault(): 환경 변수가 이미 설정되어 있지 않은 경우에만 기본값 설정
# 'DJANGO_SETTINGS_MODULE': Django가 어떤 설정 파일을 사용할지 지정하는 환경 변수
# 'myproject.settings': myproject/settings.py 파일을 사용하도록 지정
# 
# 용도:
# - Django가 시작될 때 어떤 설정을 로드할지 알려줌
# - 개발/테스트/배포 환경별로 다른 설정 파일 사용 가능
# - 예: 'myproject.settings.production', 'myproject.settings.development'
# 
# 설정 과정:
# 1. 환경 변수에 DJANGO_SETTINGS_MODULE이 있는지 확인
# 2. 없다면 기본값 'myproject.settings' 사용
# 3. 있다면 기존 값 유지 (다른 환경에서 다른 설정 사용 가능)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Django WSGI 애플리케이션 인스턴스 생성
# get_wsgi_application(): Django 프로젝트를 WSGI 호환 애플리케이션으로 변환
# application: WSGI 서버(Apache, Gunicorn 등)에서 호출할 수 있는 애플리케이션 객체
# 
# 역할:
# 1. HTTP 요청을 받아서 Django로 전달
# 2. Django에서 처리한 응답을 웹 서버로 반환
# 3. 미들웨어 체인 실행
# 4. URL 라우팅 및 뷰 함수 실행 관리
application = get_wsgi_application()

# WSGI의 작동 원리:
# 
# 1. 웹 서버(Apache, Nginx)가 HTTP 요청 수신
# 2. WSGI 서버(Gunicorn, uWSGI)가 요청을 Python 형태로 변환
# 3. application 객체를 호출하여 Django에 요청 전달
# 4. Django가 요청을 처리하고 응답 생성
# 5. WSGI 서버가 응답을 HTTP 형태로 변환하여 웹 서버로 전달
# 6. 웹 서버가 클라이언트에게 최종 응답 전송

# 배포시 WSGI 서버 사용 예시:
# 
# 1. Gunicorn (가장 일반적):
#    gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
#    gunicorn myproject.wsgi:application --workers 4 --bind unix:/tmp/gunicorn.sock
# 
# 2. uWSGI:
#    uwsgi --http :8000 --module myproject.wsgi:application
#    uwsgi --socket /tmp/uwsgi.sock --module myproject.wsgi:application
# 
# 3. Apache + mod_wsgi:
#    WSGIScriptAlias / /path/to/myproject/wsgi.py
#    WSGIDaemonProcess myproject python-path=/path/to/myproject

# WSGI vs ASGI 차이점:
# 
# WSGI (현재 파일):
# ✅ 장점:
#    - 성숙하고 안정적인 기술
#    - 대부분의 웹 호스팅에서 지원
#    - 풍부한 서버 옵션 (Apache, Nginx + Gunicorn 등)
#    - 일반적인 웹사이트에 충분한 성능
# ❌ 단점:
#    - 동기식 처리만 가능
#    - WebSocket, HTTP/2 지원 불가
#    - 실시간 기능 구현 어려움
# 
# ASGI:
# ✅ 장점:
#    - 비동기 처리 지원
#    - WebSocket, HTTP/2, Server-Sent Events 지원
#    - 실시간 기능 구현 가능
#    - 미래 지향적 기술
# ❌ 단점:
#    - 상대적으로 새로운 기술 (안정성 검증 중)
#    - 제한적인 호스팅 지원
#    - 복잡한 설정

# 언제 WSGI를 사용해야 하는가?
# 
# ✅ WSGI 사용 권장:
# - 일반적인 블로그, 쇼핑몰, 회사 홈페이지
# - 실시간 기능이 필요 없는 웹사이트
# - 안정적이고 검증된 배포 환경이 필요한 경우
# - 대부분의 Django 프로젝트
# 
# ✅ ASGI 사용 권장:
# - 채팅 애플리케이션
# - 실시간 협업 도구
# - 라이브 스트리밍 플랫폼
# - 실시간 알림 시스템
# - IoT 데이터 모니터링

# 개발 환경에서의 역할:
# - 개발 서버(python manage.py runserver) 실행시에는 직접 사용되지 않음
# - Django의 개발 서버가 내부적으로 WSGI 처리를 담당
# - 배포시에만 이 wsgi.py 파일이 직접 사용됨
# - 로컬 개발중에는 존재만 하고 실제로는 호출되지 않음

# 일반적인 배포 아키텍처:
# 
# 인터넷 → Nginx (리버스 프록시) → Gunicorn (WSGI 서버) → Django (wsgi.py)
# 
# 각 구성 요소의 역할:
# - Nginx: 정적 파일 서빙, SSL 처리, 로드 밸런싱
# - Gunicorn: Python 코드 실행, 워커 프로세스 관리
# - Django: 비즈니스 로직 처리, 데이터베이스 연동

# 환경별 설정 예시:
# 
# 개발 환경:
# export DJANGO_SETTINGS_MODULE=myproject.settings.development
# 
# 스테이징 환경:
# export DJANGO_SETTINGS_MODULE=myproject.settings.staging
# 
# 프로덕션 환경:
# export DJANGO_SETTINGS_MODULE=myproject.settings.production

# wsgi.py 파일이 하는 일 요약:
# 1. Django 설정 모듈 지정
# 2. Django 애플리케이션을 WSGI 호환 형태로 래핑
# 3. 웹 서버와 Django 사이의 인터페이스 제공
# 4. 배포시 진입점(entry point) 역할 수행