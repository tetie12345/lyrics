import subprocess as s
import threading as t
from time import sleep
import os

def waitfornextsong():
    output = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
    song = [k[2:] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
    previousSong = song
    while song == previousSong:
        previoussong = song
        output = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
        song = [k[2:] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
    return

def start():
    output = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
    songraw = [k[2:] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
    time = int([k[-1] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("duration")]]][0])
    song = " ".join(songraw[1] + songraw[0])
    try:
        if not os.path.isfile(f"/home/Floris/.cache/lyricist/{song}.lrc"):
            s.call(['syncedlyrics', f"{song}", '--synced-only'], stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
            os.system(f'mv "{song}.lrc" ~/.cache/lyricist/')
        with open(f"/home/Floris/.cache/lyricist/{song}.lrc", "r") as f:
            lyrics = [i.split() for i in f.read().split('\n')]
    except:
        os.system("clear")
        print(f'could not find any lyrics for "{song}"')
        waitfornextsong()
        return
    timings = [round(float(lyrics[i][0][4:-1]))+int(lyrics[i][0][1:3])*60 for i in range(len(lyrics))]
    previoussong = songraw
    while 1:
        previoussong = songraw
        info = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
        currenttime = int([k[-1] for k in [j.split() for j in [i for i in info.split('\n') if i.startswith("position")]]][0])
        songraw = [k[2:] for k in [j.split() for j in [i for i in info.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
        if currenttime in timings: print(' '.join(lyrics[timings.index(currenttime)][1:]))
        if songraw != previoussong: return

while 1:
    os.system("clear")
    start()
