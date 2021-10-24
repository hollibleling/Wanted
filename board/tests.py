import json
import unittest
import re
import jwt

from django.test import TestCase, Client
from user.models import User, Board
from my_settings import SECRET_KEY

class CreateTextViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "홍길동",
            email    = "wecoder@naver.com",
            password = "1234qwer!@",
            mobile   = "010-1111-1111"
        )

        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, algorithm='HS256')

        Board.objects.create(
            id      = 1,
            title   = "안녕하세요~",
            text    = "처음 뵙겠습니다~!", 
            user_id = User.objects.get(id=1).id
        )

        Board.objects.create(
            id      = 2,
            title   = "다시 또 뵙네요.",
            text    = "잘 부탁 드립니다.", 
            user_id = User.objects.get(id=1).id
        )
 
    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()

    def test_create_text_success(self):
        client = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')
        user_id    = User.objects.get(id = payload['id']).id

        text = {
            "id"      : "3",
            "title"   : "수원에 사는 공대생입니다.",
            "text"    : "잘 부탁 드립니다.",
            "user_id" : user_id
        }

        response = client.post("/board/create", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "SUCCESS"})
        self.assertEqual(response.status_code, 201)
    
    def test_create_text_empty_title_error(self):
        client = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "id"      : "3",
            "title"   : "",
            "text"    : "잘 부탁 드립니다.",
        }

        response = client.post("/board/create", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "TITLE EMPTY"})
        self.assertEqual(response.status_code, 400)

    def test_create_text_too_long_title_error(self):
        client = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "id"      : "3",
            "title"   : "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "text"    : "잘 부탁 드립니다.",
        }

        response = client.post("/board/create", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "TITLE TOO LONG"})
        self.assertEqual(response.status_code, 400)

    def test_create_text_key_error(self):
        client = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "id"      : "3",
            "title"   : "수원에 사는 공대생입니다",
            "texts"    : "잘 부탁 드립니다.",
        }

        response = client.post("/board/create", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)


class AlllTextViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "김정수",
            email    = "wecoder@naver.com",
            password = "1234qwer!@",
            mobile   = "010-1111-1111"
        )

        Board.objects.create(
            id      = 1,
            title   = "안녕하세요~",
            text    = "처음 뵙겠습니다~!", 
            user_id = 1
        )

        Board.objects.create(
            id      = 2,
            title   = "다시 또 뵙네요.",
            text    = "잘 부탁 드립니다.", 
            user_id = 1
        )

    def tearDown(self):
        Board.objects.all().delete()
        Board.objects.all().delete()

    def test_all_text_view_success(self):
        client   = Client()
        response = client.get('/board/text?page=1')

        self.assertEqual(response.json(), 
            {"title_lists": [
                    {
                        "title": "다시 또 뵙네요.",
                        "user": "김정수"
                        },
                    {
                        "title": "안녕하세요~",
                        "user": "김정수"
                        }]
            })

        self.assertEqual(response.status_code, 200)
    
    def test_all_text_view_wrong_request_error(self):
        client   = Client()
        response = client.get('/board/text?page=-1')

        self.assertEqual(response.json(), {'message' : 'WRONG REQUEST'})
        self.assertEqual(response.status_code, 404)

class AllTextViewEmptyTest(TestCase):
    def test_all_text_view_not_exist_error(self):
        client   = Client()
        response = client.get('/board/text')

        self.assertEqual(response.json(), {'message' : 'TEXT DOES NOT EXISTS'})
        self.assertEqual(response.status_code, 404)

class DetailTextViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "김정수",
            email    = "wecoder@naver.com",
            password = "1234qwer!@",
            mobile   = "010-1111-1111"
        )

        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, algorithm='HS256')
        self.token1 = jwt.encode({'id' : 2}, SECRET_KEY, algorithm='HS256')

        Board.objects.create(
            id      = 1,
            title   = "안녕하세요~",
            text    = "처음 뵙겠습니다~!", 
            user_id = 1
        )

        Board.objects.create(
            id      = 2,
            title   = "다시 또 뵙네요.",
            text    = "잘 부탁 드립니다.", 
            user_id = 1
        )

    def tearDown(self):
        Board.objects.all().delete()
        Board.objects.all().delete()

    def test_detail_text_view_get_suscces(self):
        client   = Client()
        response = client.get('/board/1')
        text = Board.objects.get(id=1)

        self.assertEqual(response.json(), 
            {
                "title": "안녕하세요~",
                "text": "처음 뵙겠습니다~!",
                "created_at": text.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                "updated_at": text.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                "user": "김정수"
                }
            )

        self.assertEqual(response.status_code, 200)
    
    def test_detail_text_view_patch_success(self):
        client   = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "title"   : "수정하려고 합니다.",
            "text"    : "문제없죠?",
        }

        response = client.patch("/board/1", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "UPDATE SUCCESS"})
        self.assertEqual(response.status_code, 201)
    
    def test_detail_text_view_patch_invalid_user_error(self):
        client   = Client()
        header  = {"HTTP_Authorization" : self.token1}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "title"   : "수정하려고 합니다.",
            "user"    : "문제없죠?",
        }

        response = client.patch("/board/1", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"MESSAGE" : "INVALID USER"})
        self.assertEqual(response.status_code, 403)
    
    def test_detail_text_view_patch_key_error(self):
        client   = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        text = {
            "title"   : "수정하려고 합니다.",
            "user"    : "문제없죠?",
        }

        response = client.patch("/board/1", json.dumps(text), **header, content_type="application/json")

        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_detail_text_view_delete_success(self):
        client   = Client()
        header  = {"HTTP_Authorization" : self.token}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        response = client.delete("/board/1", **header, content_type="application/json")
    
        self.assertEqual(response.json(), {"message" : "DELETE COMPLETE"})
        self.assertEqual(response.status_code, 200)

    def test_detail_text_view_delete_invalid_user_error(self):
        client   = Client()
        header  = {"HTTP_Authorization" : self.token1}
        token   = header["HTTP_Authorization"]
        payload = jwt.decode(token, SECRET_KEY, algorithms = 'HS256')

        response = client.delete("/board/1", **header, content_type="application/json")

        self.assertEqual(response.json(), {"MESSAGE" : "INVALID USER"})
        self.assertEqual(response.status_code, 403)

class TextSummaryViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = "김정수",
            email    = "wecoder@naver.com",
            password = "1234qwer!@",
            mobile   = "010-1111-1111"
        )

        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, algorithm='HS256')

        Board.objects.create(
            id      = 1,
            title   = "안녕하세요~",
            text    = "처음 뵙겠습니다~!", 
            user_id = 1
        )

        Board.objects.create(
            id      = 2,
            title   = "다시 또 뵙네요.",
            text    = "잘 부탁 드립니다.", 
            user_id = 1
        )

    def tearDown(self):
        Board.objects.all().delete()
        Board.objects.all().delete()

    def test_text_summary_get_success(self):
        client   = Client()
        response = client.get('/board/user/1?page=1')

        self.assertEqual(response.json(), 
            {"title_lists": [
                    {
                        "title": "다시 또 뵙네요.",
                        "user": "김정수"
                        },
                    {
                        "title": "안녕하세요~",
                        "user": "김정수"
                        }]
            })

        self.assertEqual(response.status_code, 200)
    
    def test_text_summary_ger_not_found_error(self):
        client   = Client()
        response = client.get('/board/user/2')

        self.assertEqual(response.json(), {'MESSAGE' : 'NOT FOUND'})
        self.assertEqual(response.status_code, 404)
