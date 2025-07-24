from django.shortcuts import render, redirect
from django.db import connection

def index(request):
    return render(request, 'index.html')

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

def in_notice(request):
    login_success = request.session.pop('login_success', False)
    return render(request, 'in_notice.html', {'login_success': login_success})