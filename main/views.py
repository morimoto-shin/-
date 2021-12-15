import pandas as pd
from django.shortcuts import render
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
        question = Question(sentence, pos)
        # 英語文と日本語訳がペアになったDataFrameの作成
        df = question.create_sentence_df()
        # データ加工して、英語文と日本語訳に分けたもの
        english, japanese = question.create_data()
        # 単語と品詞ペアのDataFrame
        pos_df = question.create_pos_df()

        print('英語文: ', english[0])
        print('日本語文: ', japanese[0])
        print('単語, 品詞: ', pos_df['単語'][0], pos_df['品詞'][0])

        english_question, japanese_question, answers_list, answer, question_pos = question.question(
            english, japanese, pos_df)
        print('英語問題文: ', english_question)
        print('日本語問題文: ', japanese_question)
        print('答えの選択肢: ', answers_list)
        print('答え: ', answer)
        print('答えの品詞: ', question_pos)

        return render(request, 'main/question.html', {
            'question': sentence
        })

    def request(self, request, *arg, **kwargs):
        return render({

        })
