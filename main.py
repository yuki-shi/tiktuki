#!/usr/bin/python3

from tiktuki import TikTuki
import argparse
import pandas as pd

def main() -> None:
  parser = argparse.ArgumentParser(description='')

  parser.add_argument('--username',
                      '-u',
                      type=str,
                      required=True,
                      help='profile username to be searched')

  parser.add_argument('--full',
                      action='store_true',
                      required=False,
                      help='add argument for full profile scrape')

  args = parser.parse_args()

  user = args.username
  tiktok = TikTuki(user)
  video_data = tiktok.get_video_data(args.full)

  df = pd.DataFrame(video_data)
  df.to_csv('tiktok_data.csv', index=False)

  print('Exported ot .csv!')

  return

if __name__ == '__main__':
    main()
