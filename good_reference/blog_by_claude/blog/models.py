# Django의 데이터베이스 모델을 정의하기 위한 models 모듈
# 이 모듈에는 CharField, TextField, DateTimeField 등 다양한 필드 타입이 포함
from django.db import models

# Django에서 기본 제공하는 사용자(User) 모델
# 이 User 모델은 username, email, password 등 사용자 정보를 저장
from django.contrib.auth.models import User

# URL 패턴 이름으로부터 실제 URL을 생성하는 reverse 함수를 가져옴
# 예: reverse('post_detail', kwargs={'pk': 1}) → '/post/1/' 형태의 URL 생성
from django.urls import reverse

# Create your models here.

# --------------------------- 블로그 게시글 모델(DB) 정의 ---------------------------
# Post 클래스는 Django의 Model을 상속받아 데이터베이스 테이블을 정의합니다
# 이 클래스는 블로그 게시글의 구조와 동작을 정의합니다
# Django는 이 클래스를 기반으로 'blog_post' 테이블을 데이터베이스에 생성합니다
class Post(models.Model):
    
    # 게시글 제목을 저장하는 필드
    # CharField: 짧은 문자열을 저장하는 필드 (HTML의 input type="text"와 유사)
    # max_length=200: 제목은 최대 200자까지 입력 가능
    # 데이터베이스에서는 VARCHAR(200) 타입으로 생성됩니다
    title = models.CharField(max_length=200)
    
    # 게시글 내용을 저장하는 필드
    # TextField: 긴 문자열을 저장하는 필드 (HTML의 textarea와 유사)
    # 글자 수 제한이 없어 긴 게시글 내용 저장 가능
    # 데이터베이스에서는 TEXT 타입으로 생성
    content = models.TextField()
    
    # 게시글 작성자를 저장하는 필드
    # ForeignKey: 다른 모델과의 다대일(Many-to-One) 관계를 나타냅니다
    # User: Django의 기본 사용자 모델과 연결 (한 사용자가 여러 게시글 작성 가능)
    # on_delete=models.CASCADE: 사용자가 삭제되면 해당 사용자의 모든 게시글도 자동 삭제
    #   - CASCADE: 연결된 객체가 삭제되면 이 객체도 함께 삭제
    #   - 다른 옵션들: PROTECT(삭제 방지), SET_NULL(NULL로 설정) 등
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 게시글이 처음 생성된 날짜와 시간을 자동으로 저장하는 필드
    # DateTimeField: 날짜와 시간을 저장하는 필드
    # auto_now_add=True: 객체가 처음 생성될 때만 현재 시간으로 자동 설정
    #   - 한번 설정되면 수정되지 않음 (게시글 최초 작성 시간 기록용)
    #   - 예: 2024-01-15 14:30:25
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 게시글이 마지막으로 수정된 날짜와 시간을 자동으로 저장하는 필드
    # auto_now=True: 객체가 저장될 때마다 현재 시간으로 자동 업데이트
    #   - 게시글을 수정할 때마다 최신 시간으로 갱신됨
    #   - 게시글 수정 시간 추적용
    updated_at = models.DateTimeField(auto_now=True)
    
    # 객체를 문자열로 표현할 때 사용되는 특수 메서드
    # Django Admin 페이지나 쉘에서 Post 객체를 출력할 때 제목이 표시됩니다
    # 예: print(post) → "Django 튜토리얼" (게시글 제목)
    # 이 메서드가 없으면 "Post object (1)" 같은 의미없는 문자열이 표시됩니다
    def __str__(self):
        return self.title
    
    # 해당 게시글의 상세 페이지 URL을 반환하는 메서드
    # get_absolute_url: Django에서 객체의 기본 URL을 정의하는 관례적 메서드 이름
    # reverse: URL 패턴 이름('post_detail')을 실제 URL로 변환
    # kwargs={'pk': self.pk}: URL 패턴에 필요한 매개변수 전달
    #   - 'pk': urls.py의 <int:pk> 부분에 해당
    #   - self.pk: 현재 게시글 객체의 Primary Key (고유 ID)
    # 예: 3번 게시글의 경우 '/post/3/' URL 반환
    # 사용 예시: 템플릿에서 {{ post.get_absolute_url }}로 링크 생성 가능
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

# 데이터베이스 관계 설명:
# User 모델 (1) ←→ Post 모델 (다)
# - 한 명의 사용자(User)는 여러 개의 게시글(Post)을 작성할 수 있습니다
# - 하나의 게시글(Post)은 한 명의 사용자(User)에게만 속합니다
# - 이를 "일대다(One-to-Many)" 또는 "다대일(Many-to-One)" 관계라고 합니다

# 마이그레이션 과정:
# 1. python manage.py makemigrations: 모델 변경사항을 마이그레이션 파일로 생성
# 2. python manage.py migrate: 실제 데이터베이스에 테이블 생성/수정 적용

# 생성되는 데이터베이스 테이블 구조 (blog_post):
# +------------+------------------+------+-----+---------+----------------+
# | Field      | Type             | Null | Key | Default | Extra          |
# +------------+------------------+------+-----+---------+----------------+
# | id         | int(11)          | NO   | PRI | NULL    | auto_increment |
# | title      | varchar(200)     | NO   |     | NULL    |                |
# | content    | longtext         | NO   |     | NULL    |                |
# | author_id  | int(11)          | NO   | MUL | NULL    |                |
# | created_at | datetime(6)      | NO   |     | NULL    |                |
# | updated_at | datetime(6)      | NO   |     | NULL    |                |
# +------------+------------------+------+-----+---------+----------------+