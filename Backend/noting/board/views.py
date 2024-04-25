from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Post
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import jwt
import json



def index(request):
    # JSON 데이터 생성
    data = {'msg': 'Hello, World!'}

    # JsonResponse 객체 생성하여 JSON 데이터 반환
    return JsonResponse(data)

def allMemo(req):
    posts = Post.objects.filter(isDelete=0).values()
    response_data = []

    for post in posts:
        post_data = {
            "id": post['id'],
            "writer": post['writer'],
            "title": post['title'],
            "content": post['content'],
            "writetime": post['writetime'],
        }
        response_data.append(post_data)

    print(response_data)
    return JsonResponse(response_data, safe=False)

@csrf_exempt
def uploadPost(req):
    data = json.loads(req.body)
    writer = data.get('writer')
    title = data.get('title')
    content = data.get('content')
    post = Post(writer = writer, title=title, content=content)
    post.save()
    return JsonResponse({"msg" : "Hello"})

@csrf_exempt
def Login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 로그인 성공 시 토큰 생성
            token = jwt.encode({'username': username}, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token})
        else:
            return JsonResponse({"logined": False})


@login_required
def pf(req):
    # 클라이언트로부터 JWT 토큰 받기
    jwt_token = req.COOKIES.get('jwt_token')
    if jwt_token:
        try:
            # JWT 토큰 해독하여 사용자 정보 확인
            payload = jwt.decode(jwt_token, 'SECRET_KEY', algorithms=['HS256'])
            username = payload['username']
            # 사용자 정보 반환
            return JsonResponse({"username": username})
        except jwt.ExpiredSignatureError:
            # 토큰 만료
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            # 잘못된 토큰
            return JsonResponse({"error": "Invalid token"}, status=401)
    else:
        # 토큰이 없음
        return JsonResponse({"error": "Token not provided"}, status=401)