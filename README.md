### 환경설정
BE : django, sqlite3
FE : javascript, jQuery, html/css

### DB 스키마
![image](https://github.com/jjuyeoni/python_project/assets/18046663/5a6814e8-bee2-43cb-9266-b1787e51c47a)

### 로컬 실행 가이드
  - requirements.txt 에 설정된 파일 다운 후 실행이 필요합니다. <br>
    pip3 install -r requirements.txt

  - 백오피스 project 이름은 'mysite' 입니다. <br>
    cd mysite 하고, python manage.py runserver 해주세요.

  - 계정정보 (비밀번호 : 1234)
    - 마스터 : admin@example.com 
    - 관리자 : manager1@example.com
    - 일반 :
      1. 승인 : normal1@example.com
      2. 대기 : wait1@example.com
      3. 거절 : refuse1@example.com
      4. 탈퇴 : delete1@example.com

### 기능 
  - 첫 화면은 로그인으로 세팅, 로그인 or 회원 가입 시 바로 백오피스 화면으로 진입.
    ( 이때 탈퇴 계정은 로그인 단계에서 Block )

  - 로그인 > 각 계정 등급에 따라 노출되는 화면 스펙
    - 마스터 : 가입대기, 회원 리스트, 모든 등급 유저 확인 가능
    - 관리자 : 가입대기, 회원 리스트, 관리자 등급 이하 유저 확인 가능(탈퇴 회원 조회 불가)
    - 일반(승인) : 회원 리스트, 회원 등급 유저 확인 가능(탈퇴 회원 조회 불가)
    - 일반(대기/거절) : 리스트 조회 불가, 가입대기/거절 안내 페이지로 이동

  - 회원 검색 기능
  - 회원 정보 변경 히스토리 리스트업

### 프로젝트 설계 구조

```
└─mysite
    ├─mysite
    │  └─__pycache__
    ├─office // 백오피스 관련 기능
    │  ├─ views.py // 가입 대기& 회원 리스트업, 회원정보 업데이트 등 회원과 관련된 기능 메소드
    │  ├─ search.py // 회원 검색 메소드
    │  ├─migrations
    │  │  └─__pycache__
    │  ├─templates
    │  │  └─office
    │  └─__pycache__
    ├─static
    │  └─css
    ├─users // 회원 관련 기능
    │  ├─ views.py // 로그인, 로그아웃, 회원가입 관련 메소드
    │  ├─migrations
    │  │  └─__pycache__
    │  ├─templates
    │  │  └─users
    │  └─__pycache__
    └─__pycache__
```
