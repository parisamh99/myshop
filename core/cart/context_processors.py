from .cart import CartSession
def cart_context(request):
    cart = CartSession(request.session)
    return {"cart": cart}

