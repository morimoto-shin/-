from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
  print('viewファイルは実行されている')
  template_name = 'main/index.html'