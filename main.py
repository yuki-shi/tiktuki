#!usr/bin/python3

from tiktok import TikTok
import argparse

def main():
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--username',
                      '-u',
                      type=str,
                      required=True)
  args = parser.parse_args()

  user = args.username
  tiktok = TikTok(user)
  df = tiktok.get_video_data() # arg full=True retorna IDs de todos os vídeos postados
 # print(df.head())

  return # TODO: retornar algo significativo


if __name__ == '__main__':
  main()
