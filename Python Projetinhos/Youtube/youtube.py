from pytube import Playlist, YouTube
import os

playlist = Playlist("") #Coloque dentro entre as aspas o link da playlist ou vídeo do youtube

for video in playlist:
    try:
        youtube = YouTube(video)
        video = youtube.streams.filter(only_audio=True).first()
        downloaded_file = video.download()
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.mp3'
        os.rename(downloaded_file, new_file)
    except:
        continue
    
print("FIM ...")
