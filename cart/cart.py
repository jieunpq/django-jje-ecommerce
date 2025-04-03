from django.conf import settings

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