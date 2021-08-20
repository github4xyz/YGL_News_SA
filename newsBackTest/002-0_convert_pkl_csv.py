

import pandas as pd
import pickle


with open('./newsBackTest/code_stock_name.tsv', 'rb') as f:
    code_names = pickle.load(f)

df_code_names = pd.DataFrame(list(code_names.items()), columns = ['code','name'])
df_code_names.to_csv('./newsBackTest/code_stock_name.csv')




# with open('./news/code_stock_name.pkl', 'wb') as f:
#     pickle.dump(code_names, f)

# with open('./temp/code_stock_name.pkl', 'rb') as f:
#     code_names = pickle.load(f)

# 파일 저장
# result.to_csv('./temp/'+code+'_'+stock_name+'_주가데이터.tsv', sep='\t')
# df_code_names = pd.read_csv('./newsBackTest/code_stock_name.csv')



