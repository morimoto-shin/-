import random
import re
import os
import itertools
import pandas as pd
import nltk


class Question():

    def __init__(self, csv_path, xls_path):
        self.csv_path = csv_path
        self.xls_path = xls_path

    def read_data(self, file_path):
        # ファイルの拡張子の取得
        root, ext = os.path.splitext(file_path)
        if ext == '.csv':
            df = pd.read_csv(file_path)
        if ext == '.xls':
            df = pd.read_excel(file_path)
        return df

    def create_data(self):
        # コーパスからテキスト取得
        df = self.read_data(self.xls_path)

        # 文書ごとのリストを作る
        sentences = []
        japanese = []
        # {}を取り除く
        for sentence, jp in zip(df['用例'].values, df['日本語訳'].values):
            sentences.append(''.join(re.split('[{}]', sentence)))
            japanese.append(jp)

        # 単語と品詞がペアになったDataFrameの作成
        pos_df = self.read_data(self.csv_path)

        return sentences, japanese, pos_df

    def question(self):
        sentences, japanese, pos_df = self.create_data()
        import random
        # 問題となる文をランダムに取得
        question_sent_idx = random.choice(range(len(sentences)))
        question_sent = sentences[question_sent_idx]
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
        return japanese_question, english_question, answer, question_pos

    def judge_answer(self, response, answer):
        while(1):
            wrong_answer = random.sample(
                pos_df.loc[pos_df['pos_tag'] == question_pos, 'word'].values.tolist(), 3)

            def has_duplicates(seq):
                return len(seq) != len(set(seq))
            if answer in wrong_answer:
                continue
            elif has_duplicates([str.lower(x) for x in wrong_answer]):
                continue
            else:
                break
        answers = wrong_answer
        answers.append(answer)
        answers_list = random.sample(answers, len(answers))
        if answers_list[response-1] == answer:
            """正解だったら「正解です」表示をする"""
        else:
            """「間違えです」表示をする"""
