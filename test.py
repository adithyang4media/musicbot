import YouTube from pytube
url="https://www.youtube.com/watch?v=8FAUEv_E_xQ"
yt = YouTube(url)
t = yt.streams.filter(only_audio=True)
t[0].download(./)
print("done")
