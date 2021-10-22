import json
import unittest
import bcrypt
import jwt

from user.models import User
from django.test import TestCase, Client
from my_settings import SECRET_KEY

class SignUpViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            name = "홍길동",
            email = "wecoder@naver.com",
            password = "1234qwer!@",
            mobile = "010-1111-1111"
        )
 
    def tearDown(self):
        User.objects.all().delete()

    def test_signup_exist_user_error(self):
        client = Client()

        user = {
            "name"     : "홍길동", 
            "email"    : "wecoder@naver.com", 
            "password" : "1234qwer!@", 
            "mobile"   : "010-1234-5678",
        }

        response = client.post("/user/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "EXIST USER"})
        self.assertEqual(response.status_code, 400)

    
    def test_signup_invalid_email_error(self):
        client = Client()

        user = {
            "name"     : "김정수", 
            "email"    : "wanted@navercom", 
            "password" : "1234qwer!@", 
            "mobile"   : "010-1234-5678",
        }

        response = client.post("/user/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "INVALID_EMAIL"})
        self.assertEqual(response.status_code, 400)
        

    def test_signun_invalid_password_error(self):
        client = Client()

        user = {
            "name"     : "김정수", 
            "email"    : "wanted@naver.com", 
            "password" : "1234567!@", 
            "mobile"   : "010-1234-5678",
        }

        response = client.post("/user/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "INVALID_PASSWORD"})
        self.assertEqual(response.status_code, 400)


    def test_signup_success(self):
        client = Client()

        user = {
            "name"     : "김정수", 
            "email"    : "wanted@naver.com", 
            "password" : "1234qwer!@", 
            "mobile"   : "010-1234-5678",
        }

        response = client.post("/user/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "SUCCESS"})
        self.assertEqual(response.status_code, 201)


    def test_signup_key_erorr(self):
        client = Client()

        user = {
            "name"     : "김정수", 
            "email"    : "wanted@naver.com", 
            "password" : "1234qwer!@", 
        }

        response = client.post("/user/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)


class SignInViewTest(TestCase):
    def setUp(self):
        password = "1234qwer!@"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
            name = "김정수",
            email = "wanted@naver.com",
            password = hashed_password,
            mobile = "010-1234-5678"
        )
 
    def tearDown(self):
        User.objects.all().delete()

    def test_signin_success(self):
        client = Client()

        user = {
            "email"    : "wanted@naver.com", 
            "password" : "1234qwer!@", 
        }

        response = client.post("/user/signin", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "LOGIN_SUCCESS", "token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.jyLCgMloNjfH2xze_VleQaqy-9VulZ3jOjc0wNiy9fQ"})
        self.assertEqual(response.status_code, 200)


    def test_signin_invalid_password_error(self):
        client = Client()

        user = {
            "email"    : "wanted@naver.com", 
            "password" : "1234qwer!", 
        }

        response = client.post("/user/signin", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "INVALID_PASSWORD"})
        self.assertEqual(response.status_code, 401)


    def test_signin_invalid_user_error(self):
        client = Client()

        user = {
            "email"    : "wanted1@naver.com", 
            "password" : "1234qwer!@", 
        }

        response = client.post("/user/signin", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "INVALID_USER"})
        self.assertEqual(response.status_code, 401)

    
    def test_signin_key_error(self):
        client = Client()

        user = {
            "email"    : "wanted@naver.com", 
            "password1" : "1234qwer!@", 
        }

        response = client.post("/user/signin", json.dumps(user), content_type="application/json")

        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)
