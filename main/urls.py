from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('question', views.QuestionView.as_view(), name='question'),
  path('answer', views.AnswerView.as_view(), name='answer'),
  path('wrong_answer', views.WrongAnswerView.as_view(), name='wrong_answer')
]
