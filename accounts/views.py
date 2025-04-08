from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .forms import RegisterUserForm  # 상대 경로 방식
from accounts.forms import RegisterUserForm  # 절대 경로 방식
from cart.cart import Cart
from django.contrib.auth import get_user_model
import json
from store.models import Product  # Product 모델 import 필요


# Create your views here.

def logout_user(request):
    logout(request)
    return redirect("/")


def login_user(request):
    
    if request.method == "POST":
        # username = request.POST.get("username","") # 이게 더 안전
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # session key 생성 및 세션키 DB 저장
            messages.success(request, '로그인이 되었습니다.')
            messages.success = ("")  # 이 부분은 의미가 없으므로 필요하면 수정 필요
            
            # dev_23
            User = get_user_model()
            current_user = User.objects.get(id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)

                # add
                cart = Cart(request)

                # {"1": {"quantity": 5, "price": "10000"}}
                # loop
                for product_id, data in converted_cart.items():
                    quantity = data["quantity"]
                    print("상품 ID:", product_id)  # 1
                    print("수량:", quantity)  # 5
                    product = Product.objects.get(id=product_id)
                    cart.add(product, quantity)

            return redirect("/")
        else:
            messages.success(request, '로그인이 실패하였습니다. 다시 한번 더 시도해주시기 바랍니다.')
            return redirect("accounts:login_user")
        
    else:
        return render(request, 'accounts/login.html')


def register_user(request):

    form = RegisterUserForm()
    
    if request.method == "POST":
        
        if request.POST["password1"] == request.POST["password2"]:
            form = RegisterUserForm(request.POST)  # 모델에 값을 넣음
            
            if form.is_valid():
                form.save()  # 회원 DB 저장
                
                # 회원가입 하자 마자, 로그인 시켜줌
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("/")
        
    else:
        form = RegisterUserForm()

    return render(request, 'accounts/register.html', {"form": form})