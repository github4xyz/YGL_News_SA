#%%

from operator import concat
import os
from pykrx import stock
import pandas as pd
import datetime
import time



import warnings
warnings.filterwarnings('ignore')


code_names = pd.read_csv('./news/code_stock_name_b.csv')
today = time.strftime('%Y%m%d')

for i in range(0, code_names.shape[0]-1):
  x = code_names['code'][i]
  code = '{0:06d}'.format(int(x))
  name = code_names['name'][i]
  data =  [['{0:06d}'.format(int(code_names['code'][i])), code_names['name'][i]]]
  codename = pd.DataFrame(data, columns = ['code', 'name'])
  read_df_date = stock.get_market_fundamental_by_date(today, today, code)
  print(read_df_date)
  codename.reset_index(drop=True, inplace=True)
  read_df_date.reset_index(drop=True, inplace=True)
  fundametal = pd.concat([codename, read_df_date], axis=1)
  fundametal.to_csv('./fundamental/'+today+'-'+str(code)+'_'+name+'_fundamental.tsv', sep='\t')

# print(read_df_date.shape)
# print(read_df_date)


# for i in range(0, code_names.shape[0]-1):
#   read_df = stock.get_market_fundamental_by_ticker("20210108", )

#   for ir in range(0, read_df.shape[0]-1):
#     read = [read_df['news'][ir]]
#     read_df['mlp'][ir], read_df['mlb'][ir] = logiReg.logiRegPredict(read)
#     dl_results = tf.sigmoid(reloaded_model(tf.constant(read)))
#     read_df['dlp'][ir], read_df['dlb'][ir] = bert_result.calcReuslt(dl_results)
#   read_df.to_csv('./news/'+str("{:06d}".format(code_names['code'][i]))+'_'+code_names['name'][i]+'_news_tested.tsv', sep='\t')





# 파일 저장
# result.to_csv('./temp/'+code+'_'+stock_name+'_주가데이터.tsv', sep='\t')




# %%
