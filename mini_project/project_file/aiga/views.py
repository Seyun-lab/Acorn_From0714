# myapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # settings.py에서 DB 정보 불러오기
import json
import MySQLdb  # mysqlclient 사용
 
 
def index(request):
    return render(request, 'index.html')

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
