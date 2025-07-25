# Acorn_From0714 레포지토리

## 가상환경 셋업
# 가상 환경 생성
python -m venv venv
.\venv\Scripts\activate
# 라이브러리 설치 패키지
pip install -r requirements.txt
# manage.py 파일이있는 경로로 이동
cd C:\Users\SeYun\Acorn_From0714\mini_project\project_file
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

## 적용돼있는 기능
<DB>
데이터베이스: mydb , 테이블: psy
<UI UX>
숫자 입력 -> html에서 DB 올라감 -> out 버튼->DB에서 html로 빼옴