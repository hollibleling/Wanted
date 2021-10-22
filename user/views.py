import json
import re
import bcrypt
import jwt

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from user.models import User
from my_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        data           = json.loads(request.body)
        email_regex    = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*+=-]).{9,16}$')
    
        try:
            name     = data['name']
            email    = data['email']
            password = data['password']
            mobile   = data['mobile']

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "EXIST USER"}, status = 400)

            if not email_regex.match(email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)

            if not password_regex.match(password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)

            User.objects.create(
                    name     = name, 
                    email    = email, 
                    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
                    mobile   = mobile, 
                )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            if User.objects.filter(email = email).exists():
                user_account = User.objects.get(email = email)
                if bcrypt.checkpw(password.encode('utf-8'), user_account.password.encode('utf-8')):
                    token = jwt.encode({'id' : user_account.id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({"message" : "LOGIN_SUCCESS", "token" : token}, status = 200)
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 401)
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
