import json
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
import datetime as dt
import time
import sys
import os.path
import pandas as pd


class TikTok():
  def __init__(self, username: str):
    self.driver = self.init_driver()
    self.username = username

  def init_driver(self):
    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("window-size=1400,600")
    options.add_argument("--incognito")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
    options.add_argument(f'user-agent={user_agent}')

    return webdriver.Chrome(options=options)

  @staticmethod
  def format_to_dataframe(response):
    video = response['itemList'][0]

    video_data = video['stats']
    video_data.update(dict({'desc': video['desc'],
                            'date': video['createTime'],
                            'id': video['id']}))

    df = pd.DataFrame(video_data.items()).transpose()
    header = df.iloc[0]
    df.columns = header
    df.drop(df.index[0], inplace=True)
    
    df['date'] = df['date'].astype(int)
    df['date_f'] = [(dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d')) for x in df['date']]

    return df

  def get_video_ids(self, full):
    browser = self.driver
    browser.get(f'https://www.tiktok.com/@{self.username}')
    print('Connected!')
    
    if full == True:
      # O feed do TikTok possui scroll infinito, ao que foi proposta a seguinte solução
      # que tomo aplicada aqui:
      #https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget/blob/55d474f9441d0b6a1b71a44e5267b386b66b292b/Web%20Scrapping%20For%20Infinite%20Scrolling%20Websites%20Using%20Selenium.ipynb
      screen_height = browser.execute_script('return window.screen.height;')
      counter = 0

      while True:
        browser.execute_script(f'window.scrollTo(0, {screen_height * counter});')
        time.sleep(1)
        scroll_height = browser.execute_script('return document.body.scrollHeight;')
        counter += 1

        if (screen_height * counter) > scroll_height:
          break

      html = browser.page_source
      print('Got page source!')
      soup = BeautifulSoup(html, 'html.parser')

      browser.quit()

      videos_id = []
      videos_title = []

      for anchor in soup.find_all('a', href=True):
        if anchor.has_attr('title'):
          videos_title.append(anchor['title'])
        videos_id.append(re.findall(r'.((?<=\/video\/).*)',anchor['href']))

      videos_id = list(filter(None, videos_id))
      videos_id = [item for sublist in videos_id for item in sublist]

      videos_tuple = list(zip(videos_id, videos_title))
      return pd.DataFrame(videos_tuple, columns=['id', 'title'])

    else:
      html = browser.page_source
      soup = BeautifulSoup(html, 'html.parser')

      videos_id = []
      videos_title = []

      for anchor in soup.find_all('a', href=True):
        if anchor.has_attr('title'):
          videos_title.append(anchor['title'])
        videos_id.append(re.findall(r'.((?<=\/video\/).*)',anchor['href']))

      videos_id = list(filter(None, videos_id))
      videos_id = [item for sublist in videos_id for item in sublist]

      videos_tuple = list(zip(videos_id, videos_title))

      # Exit program if no videos were found
      if len(videos_tuple) == 0:
        sys.exit('Empty or non-existent profile')

      return pd.DataFrame(videos_tuple, columns=['id', 'title'])

  def get_video_data(self, full=False):
    video_ids = self.get_video_ids(full)
    browser = self.init_driver()
    dfs = []

    for id in video_ids['id'].head(1):
      print(id)
      browser.get(f'https://www.tiktok.com/{self.username}/video/{id}')
      time.sleep(5)
      logs = browser.get_log('performance')

      for entry in logs:
        message = json.loads(entry['message'])
        message = message['message']
        method = message['method']

        if method == 'Network.requestWillBeSentExtraInfo':
          headers = message['params']['headers']
          if headers.get(':path') is not None and headers.get(':path').startswith('/api/recommend'):
            try:
              body = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['params']['requestId']})
            except exceptions.WebDriverException:
              return ('Body vazio!!')

            response = json.loads(body['body'])
            df = self.format_to_dataframe(response)
            dfs.append(df)

    return pd.concat(dfs, axis=0)
