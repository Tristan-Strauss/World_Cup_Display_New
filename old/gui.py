import vlc
import time

media_player = vlc.MediaPlayer("./media/1930.mp4")

media_player.play()

time.sleep(5)