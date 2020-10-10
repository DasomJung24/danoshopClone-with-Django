from django.views   import View
from django.http    import JsonResponse
from .models        import Review, ReviewImage
from user.utils     import login_decorator
from product.models import Product
from user.models    import User
import json

class ReviewView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        product_id = request.GET.get('product_number', None)
        if product_id == None:
            return JsonResponse({'message':'NOT FOUND'}, status=404)

        review = Review.objects.create(
            user_id    = request.user.id,
            title      = data['title'],
            content    = data['content'],
            score      = data['score'],
            product_id = product_id
        )
        
        for image_url in data['image']:
            ReviewImage.objects.create(image = image_url, review_id = review.id)

        return JsonResponse({'message':'SUCCESS'}, status=200)

    def get(self, request):
        product_id = request.GET.get('product_number', None)
        limit      = request.GET.get('limit', None)
        offset     = request.GET.get('offset', None)

        if product_id == None or limit == None or offset == None:
            return JsonResponse({'message':'INVALID REQUEST'}, status=400)
        
        reviews = Review.objects.filter(product_id=product_id).order_by('-id')[int(offset):int(limit)+int(offset)]
        results = [{
            'id'   : data.id,
            'title': data.title,
            'user' : data.user.name.replace(data.user.name[1], '*'),
            'score': data.score
        } for data in reviews]

        return JsonResponse({'review_list':results}, status=200)

    @login_decorator
    def patch(self, request, review_id):  
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'message':'NOT FOUND'}, status=404)
        data = json.loads(request.body)

        review = Review.objects.get(id=review_id)
        review.title = data['title']
        review.content = data['content']
        review.score = data['score']
        review.save()

        ReviewImage.objects.filter(review_id=review_id).delete()
        for image_url in data['image']:
            ReviewImage.objects.create(image = image_url, review_id = review_id)

        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def delete(self, request, review_id):
        
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'message':'NOT FOUND'}, status=404)
        Review.objects.get(review_id).delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)

class ReviewDetailView(View):
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)

            results = [{
                'id'       : review_id,
                'title'    : review.title,
                'score'    : review.score,
                'user_name': review.user.name.replace(review.user.name[1], '*'),
                'image'    : [data.image for data in ReviewImage.objects.filter(review_id=review_id)],
                'content'  : review.content
            }]

            return JsonResponse({'review':results}, status=200)
        
        except Review.DoesNotExist:
            return JsonResponse({'message':'NOT FOUND'}, status=404)