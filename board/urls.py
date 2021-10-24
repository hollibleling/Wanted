from django.urls import path

from board.views import CreateTextView, AllTextView, DetailTextView, TextSummaryView

urlpatterns = [
    path('/create', CreateTextView.as_view()),
    path('/text', AllTextView.as_view()), 
    path('/<int:text_id>', DetailTextView.as_view()),
    path('/user/<int:user_id>', TextSummaryView.as_view()), 
]