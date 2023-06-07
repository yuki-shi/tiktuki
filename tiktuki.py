import json
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
import datetime as dt
from time import sleep
import sys
import os.path
import pandas as pd
from typing import List, Dict, Tuple
from tqdm import tqdm


class TikTuki():
  def __init__(self, username: str):
    self.driver = self.init_driver()
    self.username = username

  def init_driver(self) -> webdriver.Chrome:
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

  def scrape_page_source(self, html: str) -> Tuple[List[str], List[str]]:
    soup = BeautifulSoup(html, 'html.parser')

    videos_id = []
    videos_title = []

    for anchor in soup.find_all('a', href=True):
      if anchor.has_attr('title'):
        videos_title.append(anchor['title'])
      videos_id.append(re.findall(r'.((?<=\/video\/).*)',anchor['href']))
    
    return videos_id, videos_title

  def get_video_ids(self, full: bool) -> Dict[str, str]:
    browser = self.driver
    browser.get(f'https://www.tiktok.com/@{self.username}')
    print(f"Scraping {self.username}'s profile")
    
    # For a full profile scrape
    if full == True:
      # O feed do TikTok possui scroll infinito, ao que foi proposta a seguinte solução
      # que tomo aplicada aqui:
      #https://github.com/KuanWeiBeCool/Choose-best-Sephora-Make-up-Products-With-A-Limited-Budget/blob/55d474f9441d0b6a1b71a44e5267b386b66b292b/Web%20Scrapping%20For%20Infinite%20Scrolling%20Websites%20Using%20Selenium.ipynb
      screen_height = browser.execute_script('return window.screen.height;')
      counter = 0

      while True:
        browser.execute_script(f'window.scrollTo(0, {screen_height * counter});')
        scroll_height = browser.execute_script('return document.body.scrollHeight;')
        sleep(3)
        counter += 1

        if (screen_height * counter) > scroll_height:
          break

      html = browser.page_source
      with open('yuki.html', 'w') as f:
          f.write(html)
      
    # For a parcial scrape (default)
    else:
      html = browser.page_source
      
    browser.quit() 
    videos_id, videos_title = self.scrape_page_source(html)

    videos_id = list(filter(None, videos_id))
    videos_id = [item for sublist in videos_id for item in sublist]

    videos_dict ={key: value for key, value in zip(videos_id, videos_title)}

    # Exit program if no videos were found
    if len(videos_dict) == 0:
      sys.exit('Empty or non-existent profile')
     
    print(f'Got {len(videos_dict)} videos')
    return videos_dict 

  def get_post_metrics(self, video_ids: List[str]) -> Dict[str, int] :
    for id in tqdm(video_ids):
      url = f'https://www.tiktok.com/@{self.username}/video/{id}'
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')

      post_data = {}
      metrics = soup.find_all('strong', attrs={'data-e2e': True})

      post_data['url'] = url

      try:
        post_data['desc'] = soup.find_all('span', attrs={'class': 'tiktok-j2a19r-SpanText efbd9f0'})[0].text
        
        for metric in metrics:
          post_data[metric['data-e2e']] = metric.text

      except:
        for key in ['like-count', 'comment-count', 'undefined-count', 'share-count']:
            post_data[key] = 0
        post_data['desc'] = 'Video not found'

      yield post_data
    
  def get_video_data(self, full: bool) -> List[Dict[str, int]]:
    video_ids = self.get_video_ids(full)
    post_metrics = self.get_post_metrics(video_ids.values())
    output_list = []

    for i in post_metrics:
      output_list.append(i) 

    return output_list
