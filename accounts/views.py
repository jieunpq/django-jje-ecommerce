from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegisterUserForm

# Create your views here.

def logout_user(request):
    logout(request)
    return redirect("/")

def login_user(request):
    
    if request.method == "POST":
        # username = request.POST.get("username","") # 이게 더 안전
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request, '로그인이 되었습니다.')
            return redirect("/")
        else:
            messages.success(request, '로그인이 실패하였습니다. 다시 한번 더 시도해주시기 바랍니다.')
            return redirect("accounts:login_user")
        
        
    else:
        return render(request, 'accounts/login.html')
    
# dev_10
def register_user(request):
    
    form = RegisterUserForm()
    
    if request.method == "POST":
        
        if request.POST["password1"] == request.POST["password2"]:
            form = RegisterUserForm(request.POST) # 모델에 값을 넣음
            
            if form.is_valid():
                form.save() # 회원 DB 저장
                
                # 회원가입 하자 마자, 로그인 시켜줌
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                
                user = authenticate(username=username,password=raw_password)
                login(request,user)
                return redirect("/")
        
    else:
        form = RegisterUserForm()
    

    return render(request, 'accounts/register.html', {"form": form})