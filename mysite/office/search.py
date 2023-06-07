from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import CustomUser

# 일반 회원 검색용 필터
def filtered_nomal_users(query, user):
    if not user.is_staff and not user.is_superuser:
        return CustomUser.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query),
            status='A', is_superuser=False, is_staff=False, is_active=True
        ).order_by('-date_joined')
    
    elif user.is_staff and not user.is_superuser:
        return CustomUser.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query),
            status='A', is_superuser=False, is_active=True
        ).order_by('-date_joined')

    else:
        return CustomUser.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query),
            status='A'
        ).order_by('-date_joined')
    

# 일반 회원 검색 ↑
def search_normal_user(request):
    query = request.GET.get('query','')
    users = filtered_nomal_users(query, request.user)

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


# 대기, 거절 상태 회원 검색용 필터
def filtered_users(query, status):
    return CustomUser.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query),
        Q(status=status)
    ).order_by('-date_joined')


# 대기, 거절 상태 회원 검색 ↑
def search_waiting_user(request):
    query = request.GET.get('query','')
    statusSearch = request.GET.get('statusSearch')

    if statusSearch == 'W':
        users = filtered_users(query, 'W')
    elif statusSearch == 'R':
        users = filtered_users(query, 'R')
    else:
        users = filtered_users(query, 'W') | filtered_users(query, 'R')
    
    paginator = Paginator(users, 10)
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