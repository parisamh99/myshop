from shop.models import ProductModel,StatusProductType


class CartSession:
    def __init__(self,session):
        
        self.session = session
        self.cart = self.session.setdefault("cart", {"items": [],
                                                     "quntity":0})
      
        # print(self.session.get("cart"))
        # self.add_product(10)
        # print(self.session.get("cart"))

    def add_product(self,product_id):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] +=1
                break
        else:
            new_item = {
                "product_id":product_id,
                "quantity":1
            }
            self.cart["items"].append(new_item)
        self.save()



    def update_product(self,product_id,quantity):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()


    def remove_product(self,product_id):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                self.cart["items"].remove(item)
                break
        self.save()

    
    def clear(self):
        self.cart = self.session["cart"] ={
            "items":[],
        }
       
        self.save()


    def get_cart_dict(self):
        return self.cart
    

    def save(self):
       self.session.modified = True    

    def get_total_quantity(self):
        total_quantity = 0 
        for item in self.cart["items"]:
            total_quantity += item["quantity"]
        return total_quantity  


    # def len_total(self):
    #     total = len(self.cart["items"])
    #     return total

    
    def get_cart_items(self):
        cart_items = self.cart["items"]
        for item in cart_items:
            product_obj = ProductModel.objects.get(id= item["product_id"], status=StatusProductType.publish.value)
            item["product_obj"] = product_obj
            item["total_price"] = int(item["quantity"]) * product_obj.get_price()
        return cart_items   

    def get_total_price(self):
     total = 0
     for item in self.get_cart_items():
        total += item["total_price"]
     return total
