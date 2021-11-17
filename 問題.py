import random
import pandas as pd
import nltk
import spacy
import requests
from bs4 import BeautifulSoup

# スクレイピングでデータ取得
url = 'https://www.bbc.com/news/science-environment-59253928'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

texts = soup.find_all('div', class_="ssrcss-uf6wea-RichTextComponentWrapper e1xue1i86")
all_text = []
for text in texts:
    all_text.append(text.text)
text = ''.join(all_text)

# 文章ごとのリストを作る
nlp = spacy.load('en_core_web_sm')
spacy_text = nlp(text)
sentences = []
for sent in spacy_text.sents:
    sentences.append(sent)
    
# 文書ごとに分かち書き
words = nltk.word_tokenize(text)

# 単語ごとの品詞の取得
pos = nltk.pos_tag(words)

# 単語と品詞がペアになったDataFrameの作成
df = pd.DataFrame()
df['word'] = None
df['pos_tag'] = None
for p in pos:
    df = df.append({'word': p[0], 'pos_tag': p[1]}, ignore_index=True)
    
    
# 問題    

print('\n次の文章の空欄に当てはまる単語を選択肢の中から選び、数字で答えなさい。')

cnt = 0
correct_num = 0
while(1):
    cnt+=1
    import random
    # 問題となる文をランダムに取得
    question_sent = str(random.choice(sentences))

    while(1):
        # 問題文を単語ごとに分割
        question_sent_words = nltk.word_tokenize(question_sent)
        # 問題文を単語ごとに分割した時のリストからランラムにインデックス番号を取得
        question_word_index = random.choice(range(len(nltk.word_tokenize(question_sent))))
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
    print(f'Question{cnt}:')
    print(question)
    print('----------------------------------------------------------')


    # 同じ品詞のものを取得
    while(1):
        wrong_answer = random.sample(df.loc[df['pos_tag'] == question_pos, 'word'].values.tolist(), 3)
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
