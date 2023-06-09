<body>
  <div align="center">
    <img src="https://github.com/yuki-shi/tiktuki/blob/main/assets/catto.gif">
    <h1>tiktuki ~ public data TikTok scraper</h1>
    <p>get public engagement metrics from videos of any TikTok profile</p>
  </div>
  <h2>:robot:  use cases</h2>
  <p>diagnosis of profile health and overall post engagement. can be used on multiple profiles for analysis and benchmarking.<br>
    the 4 public engagement metrics avaible on TikTok are <i>likes</i>, <i>comments</i>, <i>saved</i> and <i>shares</i></p>
  <h2>:steam_locomotive: usage</h2>
  <h3>setup</h3>
  <p>set your virtual environment then install the requirements</p>
  
```bash
$ pip install -r requirements.txt
```
  
  <h3>run</h3>
  
```bash
$ python3 main.py -u {username}
```

  <p>where <i>{username}</i> is the profile to be scraped, without @.<br>by default the script should return the last 30 videos posted by the user<br>you may also add the <i>--full</i> argument for full profile scrape.</p>
  <h3>expcted result</h3>
  <p>a .csv file on the project's root directory<br>it can be read as a Pandas DataFrame:</p>
  <img src="https://github.com/yuki-shi/tiktuki/blob/main/assets/Captura%20de%20tela%20de%202023-07-05%2010-37-24.png">
  <h2>:crab: todo</h2>
  <ul>
    <li>normalize csv headers</li>
    <li>fix <i>--full</i> argument, since the infinite scroll script isn't working as intended</li>
  </ul>
  <h2>:jack_o_lantern: technology</h2>
  <p>python.</p>
</body>
