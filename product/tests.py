from django.test import TestCase, Client
from .models     import Product, ProductCategory, Category, ProductType, Image

class ProductListTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'test_category1'
        )
        Category.objects.create(
            id   = 2,
            name = 'test_category2'
        )
        ProductType.objects.create(
            id   = 1,
            name = 'test_type1'
        )
        ProductType.objects.create(
            id   = 2,
            name = 'test_type2'
        )
        Product.objects.create(
            id   = 1,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 1,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Product.objects.create(
            id   = 2,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 1,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Product.objects.create(
            id   = 3,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 2,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Image.objects.create(
            image = 'test1.test1',
            product_id = 1
        )
        Image.objects.create(
            image = 'test2.test1',
            product_id = 1
        )
        ProductCategory.objects.create(category_id=1, product_id=1)
        ProductCategory.objects.create(category_id=2, product_id=1)
        ProductCategory.objects.create(category_id=2, product_id=2)
        ProductCategory.objects.create(category_id=2, product_id=3)
        ProductCategory.objects.create(category_id=1, product_id=3)

    def tearDown(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        ProductType.objects.all().delete()
        Category.objects.all().delete()
        Image.objects.all().delete()

    def test_product_filter_category_and_type_success(self):
        client = Client()

        response = client.get('/product?category=1')
        self.assertEqual(response.json(), 
            {
                'product_list':[
                    {
                        'image':['test1.test1','test2.test1'],
                        'name':'test1',
                        'price':10000,
                        'discount_rate':10,
                        'discount_price':9000,
                        'product_id':1,
                        'new':True,
                        'free_shipment':False,
                        'sale':False
                    },
                    {
                        'image':[],
                        'name':'test1',
                        'price':10000,
                        'discount_rate':10,
                        'discount_price':9000,
                        'product_id':3,
                        'new':True,
                        'free_shipment':False,
                        'sale':False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_list_category_not_exist(self):
        client = Client()

        response = client.get('/product?category=6')

        self.assertEqual(response.json(), {'message':'NOT FOUND'})
        self.assertEqual(response.status_code, 404)

class ProductDetailTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'test_category1'
        )
        Category.objects.create(
            id   = 2,
            name = 'test_category2'
        )
        ProductType.objects.create(
            id   = 1,
            name = 'test_type1'
        )
        ProductType.objects.create(
            id   = 2,
            name = 'test_type2'
        )
        Product.objects.create(
            id   = 1,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 1,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Product.objects.create(
            id   = 2,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 1,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Product.objects.create(
            id   = 3,
            name = 'test1',
            price = 10000,
            discount_rate = 10,
            product_type_id = 2,
            detail = 'test1',
            sub_detail = 'test1',
            sub_name = 'test1',            
        )
        Image.objects.create(
            image = 'test1.test1',
            product_id = 1
        )
        Image.objects.create(
            image = 'test2.test1',
            product_id = 1
        )
        ProductCategory.objects.create(category_id=1, product_id=1)
        ProductCategory.objects.create(category_id=2, product_id=1)
        ProductCategory.objects.create(category_id=1, product_id=2)
        ProductCategory.objects.create(category_id=2, product_id=3)
        ProductCategory.objects.create(category_id=1, product_id=3)

    def tearDown(self):
        Product.objects.all().delete()
        Image.objects.all().delete()
        Category.objects.all().delete()
        ProductType.objects.all().delete()
        ProductCategory.objects.all().delete()

    def test_get_product_detail_success(self):
        client = Client()

        response = client.get('/product/1')
        self.assertEqual(response.json(), 
            {
                'product_data':[
                    {
                        'image':['test1.test1','test2.test1'],
                        'name':'test1',
                        'price':10000,
                        'discount_rate':10,
                        'discount_price':9000,
                        'product_id':1,
                        'sub_name':'test1',
                        'detail':'test1',
                        'sub_detail':'test1',
                        'free_shipment':False,
                        'sale':False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_not_exist(self):
        client = Client()

        response = client.get('/product/500')
        self.assertEqual(response.json(), {'message':'NOT EXIST'})
        self.assertEqual(response.status_code, 404)