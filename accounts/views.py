from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .forms import RegisterUserForm  # 상대 경로 방식
from accounts.forms import RegisterUserForm  # 절대 경로 방식
from cart.cart import Cart
from django.contrib.auth import get_user_model
import json
from store.models import Product  # Product 모델 import 필요
from accounts.models import User


# Create your views here.


def logout_user(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        cart_data = json.dumps(cart.cart)  # 세션 장바구니를 문자열로 저장
        User.objects.filter(id=request.user.id).update(old_cart=cart_data)

    logout(request)
    return redirect("/")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '로그인이 되었습니다.')

            # 장바구니 복원
            User = get_user_model()
            current_user = User.objects.get(id=request.user.id)
            saved_cart = current_user.old_cart
            cart = Cart(request)

            if saved_cart:
                converted_cart = json.loads(saved_cart)

                for product_id, data in converted_cart.items():
                    quantity = data["quantity"]
                    product = Product.objects.get(id=product_id)
                    cart.add(product, quantity)

            # 장바구니를 DB에 다시 저장 (세션으로 복원된 내용을 기반으로)
            cart.cart_to_db()

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