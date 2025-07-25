from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # settings.py에서 DB 정보 불러오기
import MySQLdb  # mysqlclient 사용
import json
import uuid
import datetime


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
    if 'user' not in request.session:
        return redirect('aiga:login')  # 비로그인 사용자는 로그인 페이지로 리다이렉트

    username = request.session['user']
    with connection.cursor() as cursor:
        # 닉네임 가져오기
        cursor.execute("SELECT nickname, pid FROM users WHERE username = %s", [username])
        user_data = cursor.fetchone()
        if not user_data:
            return redirect('aiga:login')

        nickname, user_pid = user_data

        # 해당 유저의 게시글 가져오기
        cursor.execute("SELECT title FROM notes WHERE user_pid = %s ORDER BY last_modified DESC", [user_pid])
        posts = cursor.fetchall()  # 리스트 형태로 게시글 제목들만

    return render(request, 'm_notice.html', {
        'nickname': nickname,
        'posts': posts,
    })


# 게시글 작성
@csrf_exempt
def in_notice(request):
    if request.method == 'POST':
        if not request.session.get('user'):
            return render(request, 'login.html', {'error': '로그인이 필요합니다.'})

        title = request.POST.get('title')
        content = request.POST.get('content')
        username = request.session['user']

        with connection.cursor() as cursor:
            cursor.execute("SELECT nickname, pid FROM users WHERE username=%s", [username])
            user_data = cursor.fetchone()
            if not user_data:
                return render(request, 'in_notice.html', {'error': '사용자 정보를 찾을 수 없습니다.'})

            nickname, user_pid = user_data
            note_id = str(uuid.uuid4())
            now = datetime.datetime.now()

            cursor.execute(
                "INSERT INTO notes (note_id, title, content, last_modified, user_pid) VALUES (%s, %s, %s, %s, %s)",
                [note_id, title, content, now, user_pid]
            )
            connection.commit()

        return redirect('aiga:m_notice')  # 게시글 목록 페이지로 리다이렉트
    
    username = request.session['user']
    with connection.cursor() as cursor:
        cursor.execute("SELECT nickname FROM users WHERE username=%s", [username])
        user_data = cursor.fetchone()
        nickname = user_data[0]

    # GET 요청 시: 작성 폼 보여주기
    return render(request, 'in_notice.html', {
        'nickname': nickname,
    })

def logout(request):
    request.session.flush()  # 모든 세션 데이터 삭제
    return redirect('aiga:login')

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
