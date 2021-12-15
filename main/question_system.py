# 必要なライブラリのインポート
import os
import re
import random
import pandas as pd
import nltk


class Question():

    def __init__(self, sentence, pos):
        self.sentence = sentence
        self.pos = pos

    def create_sentence_df(self):
        japanese = self.sentence.objects.values_list(
            'japanese_question')
        english = self.sentence.objects.values_list(
            'english_question')
        df = pd.DataFrame([english, japanese]).T
        df.columns = ['用例', '日本語訳']
        return df

    def create_pos_df(self):
        word = self.pos.objects.values_list('word')
        pos_tag = self.pos.objects.values_list('pos_tag')
        df = pd.DataFrame([word, pos_tag]).T
        df.columns = ['単語', '品詞']
        df['単語'] = df['単語'].astype(str).str.strip("[{}(),.]'`")
        df['品詞'] = df['品詞'].astype(str)
        return df

    def create_data(self):
        # テキスト取得
        df = self.create_sentence_df()

        # 文書ごとのリストを作る
        sentences = []
        japanese = []
        # {}, ()を取り除く
        for sentence, jp in zip(df['用例'].astype(str).values, df['日本語訳'].astype(str).values):
            sentences.append(''.join(re.split('[{}()]', sentence)))
            japanese.append(''.join(re.split('[{}()]', jp)))
        return sentences, japanese

    def question(self, english, japanese, pos_df):
        import random
        # 問題となる文をランダムに取得
        question_sent_idx = random.choice(range(len(english)))
        question_sent = english[question_sent_idx]
        japanese_sent = japanese[question_sent_idx]

        while(1):
            # 問題文を単語ごとに分割
            question_sent_words = nltk.word_tokenize(question_sent)
            # 問題文を単語ごとに分割した時のリストからランラムにインデックス番号を取得
            question_word_index = random.choice(
                range(len(nltk.word_tokenize(question_sent))))
            # 取得したインデックス番号に対応する単語を取得
            question_word = question_sent_words[question_word_index]

            # 問題文のそれぞれの単語の品詞を取得
            question_sent_pos = nltk.pos_tag(question_sent_words)

            # もし、選択可能でない品詞のものならもう一度実行し直す
            if question_sent_pos[question_word_index][1] in ['NNP', 'NNPS', 'FW', 'LS', 'SYM', ',', '.']:
                continue
            # それ以外なら、answerとして答えを変数として格納する
            else:
                answer = question_word
                question_pos = question_sent_pos[question_word_index][1]
                break

        # 問題文の作成
        question_sent_words[question_word_index] = '____'
        question = ' '.join(question_sent_words)

        # 日本語文での問題
        japanese_question = japanese_sent
        # 英語文での問題
        english_question = question

        # 間違えの選択肢の作成

        def has_duplicates(seq):
            return len(seq) != len(set(seq))
        while(1):
            wrong_answer = random.sample(
                pos_df.loc[pos_df['品詞'] == str("('"+question_pos+"',)"), '単語'].values.tolist(), 3)
            if answer in wrong_answer:
                continue
            elif has_duplicates([str.lower(x) for x in wrong_answer]):
                continue
            else:
                break

        # 選択肢たち
        answers = wrong_answer
        answers.append(answer)
        answers_list = random.sample(answers, len(answers))

        # 答えのインデックス番号の取得
        for index, a in enumerate(answers_list):
            if a in answer:
                answer_index = index + 1
        return english_question, japanese_question, answers_list, answer, answer_index, question_pos
