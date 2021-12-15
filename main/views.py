from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

class IndexView(TemplateView):
  template_name = 'main/index.html'

class QuestionView(View):
  def get(self, request, *arg, **kwargs):
    question = {}
    answer = 1
    self.answer = answer
    return render(request, 'main/question.html', {
      'question': question,
    })
    
  def post(self, request, *args, **kwargs):
    if 'btn_1' in request.POST:
      input_answer = 1
      if self.answer == input_answer:
        return redirect('/main/answer')
      else:
        return redirect('/main/wrong')
    elif 'btn_2' in request.POST:
      input_answer = 2
      if self.answer == input_answer:
        return redirect('/main/answer')
      else:
        return redirect('/main/wrong')
    elif 'btn_3' in request.POST:
      input_answer = 3
      if self.answer == input_answer:
          return redirect('/main/answer')
      else:
        return redirect('/main/wrong')
    elif 'btn_4' in request.POST:
      input_answer = 4
      if self.answer == input_answer:
          return redirect('/main/answer')
      else:
        return redirect('/main/wrong')

    return render(request, 'main/question.html', {
    })


class AnswerView(View):
  def post(self, request, *args, **kwargs):
    return render(request, 'main/answer.html', {
      ''
    })
    
class WrongAnswerView(View):
  def post(self, request, *args, **kwargs):
    return render(request, 'main/wrong_answer.html', {
      ''
    })
