import numpy as np
import pandas as pd
import re


from konlpy.tag import Okt         ; t = Okt()     # 구 트위터
from konlpy.tag import *


import pickle

# Load pickle
with open('./with_name/with_len_okt.pkl', 'rb') as f:
    df_without = pickle.load(f)
with open('./with_name/with_up_unique.pkl', 'rb') as f:
    up_only_unique = pickle.load(f)
with open('./with_name/with_down_unique.pkl', 'rb') as f:
    down_only_unique = pickle.load(f)


idx=0
df_without['u_score'] = ''
df_without['u_words'] = ''
for sen in df_without['okt']:
    temp = list()
    # print(i)
    for i in sen:
        for c in up_only_unique:
            score = 0
            if i == c:
                score +=1
                temp.append(c)
            df_without.at[idx,'u_score'] = score
        df_without.at[idx,'u_words'] = temp
    idx += 1



print("d_score: starts")
idx=0
df_without['d_score'] = ''
df_without['d_words'] = ''
for sen in df_without['okt']:
    temp = list()
    for i in sen:
        for c in down_only_unique:
            score = 0
            if i == c:
                score -=1
                temp.append(c)
            df_without.at[idx,'d_score'] = score
        df_without.at[idx,'d_words'] = temp
    idx += 1


# Save pickle
with open('./with_name/with_score_words.pkl', 'wb') as f:
    pickle.dump(df_without, f)

df_without.sample(30)