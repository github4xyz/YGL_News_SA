

import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
tf.get_logger().setLevel('ERROR')

from pykrx import stock
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

import urllib
import pickle

import warnings
warnings.filterwarnings('ignore')


import bert_result
import logiReg

saved_model_path = './NaverNews_bert_multi_with_final'
reloaded_model = tf.saved_model.load(saved_model_path)

code_names = pd.read_csv('./news/code_stock_name.csv', sep='\t', dtype=str)
# code_names = code_name[~code_name.code.str.contains('K')]
code_names.to_csv('./news/code_stock_name_tested.csv', index=False, sep='\t')

for i in range(0, code_names.shape[0]):
  x = code_names['code'][i]
  code = '{0:06d}'.format(int(x))
  name = code_names['name'][i]
  read_df = pd.read_csv('./news/'+str(code)+'_'+name+'_news.tsv', sep='\t')
  read_df['mlp'] = 0
  read_df['mlb'] = 0
  read_df['dlp'] = 0
  read_df['dlb'] = 0
  for ir in range(0, read_df.shape[0]-1):
    read = [read_df['news'][ir]]
    if len(read_df['news'][ir]) > 2:
      read_df['mlp'][ir], read_df['mlb'][ir] = logiReg.logiRegPredict(read)
      dl_results = tf.sigmoid(reloaded_model(tf.constant(read)))
      read_df['dlp'][ir], read_df['dlb'][ir] = bert_result.calcReuslt(dl_results)
  read_df.to_csv('./news/'+str(code)+'_'+name+'_news_tested.tsv', sep='\t')


# read_df = pd.read_csv('./news/000660_SK하이닉스_news.tsv', sep='\t')
# read_df['mlp'] = 0
# read_df['mlb'] = 0
# read_df['dlp'] = 0
# read_df['dlb'] = 0
# count = 0
# for ir in range(0, 15):
#   read = [read_df['news'][ir]]
#   readx = read_df['news'][ir]
#   print(read)
#   print(readx)
#   if len(readx) > 2:
#     print(count)
#     count += 1
#     read_df['mlp'][ir], read_df['mlb'][ir] = logiReg.logiRegPredict(read)
#     # dl_results = tf.sigmoid(reloaded_model(tf.constant(read)))
#     # read_df['dlp'][ir], read_df['dlb'][ir] = bert_result.calcReuslt(dl_results)
# read_df.to_csv('./news/000660_SK하이닉스_news_tested.tsv', sep='\t')




# 파일 저장
# result.to_csv('./temp/'+code+'_'+stock_name+'_주가데이터.tsv', sep='\t')



