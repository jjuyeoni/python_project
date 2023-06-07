from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

# User 생성
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, status='W', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, status='A', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

# AbstractUser 를 이용하여 User 형태 custom 하는 함수
class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('W', '대기'),
        ('A', '승인'),
        ('R', '거절'),
    )
    username = models.CharField(max_length=50, unique=False) 
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    phone_number = models.CharField(max_length=11)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='W')
    rejection_reason = models.TextField(blank=True)
    rejection_date = models.DateTimeField(blank=True, null=True)
    quit_reason = models.TextField(blank=True)
    quit_date = models.DateTimeField(blank=True, null=True)

    # 사용자 이름 = username 필드 사용, 이외 사용하지 않는 필드 삭제
    first_name = None
    last_name = None

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    
