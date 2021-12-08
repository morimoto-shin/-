from django.db import models
from django.db.models.fields import CharField

class Pos(models.Model):
  word = CharField('単語', max_length=20)
  pos_tag = CharField('品詞', max_length=20)

class Sentence(models.Model):
  japanese_question = models.CharField('日本語問題文', max_length=50)
  english_question = models.CharField('英語問題文', max_length=50)