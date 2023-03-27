from tiktok import TikTok

def main():
  user = ''
  tiktok = TikTok('path_to_chromedriver')
  df = tiktok.get_videos_ids(user) # arg full=True retorna IDs de todos os vídeos postados
  
  return(print(df.head())) # TODO: retornar algo significativo


if __name__ == '__main__':
  main()