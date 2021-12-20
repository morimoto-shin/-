import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .question_system import Question
from .models import Sentence, Pos


class IndexView(TemplateView):
    template_name = 'main/index.html'


class QuestionView(View):
    def get(self, request, *arg, **kwargs):
        sentence = Sentence  # 英語文と日本語訳のペア
        pos = Pos  # 品詞と単語のペア
        # questionインスタンスの作成
        question_class = Question(sentence, pos)
        # 英語文と日本語訳がペアになったDataFrameの作成
        df = question_class.create_sentence_df()
        # データ加工して、英語文と日本語訳に分けたもの
        english, japanese = question_class.create_data()
        # 単語と品詞ペアのDataFrame
        pos_df = question_class.create_pos_df()
        question = question_class.question(english, japanese, pos_df)
        print('クエスチョン:', question)
        return render(request, 'main/question.html', {
            'question': question
        })

    def post(self, request, *args, **kwargs):
      input_answer = '1'
      question_answer = request.POST.get('btn_1')
      print('リクエスト',request.POST, question_answer, input_answer == question_answer)
      if 'btn_1' in request.POST:
        input_answer = '1'
        question_answer = request.POST.get('btn_1')
        print('回答',input_answer, question_answer)
        if question_answer == input_answer:
          return redirect('/main/answer')
        else:
          return redirect('/main/wrong_answer')
      elif 'btn_2' in request.POST:
        input_answer = '2'
        question_answer = request.POST.get('btn_2')
        print('回答',input_answer, question_answer)
        if question_answer == input_answer:
          return redirect('/main/answer')
        else:
          return redirect('/main/wrong_answer')
      elif 'btn_3' in request.POST:
        input_answer = '3'
        question_answer = request.POST.get('btn_3')
        print('回答',input_answer, question_answer)
        if question_answer == input_answer:
            return redirect('/main/answer')
        else:
          return redirect('/main/wrong_answer')
      elif 'btn_4' in request.POST:
        input_answer = '4'
        question_answer = request.POST.get('btn_4')
        print('回答',input_answer, question_answer)
        if question_answer == input_answer:
            return redirect('/main/answer')
        else:
          return redirect('/main/wrong_answer')
      return render(request, 'main/question.html', {})

class AnswerView(View):
    def get(self, request, *args, **kwargs):
      return render(request, 'main/answer.html')

class WrongAnswerView(View):
    def get(self, request, *args, **kwargs):
      return render(request, 'main/wrong_answer.html')
