from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cart.cart import Cart
from store.models import Product
from django.shortcuts import render
from django.contrib import messages #dev_22

def add_cart(request):
    cart = Cart(request)

    if request.method == 'POST':
        try:
            product_id = request.POST.get("product_id")
            product_qty = request.POST.get("product_qty")
            
            print("product_id =", product_id)
            print("product_qty =", product_qty)

            product_id = int(product_id)
            product_qty = int(product_qty)

            product = get_object_or_404(Product, id=product_id)
            
            # 세션에 저장
            cart.add(product, product_qty)
            
            # 카트 전체 개수 가져오기
            cart_qty = cart.__len__()
            response = JsonResponse({"qty": cart_qty})
            
            # 세션 확인 테스트
            cart.decrypt_all_sessions()
            
            #dev_22
            messages.error(request, "장바구니에 해당 상품이 추가되었습니다.")
            return response
            # return JsonResponse({
            #     "message": "장바구니에 추가되었습니다.",
            #     "product_id": product_id,
            #     "qty": cart_qty   # 여기에 qty 포함해야 함!
            # })

        except Exception as e:
            import traceback
            print("에러 발생:", e)
            traceback.print_exc()  # 실제 Traceback을 출력해줌
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

def summary_cart(request):
    
    # 카트객체 받아오기
    cart = Cart(request)
    
    return render(request,"cart/summary.html",{"cart": cart, "totals": cart.get_product_total})

def delete_cart(request):
    
    # 카트객체 받아오기
    cart = Cart(request)
    
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        
        product = Product.objects.get(id=product_id)
        
        cart.remove(product)
    
        messages.success(request, "장바구니에 해당 상품이 삭제되었습니다.")
        return JsonResponse({"삭제 상품": product_id})

def update_cart(request):
    cart = Cart(request)
    
    if request.POST.get("action") == "update":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        
        product = Product.objects.get(id=product_id)
        
        # 카트 추가가 아닌 업데이트
        cart.add(product, product_qty, True)
        
        messages.success(request, "장바구니에 해당 상품이 변경되었습니다.")
        return JsonResponse({"상품 업데이트": product_id})