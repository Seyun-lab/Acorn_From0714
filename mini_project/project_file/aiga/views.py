from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
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


# 로그아웃
def logout(request):
    request.session.flush()  # 모든 세션 데이터 삭제
    return redirect('aiga:login')


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

        # 게시글 목록 가져오기
        cursor.execute("SELECT title FROM notes ORDER BY last_modified")
        posts = list()
        rows = cursor.fetchall()  # 리스트 형태로 게시글 제목들만
        for row in rows:
            posts.append({'title': row[0]}) # 딕셔너리 형태로 저장

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

        # 게시글 목록 가져오기
        cursor.execute("SELECT title FROM notes ORDER BY last_modified")
        posts = list()
        rows = cursor.fetchall()  # 리스트 형태로 게시글 제목들만
        for row in rows:
            posts.append({'title': row[0]}) # 딕셔너리 형태로 저장

    # GET 요청 시: 작성 폼 보여주기
    return render(request, 'in_notice.html', {
        'nickname': nickname,
        'posts': posts,
    })

def logout(request):
    request.session.flush()  # 모든 세션 데이터 삭제
    return redirect('aiga:login')

# 게시글 보기
def vi_notice(request, title):
    username = request.session['user']
    with connection.cursor() as cursor:
        cursor.execute("SELECT nickname FROM users WHERE username=%s", [username])
        user_data = cursor.fetchone()
        nickname = user_data[0]
        
    user_post = None
    error_message = None

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT n.title, n.content, u.nickname, n.note_id FROM notes n JOIN users u ON n.user_pid = u.pid WHERE n.title=%s", [title]) # notes 테이블과 users 테이블을 조인하여 title, content, nickname 컬럼 조회
            result = cursor.fetchone()
            if result:
                user_post = {'title': result[0], 'content': result[1], 'author': result[2]} # result[2]는 이제 nickname
                note_id = result[3]  # ← note_id를 여기서 꺼내세요!
            else:
                error_message = "게시글을 찾을 수 없습니다."

            # 게시글 목록 가져오기
            cursor.execute("SELECT title FROM notes ORDER BY last_modified")
            posts = list()
            rows = cursor.fetchall()  # 리스트 형태로 게시글 제목들만
            for row in rows:
                posts.append({'title': row[0]}) # 딕셔너리 형태로 저장

    except Exception as e:
        error_message = "게시글을 불러오는 중 오류가 발생했습니다."

    return render(request, 'vi_notice.html', {
        'nickname': nickname, 
        'user_post': user_post, 
        'error_message': error_message, 
        'posts': posts,
        'note_id': note_id,
        })

