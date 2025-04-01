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
        MALE = "M","남성"
        FEMALE = "F", "여성"
        
        
    gender = models.CharField(
        verbose_name="성별",max_length=1,choices=GenderChoices.choices
    )
    
    JOBS = (
        ("P", "교수/강사(Professor/Lecturer)"),
        ("S", "학생(Student)"),
        ("R", "연구원(Researcher)"),
        ("E", "기타(Etc.)"),
    )
    
    gender = models.CharField(verbose_name="직업",max_length=1,choices=JOBS)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)