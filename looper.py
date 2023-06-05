import spotipy
import time
import threading
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk

client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8000"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-modify-playback-state user-read-playback-state"))


def get_seconds(time_str):
    minutes, seconds = time_str.split(":")
    total_seconds = int(minutes) * 60 + int(seconds)
    return total_seconds


class SongLooper(threading.Thread):
    def __init__(self, start_time_str, end_time_str):
        threading.Thread.__init__(self)
        self.start_time_str = start_time_str
        self.end_time_str = end_time_str
        self.running = False

    def run(self):
        start_time = get_seconds(self.start_time_str)
        end_time = get_seconds(self.end_time_str)
        start_time_ms = start_time * 1000
        self.running = True
        while self.running:
            sp.seek_track(start_time_ms)
            time.sleep((end_time - start_time))

    def stop(self):
        self.running = False


looper = None


def loop_song():
    global looper
    if looper and looper.is_alive():
        looper.stop()
        looper.join()

    start_time_str = start_time_entry.get()
    end_time_str = end_time_entry.get()

    looper = SongLooper(start_time_str, end_time_str)
    looper.start()


def stop_song():
    global looper
    if looper and looper.is_alive():
        looper.stop()
        looper.join()


window = tk.Tk()
window.title("Loop Song")
window.geometry("400x200")
start_time_label = tk.Label(window, text="Start Time (in the format MM:SS): ")
start_time_entry = tk.Entry(window)
end_time_label = tk.Label(window, text="End Time (in the format MM:SS): ")
end_time_entry = tk.Entry(window)
loop_button = tk.Button(window, text="Loop Song", command=loop_song)
stop_button = tk.Button(window, text="Stop Loop", command=stop_song)
start_time_label.pack()
start_time_entry.pack()
end_time_label.pack()
end_time_entry.pack()
loop_button.pack()
stop_button.pack()
window.mainloop()
