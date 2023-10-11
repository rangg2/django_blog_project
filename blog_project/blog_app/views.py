from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Board
from .serializers import BoardSerializer
from .forms import PostForm,CustomLoginForm
from time import sleep
from bs4 import BeautifulSoup
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.core.files.storage import default_storage


import openai

# # Create your views here.
# Board 데이터베이스 불러오기
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# def post_test(request):
#     return render(request, "post.html")


# # 게시판 페이지
# def board_page(request):
#     posts = Board.objects.all().order_by("-created_at")
#     category = "none"
#     return render(request, "board.html", {"posts": posts, "category": category})


# # 카테고리별 게시판 페이지
# def board_categorized(request, category):
#     categorized_posts = Board.objects.filter(category_name=category).order_by(
#         "-created_at"
#     )
#     context = {"posts": categorized_posts, "category": category}
#     return render(request, "board.html", context)


# def login_page(request):
#     return render(request, "login.html")


############################################################################## 09/12추가5
# 회원 가입
@csrf_exempt
def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == "POST":
        # password와 confirm에 입력된 값이 같다면
        if request.POST["password"] == request.POST["confirm"]:
            # user 객체를 새로 생성
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password"]
            )
            # 로그인 한다
            # auth.login(request, user)
            return redirect("/")
        else:
            return render(request, "failed.html")

    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    return render(request, "signup.html")


# 로그인

# def login(request):
#     # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
#     if request.method == "POST":
#         # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
#         username = request.POST["username"]
#         password = request.POST["password"]

#         # 해당 username과 password와 일치하는 user 객체를 가져온다.
#         user = auth.authenticate(request, username=username, password=password)

#         # 해당 user 객체가 존재한다면
#         if user is not None:
#             # 로그인 한다
#             auth.login(request, user)
#             return redirect("/")
#         # 존재하지 않는다면
#         else:
#             # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
#             return render(
#                 request, "failed_login.html")
#     # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
#     else:
#         return render(request, "login.html")
@csrf_exempt
def custom_login(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == "POST":

            # 입력정보가 유효한 경우 각 필드 정보 가져옴
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # 위 정보로 사용자 인증(authenticate사용하여 superuser로 로그인 가능)
                user = authenticate(request, username=username, password=password)

                # 로그인이 성공한 경우
                if user is not None:
                    login(request, user) # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect('/')  # 리다이렉션
        return render(request, 'login.html', {'form': form}) #폼을 템플릿으로 전달


# 로그 아웃
@csrf_exempt
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == "POST":
        auth.logout(request)
        return redirect("/")

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, "login.html")


############################################################################## 09/12추가5


# 게시글 조회 기능 구현
def post_page(request, post_id):
    post = Board.objects.get(id=post_id)
    next_post = (
        Board.objects.filter(created_at__gt=post.created_at)
        .order_by("created_at")
        .first()
    )
    prev_word = (
        Board.objects.filter(created_at__lt=post.created_at)
        .order_by("created_at")
        .last()
    )
    context = {"post": post, "next_post": next_post, "prev_word": prev_word}
    return render(request, "post.html", context)




def post_list(request, topic=None):
    
    # 특정 주제로 필터링
    if topic:
        posts = Board.objects.filter(topic=topic, publish='Y').order_by('-views')
    
    else:
        posts = Board.objects.filter(publish='Y').order_by('-views') 
    return render(request, 'board.html', {'posts': posts})

def post_detail(request, post_id):
    # 포스트 id로 게시물 가져옴
    post = get_object_or_404(Board, id=post_id)

    if request.method == 'POST': 

        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post.delete()
            return redirect('board')

    # 조회수 증가 및 db에 저장
    post.views += 1 
    post.save() 

    # 이전/다음 게시물 가져옴
    previous_post = Board.objects.filter(id__lt=post.id, publish='Y').order_by('-id').first()
    next_post = Board.objects.filter(id__gt=post.id, publish='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = Board.objects.filter(topic=post.topic, publish='Y').exclude(id=post.id).order_by('-created_at')[:2]
    # 게시물 내용에서 첫번째 이미지(썸네일) 태그 추출
    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'post.html', context)

class BlogPostList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    

# @csrf_exempt
@login_required
def create_or_update_post(request, post_id=None):
    # 글수정 페이지의 경우
    if post_id:
        post = get_object_or_404(Board, id=post_id)
    
    # 글쓰기 페이지의 경우, 임시저장한 글이 있는지 검색 
    else:
        post = Board.objects.filter(user_id=request.user.username, publish='N').order_by('-created_at').first()

    # 업로드/수정 버튼 눌렀을 떄
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) # 폼 초기화
        if form.is_valid():
            post = form.save(commit=False)

            # 게시물 삭제
            if 'delete-button' in request.POST:
                post.delete() 
                return redirect('board') 

            if not form.cleaned_data.get('topic'):
                post.topic = '전체'
            
            # 임시저장 여부 설정
            if 'temp-save-button' in request.POST:
                post.publish = 'N'
            else:
                post.publish = 'Y'

            # 글쓴이 설정
            post.user_id = request.user.username

            post.save()
            return redirect('post_detail', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
    
    # 수정할 게시물 정보를 가지고 있는 객체를 사용해 폼을 초기화함
    else:
        form = PostForm(instance=post)

    template = 'write.html'
    context = {'form': form, 'post': post, 'edit_mode': post_id is not None, 'MEDIA_URL': settings.MEDIA_URL,} #edit_mode: 글 수정 모드여부

    return render(request, template, context)

API_KEY = getattr(settings, 'OPENAI', 'OPENAI')

# Chat gpt API 사용
openai.api_key = API_KEY


# 글 자동완성 기능
def autocomplete(request):
    if request.method == "POST":

        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, 'write.html')

class image_upload(View):
    
    # 사용자가 이미지 업로드 하는경우 실행
    def post(self, request):
        
        # file필드 사용해 요청에서 업로드한 파일 가져옴
        file = request.FILES['file']
        
        # 저장 경로 생성
        filepath = 'uploads/' + file.name
        
        # 파일 저장
        filename = default_storage.save(filepath, file)
        
        # 파일 URL 생성
        file_url = settings.MEDIA_URL + filename
        
        # 이미지 업로드 완료시 JSON 응답으로 이미지 파일의 url 반환
        return JsonResponse({'location': file_url})