
import scipy as sp
import pandas as pd
import numpy as np
import pickle


from konlpy.tag import Okt         ; t = Okt()     # 구 트위터

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')


with open('C:\MG\Python\myPackage\\backtest\clf_lr.pkl','rb') as fp:     # 읽기
    clf = pickle.load(fp)


count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()
with open('C:\MG\Python\myPackage\\backtest\count_vect.pkl', 'rb') as f:
    count_vect = pickle.load(f)
with open('C:\MG\Python\myPackage\\backtest\\tfidf_transformer.pkl', 'rb') as f:
    tfidf_transformer = pickle.load(f)


#토큰화 및 토큰화 과정에서 불용어를 제거하는 함수
def preprocessing(data):
  tokenizer = Okt()
  text_data = []
  stopwords = ['\u200c','\n ','\n',"'",'…',',','[',']','(',')','"','주','에','·','장','-','적',\
    '도','‘','`','가','’','의','이','★','은','“','대','”','한','B','로',\
      '?','선','A','는','!','"…','상','들','제','…"','일','서','명',"'…",'기',\
        '···','소','등','자','전','률','미','...','세','시','안','폭',"…'",'만','억',\
          '눈','더','량','고','인','성','다','감','을','지','수','것','째',\
            '기','···','중','계','왜','총','내','과','젠','또','연','엔','차','할',\
              '새','사','때','..','임','속','’…','G','나','개','원',\
                '달','→','권','?…','간','배','K','저','와','하','/','조','두','분','형',\
                  '황','공','&','보','문','익','X','억원',']"','치','산','를','오','해','S','그','된','준','▶',\
                    '건','재','반','라','년','초','분','월','신','p','급','줄','경','구','진','올','발','vs','강',\
                      '국','난','판','면','"(','`…','살','아','번','텍','팜','Q','메','점','월',\
                        'D','비','됐다','채',"]'",'보니','손','확','종','동','팔','타','~','땐','말','요',\
                          "',",'스','…`','단','길','회','호','용','듯','최']

  for sentence in data:
    temp_data =[]
    # 토큰화
    temp_data = tokenizer.morphs(sentence)
    #불용어 제거
    temp_data = [word for word in temp_data if not word in stopwords]
    text_data.append(temp_data)
  text_data = list(map(' '.join, text_data))
  return text_data


def tfidf_vectorizer(data):

  data_counts = count_vect.transform(data)
  data_tfidf = tfidf_transformer.transform(data_counts)
  return data_tfidf

# new_sent = preprocessing(["민주당 일각에서 법사위의 체계·자구 심사 기능을 없애야 한다는 \
#                            주장이 나오는 데 대해 “체계·자구 심사가 법안 지연의 수단으로 \
#                           쓰이는 것은 바람직하지 않다”면서도 “국회를 통과하는 법안 중 위헌\
#                           법률이 1년에 10건 넘게 나온다. 그런데 체계·자구 심사까지 없애면 매우 위험하다”고 반박했다."])

# r1 = np.max(clf.predict_proba(tfidf_vectorizer(new_sent))*100)
# r2 = clf.predict(tfidf_vectorizer(new_sent))
# print(r1)
# print(r2)


def logiRegPredict(new_sent):
    r1 = np.max(clf.predict_proba(tfidf_vectorizer(new_sent))*100)
    r2 = np.bincount(clf.predict(tfidf_vectorizer(new_sent))).argmax()
    return r1, r2


