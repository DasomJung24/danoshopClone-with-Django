import json
import jwt
import datetime

from django.test    import TestCase, Client
from my_settings    import SECRET, ALGORITHM
from user.models    import User
from product.models import Product, ProductCategory, Category
from user.utils     import login_decorator
from .models        import Review, ReviewImage


class ReviewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = 'test1',
            email    = 'test1@nate.com',
            password = 'test1',
            birth    = None,
            job      = None,
            gender   = None
        )
        Product.objects.create(
            id            = 1,
            price         = 10000,
            discount_rate = 10,
            product_type  = None,
            detail        = 'test1',
            sub_detail    = 'test1',
            sub_name      = 'test1',
        )
        Category.objects.create(
            id   = 1,
            name = 'test1'
        )
        ProductCategory.objects.create(
            product_id  = 1,
            category_id = 1
        )
        Review.objects.create(
            id         = 1,
            user_id    = 1,
            title      = 'test1',
            content    = 'test1',
            score      = 3,
            product_id = 1
        )
        ReviewImage.objects.create(
            id        = 1,
            image     = 'test.test',
            review_id = 1
        )
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':1, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')
    
    def tearDown(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()
        User.objects.all().delete()

    def test_review_post_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        review = {
            'title'   : 'test2',
            'content' : 'test2',
            'score'   : 3,
            'image'   : 'test2.test2'
        }
        response = client.post('/review?product_number=1', json.dumps(review), **headers, content_type='application/json')
        self.assertEqual(response.json(),{'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_review_post_product_id_not_exist(self):
        client = Client()
        
        headers = {'HTTP_Authorization':self.token}

        review = {
            'title'   : 'test2',
            'content' : 'test2',
            'score'   : 3,
            'image'   : 'test2.test2'
        }
        response = client.post('/review?product_number=5', json.dumps(review), **headers, content_type='application/json')
        self.assertEqual(response.json(),{'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

    def test_review_post_product_id_none(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        review = {
            'title'   : 'test2',
            'content' : 'test2',
            'score'   : 3,
            'image'   : 'test2.test2'
        }
        response = client.post('/review', json.dumps(review), **headers, content_type='application/json')
        self.assertEqual(response.json(),{'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)
    
    
    def test_get_review_list_success(self):
        client = Client()

        response = client.get('/review?product_number=1&limit=2&offset=0')
        self.assertEqual(response.json(),
            {
                'review_list' : [{
                    'id'    : 1,
                    'title' : 'test1',
                    'user'  : 't*st1',
                    'score' : 3
                }]
            })
        self.assertEqual(response.status_code, 200)

    def test_get_review_list_not_product_id_offset_limit(self):
        client = Client()

        response = client.get('/review?product_number=1&limit=3')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_patch_review_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        review={
            'title'   : 'testest',
            'content' : 'testest',
            'score'   : 2,
            'image'   : 'tes.tes'
        }
        response = client.patch('/review/1', json.dumps(review), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_patch_review_id_is_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        review={
            'title'   : 'testest',
            'content' : 'testest',
            'score'   : 2,
            'image'   : 'tes.tes'
        }
        response = client.patch('/review/5', json.dumps(review), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

    def test_review_delete_success(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        response = client.delete('/review/1', **headers)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_delete_review_id_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization':self.token}

        response = client.delete('/reivew/6', **headers)
        self.assertEqual(response.status_code, 404)

class ReviewDetailTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = 'test1',
            email    = 'test1@nate.com',
            password = 'test1',
            birth    = None,
            job      = None,
            gender   = None
        )
        Product.objects.create(
            id            = 1,
            price         = 10000,
            discount_rate = 10,
            product_type  = None,
            detail        = 'test1',
            sub_detail    = 'test1',
            sub_name      = 'test1',
        )
        Category.objects.create(
            id   = 1,
            name = 'test1'
        )
        ProductCategory.objects.create(
            product_id  = 1,
            category_id = 1
        )
        Review.objects.create(
            id         = 1,
            user_id    = 1,
            title      = 'test1',
            content    = 'test1',
            score      = 3,
            product_id = 1
        )
        ReviewImage.objects.create(
            id        = 1,
            image     = 'test.test',
            review_id = 1
        )
      
    def tearDown(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        ReviewImage.objects.all().delete()
        User.objects.all().delete()

    def test_get_review_detail_success(self):
        client = Client()

        response = client.get('/review/detail/1')
        self.assertEqual(response.json(), 
            {
                'review':[{
                    'id'        : 1,
                    'title'     : 'test1',
                    'score'     : 3,
                    'user_name' :'t*st1',
                    'image'     : ['test.test'],
                    'content'   : 'test1'
                }]
            })
        self.assertEqual(response.status_code, 200)

    def test_get_review_id_not_exist(self):
        client = Client()

        response = client.get('/review/detail/8')
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

    