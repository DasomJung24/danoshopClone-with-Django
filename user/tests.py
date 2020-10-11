from django.test import TestCase, Client
from my_settings import SECRET, ALGORITHM
from .models     import User
from .utils      import login_decorator
import jwt
import bcrypt
import json
import datetime

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            name     = 'tom',
            email    = 'test1@naver.com',
            password = '1234567'
        )
    
    def tearDown(self):
        User.objects.filter(name='tom').delete()

    def test_sign_up_post_success(self):
        client = Client()

        user = {
            'name'     : 'jeny',
            'email'    : 'test2@naver.com',
            'password' : '9999999'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_key_error(self):
        client = Client()

        user = {
            'nam'      : 'jeny',
            'email'    : 'test2@naver.com',
            'password' : '9999999'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'KEY ERROR'})
        self.assertEqual(response.status_code, 400)

    def test_signup_email_exist_error(self):
        client = Client()

        user = {
            'name'     : 'jeny',
            'email'    : 'test1@naver.com',
            'password' : '9999999'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'EMAIL EXIST'})
        self.assertEqual(response.status_code, 400)

    def test_email_invalid(self):
        client = Client()

        user = {
            'name'     : 'jeny',
            'email'    : 'test2naver.com',
            'password' : '9999999'
        }        

        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID_EMAIL'})
        self.assertEqual(response.status_code, 400)

    def test_signup_nothing_in_data(self):
        client = Client()

        user = {
            'name'     : '',
            'email'    : 'test2@naver.com',
            'password' : '9999999'
        }    

        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID_REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_signup_password_shorter_than_minimum(self):
        client = Client()

        user = {
            'name'     : 'jeny',
            'email'    : 'test2@naver.com',
            'password' : '999'
        }

        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})
        self.assertEqual(response.status_code, 400)

    def test_signup_password_longer_than_maximum(self):
        client = Client()

        user = {
            'name'     : 'jeny',
            'email'    : 'test2@naver.com',
            'password' : '999999999999999999999999999999999999999999999999999999'
        }

        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})
        self.assertEqual(response.status_code, 400)

class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            name     = 'james', 
            email    = 'test123@naver.com',
            password = bcrypt.hashpw('123456789'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.filter(name='james').delete()

    def test_signin_post_success(self):
        client = Client()

        user = {
            'email'    : 'test123@naver.com',
            'password' : '123456789'
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_signin_nothin_in_data(self):
        client = Client()

        user = {
            'email'    : '',
            'password' : '123456789'
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID REQUEST'})
        self.assertEqual(response.status_code, 400)

    def test_signin_email_not_exist(self):
        client = Client()

        user = {
            'email'    : 'test145@naver.com',
            'password' : '123456789'
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'INVALID USER'})
        self.assertEqual(response.status_code, 400)

    def test_signin_wrong_password(self):
        client = Client()

        user = {
            'email'    : 'test123@naver.com',
            'password' : '1234569'
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'WRONG_PASSWORD'})
        self.assertEqual(response.status_code, 400)

    def test_signin_key_error(self):
        client = Client()

        user = {
            'email'   : 'test123@naver.com',
            'pasword' : '123456789'
        }

        response = client.post('/user/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.json(), {'message':'KEY ERROR'})
        self.assertEqual(response.status_code, 400)