import random
import re
import itertools
import pandas as pd
import nltk
import spacy
import requests
from bs4 import BeautifulSoup

# コーパスからテキスト取得
df = pd.read_excel('SCoRE.xls')

# 文書ごとのリストを作る
sentences = []
japanese = []
# {}を取り除く
for sentence, jp in zip(df['用例'].values, df['日本語訳'].values):
    sentences.append(''.join(re.split('[{}]', sentence)))
    japanese.append(jp)

# 文書ごとに分かち書き
word = []
for text in sentences:
    word.append(nltk.word_tokenize(text))
words = list(itertools.chain.from_iterable(word))

# 単語ごとの品詞の取得
pos = nltk.pos_tag(words)

# 単語と品詞がペアになったDataFrameの作成
pos_df = pd.read_csv('word_pos.csv')


# 問題

print('\n次の文章の空欄に当てはまる単語を選択肢の中から選び、数字で答えなさい。')

cnt = 0
correct_num = 0
while(1):
    cnt += 1
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
    question_sent_words[question_word_index] = ' ____ '
    question = ' '.join(question_sent_words)
    print(f'Question{cnt}: {japanese_sent}')
    print(question)
    print('----------------------------------------------------------')

    # 同じ品詞のものを取得
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
    for i, ans in enumerate(answers_list):
        print(f'{i+1}: {ans}')

    response = int(input('Which number is Correct?'))
    if answers_list[response-1] == answer:
        correct_num += 1
        print('Correct!!')
    else:
        print('Wrong!!')
        print(f'Correct answer is: {answer}')

    print('----------------------------------------------------------')
    if cnt % 10 == 0:
        is_continue = input('まだ続けますか？(y/n)')
        if is_continue == 'y':
            continue
        else:
            print('正答率: ', (correct_num / cnt) * 100, '%')
            break
