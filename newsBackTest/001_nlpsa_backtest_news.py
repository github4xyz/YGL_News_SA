
from pykrx import stock
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import urllib
import pickle

import warnings
warnings.filterwarnings('ignore')

def naver_news_title(stock, date):
  result_list = []
  error_cnt = 0

  stock_encode = urllib.parse.quote(stock, encoding='euc-kr')
  date = date.strftime('%Y-%m-%d')

  base_url = 'https://finance.naver.com/news/news_search.nhn?rcdate=1&q={}&sm=title.basic&pd=4&stDateStart={}&stDateEnd={}'
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

  url = base_url.format(stock_encode, date, date)
  res = requests.get(url, headers=headers)


  if res.status_code == 200:
    soup = BeautifulSoup(res.text, "lxml")
    title_list = soup.select('.articleSubject')
    for title in title_list:
      try:
        news_title = title.select_one('a').text.strip()
        result_list.append(news_title)
      except:
        error_cnt += 1
  
  return result_list, url

df = stock.get_market_cap_by_ticker(datetime.date.today().strftime('%Y%m%d'))
df_top = df.sort_values('시가총액', ascending=False).head(10) # 10
code_lists = df_top.index.tolist()

stock_name_lists = []
for ticker in code_lists:
    stock_name_lists.append(stock.get_market_ticker_name(ticker))

code_names = dict(zip(code_lists, stock_name_lists))
df_code_names = pd.DataFrame(list(code_names.items()), columns = ['code','name'])
df_code_names.to_csv('./news/code_stock_name.csv')

# with open('./news/code_stock_name.pkl', 'wb') as f:
#     pickle.dump(code_names, f)

# with open('./temp/code_stock_name.pkl', 'rb') as f:
#     code_names = pickle.load(f)

fail_count = 0
ok_count = 0

# start = "20180701" 
# end = "20210716" 
start = "20210101" 
end = "20210716" 

for code in code_lists:
  try:
    result = stock.get_market_ohlcv_by_date(start, end, code)
    ok_count += 1
  except:
    print ("Could not read data for " + code)
    fail_count += 1

  print(str(ok_count) + " loads, " + str(fail_count) + " failures")                               

  result['UpDown'] = 0
  for i in range(0, result.shape[0]-1):
      if result['종가'][i] < result['종가'][i+1]:
          result['UpDown'][i] = 1
      else:
          result['UpDown'][i] = 0
  
  stock_name = code_names.get(code)
  result['news'] = ""
  if not result.empty:
    for i in range(0, result.shape[0]):
        news, _ = naver_news_title(stock_name, result.index[i])
        result['news'][i] = news

  result.to_csv('./news/'+code+'_'+stock_name+'_news.tsv', sep='\t')

