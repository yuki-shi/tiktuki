#!usr/bin/python3

from tiktuki import TikTuki
import argparse

def main():
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
  df = tiktok.get_video_data(args.full)
  return # TODO: retornar algo significativo


if __name__ == '__main__':
  main()
