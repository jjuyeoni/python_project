from django.urls import path
from . import views, search
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"), # 회원 상태별 화면 분기 
    path("logout/", LogoutView.as_view(next_page="/auth/login")), # 로그아웃
    path("waitingList/", views.waitingList, name="waitingList"), # 가입 대기 리스트
    path("userList/", views.user_list, name="userList"), # 회원 리스트
    path("update_user_info/<int:user_id>/", views.update_user_info, name="update_user_info"), # 회원 정보 수정
    path('update_user_status/', views.update_user_status, name='update_user_status'), # 가입 대기 → 승인/거절 처리
    path('quit_user/', views.quit_user, name='quit_user'), # 회원 탈퇴
    path('normalUserSearch/', search.search_normal_user, name='search_normal_user'), # 회원 검색
    path('waitingUserSearch/', search.search_waiting_user, name='search_waiting_user'), # 가입대기 검색
    path('history/',views.userInfoHistory, name="userIfoHistory"),
]