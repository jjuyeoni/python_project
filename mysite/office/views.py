from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import CustomUser
from office.models import UserInfoHistory
from datetime import datetime


# 회원 상태별 화면 분기
@login_required(login_url='login')
def index(request):
    # 가입 대기 유저
    if request.user.status == 'W':  
        context = {
            'mainMsg': '[[가입 대기]]',
            'subMsg': '관리자의 승인이 필요합니다.',
        }
        return render(request, 'office/waiting.html', context)
    
    # 가입 거부 유저
    if request.user.status == 'R':
        context = {
            'mainMsg': '[[가입 거절]]',
            'subMsg': '관리자에게 문의 부탁드립니다.',
        }
        return render(request, 'office/waiting.html', context)
    
    # 일반 회원 유저
    if request.user.is_staff == False:
        return redirect('userList')
    
    return redirect('waitingList')


# 가입대기/ 회원 목록 
@login_required(login_url='login')
def waitingList(request):
    if request.user.status != 'A': 
        return redirect('index')
    
    waiting_users = CustomUser.objects.filter(status__in=['W', 'R']).order_by('-date_joined')

    paginator = Paginator(waiting_users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'signedUser': request.user,
        'waiting_users': page_obj,
        'previous_page_number': page_obj.previous_page_number if page_obj.has_previous() else None,
        'number': page_obj.number,
        'next_page_number': page_obj.next_page_number if page_obj.has_next() else None,
    }
    return render(request, 'office/index.html', context)


# 유저 목록
@login_required(login_url='login')
def user_list(request):
    if request.user.status != 'A': 
        return redirect('index')
    
    # Logged in user = nomal
    if not request.user.is_staff and not request.user.is_superuser:
        users = CustomUser.objects.filter(status='A', is_superuser=False, is_staff=False, is_active=True).order_by('-date_joined')
    
    # Logged in user = staff
    elif request.user.is_staff and not request.user.is_superuser:
        users = CustomUser.objects.filter(status='A', is_superuser=False, is_active=True).order_by('-date_joined')
    
    # Logged in user = master
    else: 
        users = CustomUser.objects.filter(status='A').order_by('-date_joined')

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'signedUser': request.user,
        'users': page_obj,
        'previous_page_number': page_obj.previous_page_number if page_obj.has_previous() else None,
        'number': page_obj.number,
        'next_page_number': page_obj.next_page_number if page_obj.has_next() else None,
    }
    return render(request, 'office/userList.html', context)

def makeNotiMsg(user, username, phone_number, role):
    msg = ""
    if user.username != username:
        msg += "이름이 "
    if user.phone_number != phone_number:
        msg += "전화번호가 "
    if not user.is_staff and role == 'staff':
        msg += "등급이 스태프로 "
    elif user.is_staff and role == 'normal':
        msg += "등급이 일반으로 "
    
    if msg != "":
        msg = user.email+"님의 " + msg + " 변경되었습니다."
        noti = UserInfoHistory(
            user = user,
            alarmMsg = msg,
            timestamp = datetime.now()
        )

        noti.save()

# 회원 정보 update
@login_required(login_url='login')
def update_user_info(request, user_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        user = CustomUser.objects.get(id=user_id)

        # 변경사항에 대한 noti 생성
        makeNotiMsg(user, username, phone_number, role)

        user.username = username
        user.phone_number = phone_number
        if role == 'master':
            user.is_superuser = True
            user.is_staff = True
        elif role == 'staff':
            user.is_superuser = False
            user.is_staff = True
        elif role == 'normal':
            user.is_superuser = False
            user.is_staff = False

        user.save()
        
        return redirect('userList')
    
    return render(request, 'office/update_user_info.html')

# 대기상태의 회원 -> 승인/거절 처리
@login_required(login_url='login')
def update_user_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason')
        
        user = CustomUser.objects.get(id=user_id)
        
        if status == 'A':
            user.status = 'A'
        elif status == 'R':
            user.status = 'R'
            user.rejection_reason = rejection_reason
            user.rejection_date = datetime.now()
        
        user.save()
        
    return redirect('index')

# 회원 탈퇴
@login_required(login_url='login')
def quit_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        quit_reason = request.POST.get('quit_reason')
        
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.quit_reason = quit_reason
        user.quit_date = datetime.now()
        user.save()
        
    return redirect('userList')


# 회원 정보 변경 히스토리
def userInfoHistory(request):
    if not request.user.is_superuser:
        user_history = UserInfoHistory.objects.exclude(user__is_superuser=True)
    else :
        user_history = UserInfoHistory.objects.all()

    return render(request, 'office/history.html', {'user_history': user_history})


