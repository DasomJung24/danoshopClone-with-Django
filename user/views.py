import jwt
import bcrypt
import json
import datetime

from django.views    import View
from django.http     import JsonResponse
from my_settings     import SECRET, ALGORITHM
from .models         import User



class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        MINIMUM_PASSWORD = 6
        MAXIMUM_PASSWORD = 30

        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'EMAIL EXIST'}, status=400)

            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if data['password'] == '' or data['email'] == '' or data['name'] == '':
                return JsonResponse({'message':'INVALID_REQUEST'}, status=400)

            if len(data['password']) < MINIMUM_PASSWORD or len(data['password']) > MAXIMUM_PASSWORD:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User(
                email    = data['email'],
                password = password,
                name     = data['name'],
                birth    = data.get('birth',None),
                job      = data.get('job',None),
                gender   = data.get('gender',None)
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if data['email'] == '' or data['password'] == '':
                return JsonResponse({'message':'INVALID REQUEST'}, status=400)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID USER'}, status=400)

            new_password = data['password']
            user         = User.objects.get(email=data['email'])
            password     = user.password

            if not bcrypt.checkpw(new_password.encode('utf-8'), password.encode('utf-8')):
                return JsonResponse({'message':'WRONG_PASSWORD'}, status=400)

            expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)

            access_token = jwt.encode({'user_id':user.id, 'exp':expire}, SECRET['secret'], algorithm=ALGORITHM).decode('utf-8')

            return JsonResponse({'Authorization':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)