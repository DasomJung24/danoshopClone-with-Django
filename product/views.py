from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from .models                import Product, ProductCategory, Category, ProductType, Image
from django.core.exceptions import ObjectDoesNotExist

class ProductListView(View):
    def get(self, request):
        category_number = request.GET.get('category', None)
        type_number     = request.GET.get('type', None)
        keywords        = request.GET.get('keywords', None)

        if category_number != None or type_number != None:
            if not Product.objects.filter(Q(category=category_number)|Q(product_type_id=type_number)).exists():
                return JsonResponse({'message':'NOT FOUND'}, status=404)
            products = Product.objects.filter(Q(category=category_number)|Q(product_type_id=type_number))
        
        elif keywords != None:
            products = Product.objects.filter(name__icontains=keywords)
        
        else:
            products = Product.objects.all()

        results = [{
            'image'         : [image.image for image in Image.objects.filter(product_id=data.id)],
            'name'          : data.name,
            'price'         : int(data.price),
            'discount_rate' : int(data.discount_rate),
            'discount_price': int(data.price) // 100 * (100 - int(data.discount_rate)) if int(data.discount_rate) != 0 else 0,
            'product_id'    : data.id,
            'new'           : True if Product.objects.filter(category=1).filter(id=data.id).exists() else False,
            'free_shipment' : True if Product.objects.filter(category=5).filter(id=data.id).exists() else False,
            'sale'          : True if Product.objects.filter(category=4).filter(id=data.id).exists() else False
        } for data in products]

        return JsonResponse({'product_list':results}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            results = {
                'image'         : [image.image for image in Image.objects.filter(product_id=product.id)],
                'name'          : product.name,
                'price'         : int(product.price),
                'discount_rate' : int(product.discount_rate),
                'discount_price': int(product.price) // 100 * (100 - int(product.discount_rate)) if int(product.discount_rate) != 0 else 0,
                'product_id'    : product.id,
                'sub_name'      : product.sub_name,
                'detail'        : product.detail,
                'sub_detail'    : product.sub_detail,
                'free_shipment' : True if Product.objects.filter(category=5).filter(id=product.id).exists() else False,
                'sale'          : True if Product.objects.filter(category=4).filter(id=product.id).exists() else False
            }

            return JsonResponse({'product_data':[results]}, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message':'NOT EXIST'}, status=404)