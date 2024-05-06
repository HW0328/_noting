from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Post, Comment
from django.contrib import auth
from bs4 import BeautifulSoup
import httpx, json, re

def clean_html_text(html_text):
    # HTML 태그 제거
    cleaned_text = re.sub(r'<[^>]+>', '', html_text)
    # 여러 개의 공백을 단일 공백으로 변경
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # 앞뒤 공백 제거
    cleaned_text = cleaned_text.strip()
    return cleaned_text

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

    # print(response_data)
    return JsonResponse(response_data, safe=False)

@csrf_exempt
def uploadPost(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        writer = data.get('writer')
        title = data.get('title')
        content = data.get('content')
        post = Post(writer = writer, title=title, content=content)
        post.save()
        return JsonResponse({"msg" : "Hello"})


def donong_lunch(req):
    with httpx.Client(verify=False) as client:
        response = client.get('https://donong-m.goegn.kr/donong-m/main.do')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        lunch = soup.select_one('#container > div.MC_wrap3 > div > div.con_wrap > div.MC_box7.widgEdit > div > div.inner > ul > li:nth-child(1) > dl > dd')
        # print(f"LUNCH : {lunch}")
        # print(lunch)
        print(lunch)
        lunch = str(lunch)
        lunch = clean_html_text(lunch)
    return JsonResponse({"lunch" : lunch})

def getComments(req, post_id):
    print(post_id)
    comments = Comment.objects.filter(postId=post_id).values()
    print(comments)
    cmt = []
    for i in comments:
        if i['isDelete'] == 0:
            cmt.append({
                'writer' : i['writer'],
                'content' : i['content'],
            })

    return JsonResponse({'cmt' : cmt})


@csrf_exempt
def uploadComment(req):
    if req.method=='POST':
        data = json.loads(req.body)
        writer = data.get('writer')
        content = data.get('content')
        postId = data.get('postId')
        print(writer, content, postId)
        comment = Comment(writer=writer, content=content, postId=postId)
        comment.save()

    return JsonResponse({'msg' : 'Hello, World!'})

@csrf_exempt
def log_in(req):
    if req.method=='POST':
        data = json.loads(req.body)
        id = data.get('id')
        pw = data.get('pw')
        
        user = authenticate(req, username=id, password=pw)

        print(id, pw, user)
        if user != None:
            login(req, user)

            return JsonResponse({
                'msg' : f'<Logined massage> Hello, {id}!', 
                'isLogined' : 1
                })
        
        else:
            return JsonResponse({
                'msg' : 'FUCK YOU',
                'isLogined' : 0
                })

@csrf_exempt
def sign_up(req):
    if req.method == 'POST':
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        data = json.loads(req.body)
        id = data.get('id')
        pw = data.get('pw')
        if not re.fullmatch(regex, pw):
            return JsonResponse({'err' : 'Invalid password'})   
        else:    
            user = User.objects.create_user(
                username=id,
                password=pw
            )
            auth.login(req, user)

            return JsonResponse({'suc' : 'success', 'err' : 'None'})