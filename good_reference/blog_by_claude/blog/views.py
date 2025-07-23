# 기본 Django 뷰 설정
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# 추가된 모듈
from .models import Post # Post 모델을 가져옵니다.
from .forms import PostForm # PostForm을 가져옵니다.

# Create your views here.

# 루트 페이지 뷰 함수
def index(request): # 루트 페이지를 렌더링하는 함수
    return render(request, 'blog/index.html') # templates/blog/index.html 파일을 렌더링합니다.

# 로그인 페이지 뷰 함수
def login_view(request): # 로그인 페이지를 렌더링하는 함수
    return render(request, 'registration/login.html') # templates/registration/login.html 파일을 렌더링합니다.

# 회원가입 페이지 뷰 함수
def signup_view(request): # 회원가입 페이지를 렌더링하는 함수
    if request.method == 'POST': # POST 요청이 들어오면
        form = UserCreationForm(request.POST) # UserCreationForm을 사용하여 폼을 생성합니다.
        if form.is_valid(): # 폼이 유효하면
            user = form.save() # 사용자 계정을 저장합니다.
            username = form.cleaned_data.get('username') # 사용자 이름을 가져옵니다.
            messages.success(request, f'계정이 생성되었습니다: {username}!') # 성공 메시지를 추가합니다.
            login(request, user) # 로그인합니다.
            return redirect('index') # 인덱스 페이지로 리다이렉트합니다.
    else:
        form = UserCreationForm() # GET 요청이면 빈 폼을 생성합니다.
    return render(request, 'registration/signup.html', {'form': form}) # 회원가입 페이지를 렌더링합니다.

# 게시글 보기 페이지 뷰 함수
def posts_view(request): # 게시글 목록 페이지를 렌더링하는 함수
    posts = Post.objects.all().order_by('-created_at') # 모든 게시글을 가져와서 생성일 기준으로 내림차순 정렬합니다.
    return render(request, 'blog/posts.html', {'posts': posts}) # 게시글 목록을 렌더링합니다.

#------------------------- 게시글 생성, 수정, 상세 페이지 뷰 함수들 -------------------------
@login_required # 로그인한 사용자만 접근 가능
def post_create_view(request): # 게시글 생성 페이지 뷰 함수
    # 사용자가 폼을 작성하고 나서 "저장 버튼을 눌렀을 때의 처리"
    if request.method == 'POST': # POST 요청이 들어오면
        form = PostForm(request.POST) # 사용자가 입력한 데이터(request.POST)를 포함한 폼을 생성합니다.
        # form.is_vaild() 메서드는 폼의 유효성을 검사
        # 필수 필드가 모두 입력되었는지
        # 데이터 형식이 올바른지(숫자 필드에 문자가 들어가진 않았는 지)
        # 글자 수 제한을 지켰는지
        # 기타 유효성 검사 규칙을 통해 폼이 유효한지 확인
        if form.is_valid():
            # 폼이 유효하면, 데이터를 저장함
            # 1단계: form.save()로 post에 반영 후 commit=False로 메모리에만 임시 저장
            # 2단계: post의 author 필드는 공란인 상태이므로, request.user로 사용자를 전달 받음
            # 3단계: post.save()로 DB에 저장
            post = form.save(commit=False) # (form.save)폼 데이터를 저장하되, (commit=False)메모리에만 저장, DB에는 미 반영
            post.author = request.user # 현재 로그인한 사용자(request.user)를 게시글 작성자(post.author)로 설정합니다.
            post.save() # 게시글을 데이터베이스에 저장합니다.
            # 방금 작성한 게시글의 DB에 저장된 pk 값(post.pk)을 사용하여
            # 방금 작성한 게시글의 상세 페이지로 이동함(리다이렉트)
            # 기존 페이지 url에서 새로운 페이지의 url로 이동함 이후 밑에 render를 통해서 
            return redirect('post_detail', pk=post.pk) # 방금 작성한 게시글의 상세 페이지로 리다이렉트합니다.
    else: # 사용자가 처음 페이지에 접속했을 때
        form = PostForm() # GET 요청이면 빈 폼을 생성합니다.
    # redirect()와 reender()의 차이점
    return render(request, 'blog/post_create.html', {'form': form}) # 게시글 생성 페이지를 렌더링합니다.

def post_detail_view(request, pk): # 게시글 상세 페이지 뷰 함수
    post = get_object_or_404(Post, pk=pk) # 주어진 pk에 해당하는 게시글을 가져옵니다. 게시글이 없으면 404 에러를 발생시킵니다.
    # 삭제 요청 처리
    if request.method == 'POST' and request.POST.get('delete'): # 삭제 버튼이 눌렸을 때
        if post.author == request.user: # 현재 로그인한 사용자가 게시글 작성자일 때만 삭제 가능
            post.delete() # 게시글을 삭제합니다.
            messages.success(request, '게시글이 삭제되었습니다.') # 성공 메시지를 추가합니다.
            return redirect('posts') # 게시글 목록 페이지로 리다이렉트합니다.
        else: # 작성자가 아닐 경우
            messages.error(request, '본인의 게시글만 삭제할 수 있습니다.') # 작성자가 아닐 경우 에러 메시지를 추가합니다.
    
    return render(request, 'blog/post_detail.html', {'post': post}) # 게시글 상세 페이지를 렌더링합니다.

# 게시글 수정 페이지 뷰 함수
@login_required # 로그인한 사용자만 접근 가능
def post_edit_view(request, pk): # 게시글 수정 페이지 뷰 함수
    post = get_object_or_404(Post, pk=pk) # 주어진 pk에 해당하는 게시글을 가져옵니다. 게시글이 없으면 404 에러를 발생시킵니다.
    
    # 보안 처리
    if post.author != request.user: # 현재 로그인한 사용자가 게시글 작성자가 아닐 때
        messages.error(request, '본인의 게시글만 수정할 수 있습니다.') # 에러 메시지를 추가합니다.
        return redirect('post_detail', pk=pk) # 게시글 상세 페이지로 리다이렉트합니다.

    # 게시글 수정 폼 처리
    if request.method == 'POST': # POST 요청이 들어오면(기존 게시글 수정 요청)
        # instance=post는 기존 게시글 데이터를 포함하여 폼을 생성합니다.(수정을 위해서)
        form = PostForm(request.POST, instance=post) # PostForm을 사용하여 폼을 생성합니다. 기존 게시글 데이터를 포함합니다.
        if form.is_valid(): # 폼이 유효하면
            # 이미 상단에서 게시글의 작성자임을 확인했으므로, 추가적인 작성자 설정(post.author = request.user)은 필요하지 않습니다
            form.save() # 폼 데이터를 저장합니다.
            return redirect('post_detail', pk=pk) # 게시글 상세 페이지로 리다이렉트합니다.
    else:
        # instance=post는 기존 게시글 데이터를 포함하여 폼을 생성합니다.
        form = PostForm(instance=post) # GET 요청이면 기존 게시글 데이터를 포함한 폼을 생성합니다.
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post}) # 게시글 수정 페이지를 렌더링합니다.
