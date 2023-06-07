from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from users.models import CustomUser
from django.http import JsonResponse

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.phone_number = form.cleaned_data['phone_number']
            user.username = form.cleaned_data['username']
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            login(request, user)
            return redirect("index") 
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# 로그인
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            msg = "올바른 ID와 패스워드를 입력하세요."
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(raw_password):
                    if user.is_active:
                        login(request, user)
                        return redirect("index")
                    else:
                        msg = "탈퇴한 회원입니다."
            except CustomUser.DoesNotExist:
                msg = "존재하지 않는 ID 또는 비밀번호 입니다."
        else:
            if user.check_password(raw_password):
                msg = None
                login(request, user)
                return redirect("index")
    else:
        msg = None
        form = LoginForm()
    return render(request, "users/login.html", {"form": form, "msg": msg})


# 이메일 중복 확인
def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        exists = CustomUser.objects.filter(email=email).exists()
        
        return JsonResponse({'exists': exists})
    