# 게시글 삭제
@csrf_protect
def delete_notice(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        if not note_id:
            return render(request, 'vi_notice.html', {'error': 'note_id가 필요합니다.'})
        # 현재 로그인한 유저 확인
        username = request.session.get('user')
        print("Current user:", username) # 확인
        if not username:
            return render(request, 'vi_notice.html', {'error': '로그인이 필요합니다.'})
        try:
            with connection.cursor() as cursor:
                # 유저의 pid 가져오기
                cursor.execute("SELECT pid FROM users WHERE username=%s", [username])
                user_row = cursor.fetchone()
                print("User row:", user_row)  # 확인
                if not user_row:
                    return render(request, 'vi_notice.html', {'error': '사용자 정보를 찾을 수 없습니다.'})
                user_pid = user_row[0]
                # 게시글의 user_pid 확인
                cursor.execute("SELECT user_pid FROM notes WHERE note_id=%s", [note_id])
                note_row = cursor.fetchone()
                print("note row:", note_row)  # 확인
                if not note_row:
                    return render(request, 'vi_notice.html', {'error': '게시글을 찾을 수 없습니다.'})
                note_pid = note_row[0]
                if user_pid != note_pid:
                    print("삭제 권한이 없습니다.")
                    # 게시글 정보와 목록 다시 조회
                    cursor.execute("SELECT n.title, n.content, u.nickname, n.note_id FROM notes n JOIN users u ON n.user_pid = u.pid WHERE n.note_id=%s", [note_id])
                    result = cursor.fetchone()
                    if result:
                        user_post = {'title': result[0], 'content': result[1], 'author': result[2]}
                        note_id_val = result[3]
                    else:
                        user_post = None
                        note_id_val = None
                    # 현재 로그인한 사용자의 nickname 조회
                    cursor.execute("SELECT nickname FROM users WHERE username=%s", [username])
                    user_nick_row = cursor.fetchone()
                    nickname_val = user_nick_row[0] if user_nick_row else None
                    cursor.execute("SELECT title FROM notes ORDER BY last_modified")
                    posts = [{'title': row[0]} for row in cursor.fetchall()]
                    return render(request, 'vi_notice.html', {
                        'nickname': nickname_val,
                        'user_post': user_post,
                        'error_message': '삭제 권한이 없습니다.',
                        'posts': posts,
                        'note_id': note_id_val,
                    })
                # 삭제
                cursor.execute("DELETE FROM notes WHERE note_id=%s", [note_id])
                connection.commit()
            return redirect('aiga:m_notice')
        except Exception as e:
            return render(request, 'vi_notice.html', {'error': str(e)})
    return render(request, 'vi_notice.html', {'error': 'POST 요청만 허용됩니다.'})

# 게시글 수정 폼 및 처리
@csrf_protect
def up_notice(request):
    # 현재 로그인한 유저 확인
    username = request.session.get('user')
    if not username:
        return render(request, 'vi_notice.html', {'error': '로그인이 필요합니다.'})
    if request.method == 'GET':
        note_id = request.GET.get('note_id')
        if not note_id:
            return render(request, 'vi_notice.html', {'error': 'note_id가 필요합니다.'})
        with connection.cursor() as cursor:
            # 유저의 pid 가져오기
            cursor.execute("SELECT pid FROM users WHERE username=%s", [username])
            user_row = cursor.fetchone()
            if not user_row:
                return render(request, 'vi_notice.html', {'error': '사용자 정보를 찾을 수 없습니다.'})
            user_pid = user_row[0]
            # 게시글 정보 및 user_pid 확인
            cursor.execute("SELECT title, content, user_pid FROM notes WHERE note_id=%s", [note_id])
            note = cursor.fetchone()
        if not note:
            return render(request, 'vi_notice.html', {'error': '게시글을 찾을 수 없습니다.'})
        print(user_pid, note[2])
        if user_pid != note[2]:
            # 게시글 목록 다시 조회
            with connection.cursor() as cursor:
                cursor.execute("SELECT title FROM notes ORDER BY last_modified")
                posts = [{'title': row[0]} for row in cursor.fetchall()]
                cursor.execute("SELECT nickname FROM users WHERE username=%s", [username])
                user_nick_row = cursor.fetchone()
                nickname_val = user_nick_row[0] if user_nick_row else None
            user_post = {'title': note[0], 'content': note[1], 'author': nickname_val}
            return render(request, 'vi_notice.html', {
                'nickname': nickname_val,
                'user_post': user_post,
                'error_message': '수정 권한이 없습니다.',
                'posts': posts,
                'note_id': note_id,
            })
        return render(request, 'up_notice.html', {
            'note_id': note_id,
            'title': note[0],
            'content': note[1],
        })
    elif request.method == 'POST':
        note_id = request.POST.get('note_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not (note_id and title):
            return render(request, 'up_notice.html', {'error': '제목을 입력하세요.', 'note_id': note_id, 'title': title, 'content': content})
        try:
            with connection.cursor() as cursor:
                # 유저의 pid 가져오기
                cursor.execute("SELECT pid FROM users WHERE username=%s", [username])
                user_row = cursor.fetchone()
                if not user_row:
                    return render(request, 'up_notice.html', {'error': '사용자 정보를 찾을 수 없습니다.', 'note_id': note_id, 'title': title, 'content': content})
                user_pid = user_row[0]
                # 게시글의 user_pid 확인
                cursor.execute("SELECT user_pid FROM notes WHERE note_id=%s", [note_id])
                note_row = cursor.fetchone()
                if not note_row:
                    return render(request, 'up_notice.html', {'error': '게시글을 찾을 수 없습니다.', 'note_id': note_id, 'title': title, 'content': content})
                note_pid = note_row[0]
                if user_pid != note_pid:
                    return render(request, 'up_notice.html', {'error': '수정 권한이 없습니다.', 'note_id': note_id, 'title': title, 'content': content})
                # 수정
                cursor.execute("UPDATE notes SET title=%s, content=%s, last_modified=NOW() WHERE note_id=%s", [title, content, note_id])
                connection.commit()
            return redirect('aiga:m_notice')
        except Exception as e:
            return render(request, 'up_notice.html', {'error': str(e), 'note_id': note_id, 'title': title, 'content': content})
    return render(request, 'vi_notice.html', {'error': '잘못된 요청입니다.'})