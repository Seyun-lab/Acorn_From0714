# --------------------- forms.py 설명 ---------------------
# 입력부터 출력까지 데이터가 주고 받는 형태와 구조를 정의(설계도)
# 어떻게 사용자가 입력한 데이터를 입력 받을까?
# 어떻게 함수에 데이터를 넘겨줄까?
# 어떻게 DB안에 저장하고 다시 꺼내와서 사용자에게 보여줄까?
# ------------------------------------------------------------------


# Django의 폼(Form) 기능을 사용하기 위한 forms 모듈을 가져옵니다
# 이 모듈에는 ModelForm, CharField, TextInput 등 폼 관련 클래스들이 포함되어 있습니다
from django import forms

# 현재 앱의 models.py에서 Post 모델을 가져옵니다
# '.'은 현재 디렉토리(blog 앱)를 의미합니다
from .models import Post

# PostForm 클래스는 Django의 ModelForm을 상속받습니다
# ModelForm: 기존 모델을 기반으로 자동으로 폼을 생성하는 Django의 특별한 폼 클래스
# 장점: 모델의 필드 정의를 재사용하여 중복 코드를 줄이고 일관성 유지
class PostForm(forms.ModelForm):
    
    # Meta 클래스는 ModelForm의 설정을 정의하는 내부 클래스입니다
    # 여기서 어떤 모델을 사용할지, 어떤 필드를 포함할지 등을 설정합니다
    class Meta:
        
        # 이 폼이 기반으로 할 모델을 지정합니다
        # Post 모델의 필드 구조를 참조하여 폼 필드를 자동 생성합니다
        model = Post
        
        # 폼에 포함할 모델 필드들을 리스트로 지정합니다
        # ['title', 'content']: Post 모델의 title과 content 필드만 폼에 포함
        # 포함되지 않은 필드들:
        #   - author: 사용자가 직접 선택하지 않고 views.py에서 자동으로 설정
        #   - created_at: auto_now_add=True로 자동 설정
        #   - updated_at: auto_now=True로 자동 설정
        fields = ['title', 'content']
        
        # widgets: HTML 폼 요소의 모양과 속성을 사용자 정의하는 딕셔너리
        # 각 필드가 HTML에서 어떻게 렌더링될지를 세밀하게 제어할 수 있습니다
        widgets = {
            # 'title' 필드에 대한 위젯 설정
            # forms.TextInput: HTML의 <input type="text"> 요소를 생성
            # attrs: HTML 요소에 추가할 속성들을 딕셔너리로 지정
            'title': forms.TextInput(attrs={
                'class': 'form-control',           # Bootstrap CSS 클래스 적용 (스타일링용)
                'placeholder': '제목을 입력하세요'    # 입력 필드에 표시할 힌트 텍스트
            }),
            
            # 'content' 필드에 대한 위젯 설정
            # forms.Textarea: HTML의 <textarea> 요소를 생성 (여러 줄 텍스트 입력용)
            'content': forms.Textarea(attrs={
                'class': 'form-control',           # Bootstrap CSS 클래스 적용
                'rows': 10,                       # textarea의 높이를 10줄로 설정
                'placeholder': '내용을 입력하세요'   # 텍스트 영역에 표시할 힌트 텍스트
            }),
        }

# 생성되는 HTML 예시:
# <input type="text" 
#        name="title" 
#        class="form-control" 
#        placeholder="제목을 입력하세요" 
#        maxlength="200" 
#        required 
#        id="id_title">
#
# <textarea name="content" 
#           class="form-control" 
#           rows="10" 
#           placeholder="내용을 입력하세요" 
#           required 
#           id="id_content">
# </textarea>

# ModelForm vs 일반 Form의 차이점:
# 
# ModelForm 사용시 (현재 코드):
# - 모델 필드 정의 재사용
# - 유효성 검사 자동 적용 (max_length=200 등)
# - form.save() 메서드 자동 제공
# - 코드 간결함
#
# 일반 Form 사용시:
# - 모든 필드를 수동으로 정의해야 함
# - 유효성 검사 규칙을 수동으로 작성해야 함
# - 저장 로직을 수동으로 구현해야 함
# - 더 많은 코드 필요

# 폼 사용 과정:
# 1. views.py에서 PostForm() 인스턴스 생성
# 2. 템플릿에서 {{ form.as_p }} 또는 개별 필드로 렌더링
# 3. 사용자가 폼 작성 후 제출
# 4. views.py에서 PostForm(request.POST)로 데이터 받아서 처리
# 5. form.is_valid()로 유효성 검사 후 form.save()로 저장

# Bootstrap 클래스 'form-control'의 역할:
# - 입력 필드의 스타일을 Bootstrap 테마에 맞게 설정
# - 반응형 디자인 지원 (모바일, 태블릿, 데스크탑에서 적절한 크기)
# - 포커스, 호버 효과 등 사용자 경험