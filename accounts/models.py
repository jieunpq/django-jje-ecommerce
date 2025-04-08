from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# dev_9
# User 계정을 커스터마이징 시키는 방법은 4가지 정도 있음
# 1) proxy 활용
# 2) AbstractUser 상속하는 방법
# 3) AbstractBaseUser 상속하는 방법

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    class JobChoices(models.TextChoices):
        PROFESSOR = "P", "교수/강사"
        STUDENT = "S", "학생"
        RESEARCHER = "R", "연구원"
        ETC = "E", "기타"

    gender = models.CharField(
        verbose_name="성별",
        max_length=1,
        choices=GenderChoices.choices,
        blank=True,
        null=True
    )
    
    email = models.EmailField(
        verbose_name="이메일", 
        unique=True, 
        blank=False, 
        null=False
    )


    job = models.CharField(
        verbose_name="직업",
        max_length=1,
        choices=JobChoices.choices,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # dev_23
    old_cart = models.CharField(max_length=200, blank=True, null=True)

