# Django의 URL 패턴 정의를 위한 path 함수를 가져옵니다
from django.urls import path

# 현재 디렉토리(blog 앱)의 views.py 파일에서 정의한 모든 뷰 함수들을 가져옵니다
# '.' 은 현재 디렉토리를 의미합니다 (blog/views.py)
from . import views

# URL 패턴들을 정의하는 리스트입니다
# Django는 이 리스트를 순서대로 확인하여 요청받은 URL과 일치하는 패턴을 찾습니다
urlpatterns = [
    
    # URL 패턴의 기본 구조: path('URL패턴', 뷰함수, name='URL이름')
    # 'URL패턴': 브라우저에서 입력하는 주소 경로
    # 뷰함수: 해당 URL로 요청이 들어왔을 때 실행할 함수
    # name: 템플릿이나 다른 곳에서 이 URL을 참조할 때 사용하는 별명(html 파일)
    
    # 루트 페이지 (홈페이지)
    # URL: http://도메인/ (아무것도 입력하지 않은 기본 페이지)
    # 실행: views.py의 index 함수 호출
        # views.py의 index(request) 함수는
        # templates/blog/index.html 파일을 렌더링합니다(최초 페이지 렌더링)
    # 별명: 'index' (템플릿에서 {% url 'index' %}로 참조 가능)
    path('', views.index, name='index'),
    
    # 게시물 목록 페이지
    # URL: http://도메인/posts/ (모든 게시글 목록을 보여주는 페이지)
    # 실행: views.py의 posts_view 함수 호출
        # views.py의 posts_view(request) 함수는
        # templates/blog/posts.html 파일을 렌더링합니다(게시글 목록 렌더링)
    # 별명: 'posts' (템플릿에서 {% url 'posts' %}로 참조 가능)
    path('posts/', views.posts_view, name='posts'),
    
    # 개별 게시물 상세 페이지
    # URL: http://도메인/post/5/ (5번 게시글의 상세 내용을 보여주는 페이지)
    # <int:pk>: URL에서 정수값(int)을 받아서 'pk'라는 변수로 뷰 함수에 전달
    #           예: post/1/ → pk=1, post/25/ → pk=25
    # 실행: views.py의 post_detail_view(request, pk) 함수 호출
        # views.py의 post_detail_view(request, pk) 함수는
        # templates/blog/post_detail.html 파일을 렌더링합니다(게시글 상세 페이지 렌더링)
        # pk: 게시글의 Primary Key (고유 ID)로, 데이터베이스에서 해당 게시글을 찾는 데 사용
    # 별명: 'post_detail' (템플릿에서 {% url 'post_detail' post.pk %}로 참조 가능)
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    
    # 새 게시물 작성 페이지
    # URL: http://도메인/post/create/ (새로운 게시글을 작성하는 폼 페이지)
    # 실행: views.py의 post_create_view 함수 호출
    # 별명: 'post_create' (템플릿에서 {% url 'post_create' %}로 참조 가능)
    # 주의: 이 URL은 <int:pk> 패턴보다 아래에 있어야 함 (순서 중요!)
        # 왜? Django는 URL 패턴을 위에서부터 순서대로 확인하기 때문에
        # 만약 'post/create/'가 <int:pk>보다 위에 있으면
        # 모든 'post/숫자/' URL이 이 패턴으로 인식되어
        # 게시글 작성 페이지로 잘못 연결될 수 있습니다
        # 따라서, 'post/create/'는 <int:pk> 패턴보다 아래에 위치해야 합니다
    path('post/create/', views.post_create_view, name='post_create'),
    
    # 기존 게시물 수정 페이지
    # URL: http://도메인/post/5/edit/ (5번 게시글을 수정하는 폼 페이지)
    # <int:pk>: 수정할 게시글의 ID를 받아서 'pk' 변수로 뷰 함수에 전달
    #           예: post/3/edit/ → pk=3을 post_edit_view 함수에 전달
    # 실행: views.py의 post_edit_view(request, pk) 함수 호출
        # views.py의 post_edit_view(request, pk) 함수는
        # templates/blog/post_edit.html 파일을 렌더링합니다(게시글 수정 페이지 렌더링)
        # pk: 수정할 게시글의 Primary Key (고유 ID)로, 데이터베이스에서 해당 게시글을 찾는 데 사용
    # 주의: 이 URL은 <int:pk> 패턴보다 아래에 있어야 함 (순서 중요!)
        # 이유는 위의 'post/create/'와 동일합니다
        # 만약 'post/<int:pk>/edit/'가 <int:pk>보다 위에 있으면
        # 모든 'post/숫자/' URL이 이 패턴으로 인식되어
        # 게시글 수정 페이지로 잘못 연결될 수 있습니다
    # 별명: 'post_edit' (템플릿에서 {% url 'post_edit' post.pk %}로 참조 가능)
    path('post/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
]

# URL 매칭 과정 예시:
# 1. 사용자가 브라우저에 '/posts/' 입력
# 2. Django가 urlpatterns 리스트를 위에서부터 순서대로 확인
# 3. 'posts/' 패턴과 일치하는 두 번째 path 발견
# 4. views.posts_view 함수 실행
# 5. 함수 결과를 브라우저에 전송

# <int:pk> 매개변수 설명:
# - <int:pk>는 Django의 URL 컨버터입니다
# - int: 정수만 허용 (문자열이나 다른 타입은 매칭되지 않음)
# - pk: 뷰 함수의 매개변수 이름 (Primary Key의 줄임말)
# - 예: post/123/ → pk=123이 뷰 함수로 전달됨
# - 예: post/abc/ → 매칭 실패 (abc는 정수가 아님)

# name 매개변수의 활용:
# 템플릿에서 하드코딩된 URL 대신 name을 사용할 수 있습니다
# 하드코딩: <a href="/post/{{ post.pk }}/">게시글 보기</a>
# name 사용: <a href="{% url 'post_detail' post.pk %}">게시글 보기</a>
# 장점: URL 구조가 바뀌어도 name만 그대로 두면 템플릿 수정 불필요