from django.views   import View
from django.http    import JsonResponse
from user.utils     import login_decorator
from .models        import Cart
from product.models import Product, Image
from user.models    import User
import json

class CartView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        if not Product.objects.filter(id=data['product_id']).exists():
            return JsonResponse({'message':'INVALID REQUEST'}, status=400)

        if Cart.objects.filter(product_id=data['product_id'], user=request.user).exists():
            return JsonResponse({'message':'INVALID REQUEST'}, status=400)
        
        Cart.objects.create(
            user = request.user,
            product_id = data['product_id'],
            count = data['count']
        )

        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def get(self, request):
        carts = Cart.objects.filter(user=request.user).select_related('product')
        
        results = [{
            'id':cart.id,
            'product_id':cart.product.id,
            'name':cart.product.name,
            'image':Image.objects.filter(product_id=cart.product).first().image,
            'price':int(cart.product.price if cart.product.discount_rate==0 \
                        else cart.product.price // 100 * (100-cart.product.discount_rate)),
            'count':cart.count
        } for cart in carts]

        return JsonResponse({'cart_list':results}, status=200)

    @login_decorator
    def patch(self, request, cart_id):
        try:
            data = json.loads(request.body)
            cart = Cart.objects.get(id=cart_id)
            if data['click'] == '+':
                cart.count += 1
                cart.save()
            elif data['click'] == '-':
                cart.count -= 1
                cart.save()
            else:
                return JsonResponse({'message':'INVALID REQUEST'}, status=400)

            return JsonResponse({'message':'SUCCESS'}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message':'NOT FOUND'}, status=404)

    @login_decorator
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'message':'NOT FOUND'}, status=404)