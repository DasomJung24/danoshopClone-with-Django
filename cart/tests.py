import json
import jwt 
import datetime

from django.test    import TestCase, Client
from my_settings    import SECRET, ALGORITHM
from user.utils     import login_decorator
from user.models    import User
from product.models import Product, Image, Category, ProductCategory
from .models        import Cart



class CartTest(TestCase):
    maxDiff = None
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
        User.objects.create(
            id       = 2,
            name     = 'test1',
            email    = 'test1@nate.com',
            password = 'test1',
            birth    = None,
            job      = None,
            gender   = None
        )
        Product.objects.create(
            id            = 1,
            name          = 'test1',
            price         = 10000,
            discount_rate = 10,
            product_type  = None,
            detail        = 'test1',
            sub_detail    = 'test1',
            sub_name      = 'test1',
        )
        Product.objects.create(
            id            = 2,
            name          = 'test2',
            price         = 100,
            discount_rate = 0,
            product_type  = None,
            detail        = 'test',
            sub_detail    = 'test',
            sub_name      = 'test'
        )
        Product.objects.create(
            id            = 3,
            name          = 'test2',
            price         = 100,
            discount_rate = 0,
            product_type  = None,
            detail        = 'test',
            sub_detail    = 'test',
            sub_name      = 'test'
        )
        Category.objects.create(
            id   = 1,
            name = 'test1'
        )
        ProductCategory.objects.create(
            product_id  = 1,
            category_id = 1
        )
        Image.objects.create(
            id         = 1,
            image      = 'test.test',
            product_id = 1
        )
        Image.objects.create(
            id         = 2,
            image      = 'testes.es',
            product_id = 1
        )
        Image.objects.create(
            id         = 3,
            image      = 'test.test',
            product_id = 2
        )
        Image.objects.create(
            id         = 4,
            image      = 'test.test',
            product_id = 3
        )
        Cart.objects.create(
            id         = 1,
            user_id    = 1,
            product_id = 2,
            count      = 1
        )
        Cart.objects.create(
            id         = 2,
            user_id    = 1,
            product_id = 1,
            count      = 2
        )
        expire     = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        self.token = jwt.encode({'user_id':1, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        ProductCategory.objects.all().delete()
        Image.objects.all().delete()
        User.objects.all().delete()
        Cart.objects.all().delete()

    def test_post_create_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'product_id' : 3,
            'count'      : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_create_cart_product_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'product_id' : 9,
            'count'      : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_creat_cart_already_exist(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'product_id' : 1,
            'count'      : 1
        }
        response = client.post('/cart', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'ALREADY EXIST'})
        self.assertEqual(response.status_code, 400)

    def test_get_cart_list_success(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        response = client.get('/cart', **headers)
        self.assertEqual(response.json(), 
            {
                'cart_list':[
                    {
                        'id'         : 1,
                        'product_id' : 2,
                        'name'       : 'test2',
                        'image'      : 'test.test',
                        'price'      : 100,
                        'count'      : 1
                    },
                    {
                        'id'         : 2,
                        'product_id' : 1,
                        'name'       : 'test1',
                        'image'      : 'test.test',
                        'price'      : 9000,
                        'count'      : 2
                    }        
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'button':'+'
        }
        response = client.patch('/cart/2', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_patch_cart_but_count_is_one(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'button' : '-'
        }
        response = client.patch('/cart/1', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_patch_cart_wrong_data(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'button' : '*'
        }
        response = client.patch('/cart/1', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_patch_cart_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        cart = {
            'button' : '+'
        }
        response = client.patch('/cart/5', json.dumps(cart), **headers, content_type='application/json')
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

    def test_delete_cart_success(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        response = client.delete('/cart/2', **headers)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_delete_cart_not_exist(self):
        client = Client()

        headers = {'HTTP_Authorization': self.token}

        response = client.delete('/cart/7', **headers)
        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)