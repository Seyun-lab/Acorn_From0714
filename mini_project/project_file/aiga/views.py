from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # settings.py에서 DB 정보 불러오기
from django.utils import timezone
import MySQLdb  # mysqlclient 사용
import json
import uuid
from datetime import datetime


# 시작 페이지
def index(request):
    return render(request, 'index.html')

# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        with connection.cursor() as cursor:
            # ID 존재 여부 확인
            cursor.execute("SELECT * FROM users WHERE username=%s", [username])
            user = cursor.fetchone()
            if not user:
                return render(request, 'login.html', {'error': '존재하지 않는 ID입니다.'})
            # PW 일치 여부 확인
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", [username, password])
            user_pw = cursor.fetchone()
            if user_pw:
                # 로그인 성공 (세션 처리 등)
                request.session['user'] = username
                request.session['login_success'] = True
                return redirect('aiga:m_notice')  # 로그인 성공 후 m_notice.html로 이동
            else:
                return render(request, 'login.html', {'error': '비밀번호가 올바르지 않습니다.'})
    return render(request, 'login.html')

# 회원가입
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        with connection.cursor() as cursor:
            # ID 중복 확인
            cursor.execute("SELECT * FROM users WHERE username=%s", [username])
            if cursor.fetchone():
                return render(request, 'register.html', {'error': '이미 존재하는 ID입니다.'})
            # 사용자 등록 (pid는 UUID)
            pid = str(uuid.uuid4())
            cursor.execute("INSERT INTO users (pid, username, password, nickname) VALUES (%s, %s, %s, %s)", [pid, username, password1, nickname])
            connection.commit()
            return redirect('aiga:login')  # 등록 후 로그인 페이지로 이동
    return render(request, 'register.html')

# 게시글 페이지
def m_notice(request):
    return render(request, 'm_notice.html')



# DB 연결 처리 예시 ----------------------------------------------------------------

# DB 연결 함수 (mysqlclient)
def get_connection():
    db = settings.DATABASES['default']
    return MySQLdb.connect(
        user=db['USER'],
        passwd=db['PASSWORD'],
        host=db['HOST'],
        port=int(db['PORT']),
        db=db['NAME'],
        charset='utf8'
    )

@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = int(data.get('name'))
        number = int(data.get('number'))
        try:
            conn = get_connection()
            cur = conn.cursor()
            # mysqlclient는 %s를 사용
            cur.execute("INSERT INTO psy (name, number) VALUES (%s, %s)", (name, number))
            conn.commit()
            cur.close()
            conn.close()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def get_data(request):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM psy")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        data = [{'name': r[0], 'number': r[1]} for r in rows]
        return JsonResponse({'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})  