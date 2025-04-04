from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cart.cart import Cart
from store.models import Product

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
            cart.decrypt_all_sessions()

            return JsonResponse({
                "message": "장바구니에 추가되었습니다.",
                "product_id": product_id,
                "qty": cart_qty   # 여기에 qty 포함해야 함!
            })

        except Exception as e:
            import traceback
            print("에러 발생:", e)
            traceback.print_exc()  # 실제 Traceback을 출력해줌
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)
