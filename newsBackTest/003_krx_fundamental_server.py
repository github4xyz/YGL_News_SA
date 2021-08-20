#######################################################
# there is JSON error in api.py of PYKRX
# this would not run 

from operator import concat
import os
from pykrx import stock
import pandas as pd
import datetime
import time

import warnings
warnings.filterwarnings('ignore')


code_names = pd.read_csv('./newsBackTest/code_stock_name.csv')
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
  fundametal.to_csv('./fundamentals/'+today+'-'+str(code)+'_'+name+'_fundamental.tsv', sep='\t')

#############################################################################################
# Error message
#############################################################################################
# Traceback (most recent call last):
#   File "003_krx_fundamental_server.py", line 23, in <module>
#     read_df_date = stock.get_market_fundamental_by_date(today, today, code)
#   File "/home/ubuntu4xyz/.local/lib/python3.8/site-packages/pykrx/stock/api.py", line 431, in get_market_fundamental_by_date
#     df = krx.get_market_fundamental_by_date(fromdate, todate, ticker)
#   File "/home/ubuntu4xyz/.local/lib/python3.8/site-packages/pykrx/website/comm/util.py", line 7, in wrapper
#     return func(*args, **kwargs)
#   File "/home/ubuntu4xyz/.local/lib/python3.8/site-packages/pykrx/website/krx/market/wrap.py", line 210, in get_market_fundamental_by_date
#     df = PER_PBR_배당수익률_개별().fetch(fromdate, todate, "ALL", isin)
#   File "/home/ubuntu4xyz/.local/lib/python3.8/site-packages/pykrx/website/krx/market/core.py", line 164, in fetch
#     result = self.read(mktId=mktId, strtDd=strtDd, endDd=endDd, isuCd=isuCd)
#   File "/home/ubuntu4xyz/.local/lib/python3.8/site-packages/pykrx/website/krx/krxio.py", line 10, in read
#     return resp.json()
#   File "/home/youngwoo/anaconda3/lib/python3.8/site-packages/requests/models.py", line 900, in json
#     return complexjson.loads(self.text, **kwargs)
#   File "/home/youngwoo/anaconda3/lib/python3.8/json/__init__.py", line 357, in loads
#     return _default_decoder.decode(s)
#   File "/home/youngwoo/anaconda3/lib/python3.8/json/decoder.py", line 337, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#   File "/home/youngwoo/anaconda3/lib/python3.8/json/decoder.py", line 355, in raw_decode
#     raise JSONDecodeError("Expecting value", s, err.value) from None
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
