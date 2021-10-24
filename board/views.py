import json

from django.http  import JsonResponse
from django.views import View

from user.models import User, Board
from user_auth   import authentication

class CreateTextView(View):
    @authentication
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            title = data["title"]
            text  = data["text"]
            user_id  = request.user
        
            if title == "":
                return JsonResponse({"message" : "TITLE EMPTY"}, status = 400)
            
            if len(title) >= 128:
                return JsonResponse({"message" : "TITLE TOO LONG"}, status = 400)

            Board.objects.create(
                title = title,
                text = text,
                user_id = user_id
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class AllTextView(View):
    def get(self, request):
        if not Board.objects.all():
            return JsonResponse({'MESSAGE' : 'TEXT DOES NOT EXISTS'}, status=404)
            
        texts = Board.objects.select_related("user").all()

        return JsonResponse({'title_lists' : [
            {
                'title' : text.title, 
                'user'  : text.user.name, 
            } for text in texts]}, status = 200)

class DetailTextView(View):
    def get(self, request, text_id):
        if not Board.objects.filter(id = text_id).exists():
            return JsonResponse({'MESSAGE' : 'NOT FOUND'}, status = 404)

        text = Board.objects.select_related("user").get(id = text_id)

        return JsonResponse({
            'title'      : text.title,
            'text'       : text.text,
            'created_at' : text.created_at,
            'updated_at' : text.updated_at,
            'user'       : text.user.name,
        })

    @authentication
    def patch(self, request, text_id):
        data = json.loads(request.body)

        try:
            title = data["title"]
            text  = data["text"]

            detail_text = Board.objects.select_related("user").get(id = text_id)
            detail_text.title = title
            detail_text.text = text
            detail_text.save()

            return JsonResponse({"message" : "UPDATE SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
    
    @authentication
    def delete(self, request, text_id):
        detail_text = Board.objects.select_related("user").get(id = text_id)

        detail_text.delete()

        return JsonResponse({"message" : "DELETE COMPLETE"}, status = 200)

class TextSummaryView(View):
    def get(self, request, user_id):
        if not Board.objects.filter(user_id = user_id).exists():
            return JsonResponse({'MESSAGE' : 'NOT FOUND'}, status = 404)
            
        texts = Board.objects.filter(user_id = user_id)

        return JsonResponse({'title_lists' : [
            {
                'title' : text.title, 
                'user'  : text.user.name, 
            } for text in texts]}, status = 200)
