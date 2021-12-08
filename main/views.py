from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Sentence
import pandas as pd
class IndexView(TemplateView):
  template_name = 'main/index.html'

class QuestionView(View):
  def get(self, request, *arg, **kwargs):
    sentence = Sentence.objects.all()
    print('センテンス', len(sentence))
    return render(request, 'main/question.html', {
      'question': sentence
    })
  
  def request(self, request, *arg, **kwargs):
    return render({
      
    })
