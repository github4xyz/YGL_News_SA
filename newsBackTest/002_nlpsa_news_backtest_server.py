
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
tf.get_logger().setLevel('ERROR')
import warnings
warnings.filterwarnings('ignore')

import bert_result
import logiReg

saved_model_path = './NaverNews_bert_multi_with_final'
reloaded_model = tf.saved_model.load(saved_model_path)

code_names = pd.read_csv('./newsBackTest/code_stock_name.csv')

for i in range(0, code_names.shape[0]-1):
  x = code_names['code'][i]
  code = '{0:06d}'.format(int(x))
  name = code_names['name'][i]
  read_df = pd.read_csv('./newsBackTest/'+str(code)+'_'+name+'_주가데이터.tsv', sep='\t')
  read_df['mlp'] = 0
  read_df['mlb'] = 0
  read_df['dlp'] = 0
  read_df['dlb'] = 0
  for ir in range(0, read_df.shape[0]-1):
    read = [read_df['news'][ir]]
    read_df['mlp'][ir], read_df['mlb'][ir] = logiReg.logiRegPredict(read)
    dl_results = tf.sigmoid(reloaded_model(tf.constant(read)))
    read_df['dlp'][ir], read_df['dlb'][ir] = bert_result.calcReuslt(dl_results)
  read_df.to_csv('./newsBackTested/'+str(code)+'_'+name+'_news_tested.tsv', sep='\t')
