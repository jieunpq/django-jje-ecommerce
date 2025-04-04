from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


# dev_15
class Cart(): # 카트 클래스 생성
    
    def __init__(self,request): # 객체 생성시 request 객체
        
        self.session = request.session # session 객체를 cart
        
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # session에 cart 객체가 없으면 session 객체에 cart를 만듦
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart
    
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
    
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        
        # self.cart = {
        #     "1":{"quantity":7, "price":"3000.00"}, 
        #     "2":{"quantity":1, "price":"5000.00"}, 
        # }

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }

        if is_update:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True # 해당 세션을 DB에 저장
        
    def decrypt_all_sessions(self):
        """현재 DB에 저장된 모든 세션을 복호화하여 출력"""
        sessions = Session.objects.all()  # DB에서 모든 세션 조회

        if not sessions.exists():
            print("❌ 현재 저장된 세션이 없습니다.")
            return

        print(f"🔹 총 {sessions.count()}개의 세션을 찾았습니다.")

        for session in sessions:
            try:
                session_data = SessionStore(
                    session_key=session.session_key
                ).load()  # 세션 복호화
                print(f"✅ 세션 키: {session.session_key}\n   데이터: {session_data}\n")

            except Exception as e:
                print(f"❌ 복호화 실패 - 세션 키: {session.session_key}, 오류: {e}")