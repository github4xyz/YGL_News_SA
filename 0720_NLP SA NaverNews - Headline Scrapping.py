
import pandas_datareader as wb
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt
import urllib
from pykrx import stock



# today's 시가총액 Top 50 code lists
df = stock.get_market_cap_by_ticker(datetime.date.today().strftime('%Y%m%d'))
df_t50 = df.sort_values('시가총액', ascending=False).head(300) # 50
code_lists = df_t50.index.tolist()
# code_lists



# today's 시가총액 Top 50 code lists covert to stock name lists
stock_name_lists = []
for ticker in code_lists:
    stock_name_lists.append(stock.get_market_ticker_name(ticker))
# stock_lists



# Build name code index
code_names = dict(zip(code_lists, stock_name_lists))
# code_names



# 주가데이터 with next day price up and down indicator
fail_count = 0
ok_count = 0

start = "20180701" 
end = "20210716" 

for code in code_lists:
  try:
    result = stock.get_market_ohlcv_by_date(start, end, code)
    print ("Read data for " + code + " " + repr(result.shape))
    ok_count += 1
  except:
    print ("Could not read data for " + code)
    fail_count += 1

  print(str(ok_count) + " loads, " + str(fail_count) + " failures")                               # 결측치 제거

  # 새로운 칼럼 생성
  # (Price : 당일 대비 다음날 주가가 상승했으면 1, 하락했으면 0 표시)
  result['UpDown'] = 0
  for i in range(0, result.shape[0]-1):
      if result['종가'][i] < result['종가'][i+1]:
          result['UpDown'][i] = 1
      else:
          result['UpDown'][i] = 0

  # 파일 저장
  result.to_csv(code+'_주가데이터.csv')


# Read 주가데이터 per stock code and returns each day's up or down
def get_upDownDays(code):
  df_down = []
  df_up = []

  price_data = pd.read_csv(code+'_주가데이터.csv')

  df_down = price_data[price_data['UpDown']==0]['날짜']   
  df_up = price_data[price_data['UpDown']==1]['날짜']

  return df_up, df_down

#
def naver_news_title(stock, dates):
  result_list = []
  error_cnt = 0

  stock_name = code_names.get(stock)
  stock_encode = urllib.parse.quote(stock_name, encoding='euc-kr')


  base_url = 'https://finance.naver.com/news/news_search.nhn?rcdate=1&q={}&sm=title.basic&pd=4&stDateStart={}&stDateEnd={}'
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

  for date in dates:
    url = base_url.format(stock_encode, date, date)
    res = requests.get(url, headers=headers)

    # print("page: ", page)
    if res.status_code == 200:
      soup = BeautifulSoup(res.text)
      title_list = soup.select('.articleSubject')
      for title in title_list:
        try:
          news_title = title.select_one('a').text.strip()
          news_title = news_title.replace(stock_name, '')
          # print("add: ", news_title)
          result_list.append([news_title])
        except:
          error_cnt += 1
  
  return result_list


#
headline_count = pd.DataFrame(columns=['code', 'name', 'counts'])

for code in code_lists:
  date_up, date_down = get_upDownDays(code)

  result_list = naver_news_title(code, date_up)
  title_df_up = pd.DataFrame(result_list, columns=['뉴스제목'])
  title_df_up['주가변동'] = 1

  result_list = naver_news_title(code, date_down)
  title_df_down = pd.DataFrame(result_list, columns=['뉴스제목'])
  title_df_down['주가변동'] = 0

  title_df = pd.concat([title_df_up, title_df_down])
  title_df.to_csv(code+'_뉴스타이틀.tsv', index=False, encoding='utf-8', sep="\t")

  stock_name = code_names.get(code)
  new_row = {'code':code, 'name':stock_name, 'counts':title_df.shape[0]}
  headline_count = headline_count.append(new_row, ignore_index=True) 
headline_count.to_csv('news_headline_counts.csv')
# headline_count



# headline_count = pd.DataFrame(columns=['code', 'name', 'counts'])
# count = 1
# for code in code_lists:
#     stock_name = code_names.get(code)
#     new_row = {'code':code, 'name':stock_name, 'counts':count}
#     headline_count = headline_count.append(new_row, ignore_index=True) 
#     count += 1
# headline_count.to_csv('news_headline_counts.csv')
# headline_count

#
all_headlines = pd.DataFrame()

for code in code_lists:
  title_df = pd.read_csv(code+'_뉴스타이틀.tsv', sep="\t")
  all_headlines = pd.concat([all_headlines, title_df])

# shuffle the DataFrame rows
all_headlines = all_headlines.sample(frac = 1)
all_headlines.to_csv('all_headlines.tsv', index=False, encoding='utf-8', sep="\t")

