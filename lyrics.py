#! /usr/bin/env python
import subprocess as s
import threading as t
from time import sleep
import os, textwrap

try:
    import syncedlyrics as sy
except ImportError:
    os.system("pip install syncedlyrics")

def getsong():
    output = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
    songraw = [k[2:] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
    time = int([k[-1] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("position")]]][0])
    return songraw, time

def waitfornextsong():
    song = getsong()[0]
    previousSong = song
    while song == previousSong:
        previoussong = song
        song = getsong()[0]
    return

def start():
    songraw = getsong()[0]
    song = " ".join(songraw[1] + songraw[0])
    try:
        if not os.path.isfile(f"/home/Floris/.cache/lyricist/{song}.lrc"):
            sy.search(song, synced_only=True, save_path=f"{song}.lrc", providers=["NetEase", "Lrclib", "Megalobiz"])
            os.system(f'mv "{song}.lrc" ~/.cache/lyricist/')
        with open(f"/home/Floris/.cache/lyricist/{song}.lrc", "r") as f:
            lyrics = [i.split() for i in f.read().split('\n')][:-1]
    except Exception as e:
        currentsong = getsong()[0]
        currentsong = " ".join(currentsong[1] + currentsong[0])
        if currentsong != song: return
        print(f'could not find any lyrics for "{song}"')
        waitfornextsong()
        return
    timings = [round(float(lyrics[i][0][4:-1]))+int(lyrics[i][0][1:3])*60 for i in range(len(lyrics))]
    timings.append(timings[-1]+8)
    lyrics.append("a")
    previoussong = songraw
    while 1:
        previoussong = songraw
        songraw, currenttime = getsong()
        if currenttime in timings:
            os.system("clear")
            print(textwrap.fill(' '.join(lyrics[timings.index(currenttime)][1:]),40), end='\r')
            print("\n")
            if len(lyrics) > timings.index(currenttime)+1:
                print(textwrap.fill(' '.join(lyrics[timings.index(currenttime)+1][1:]),40), end='\r')
            sleep(1.2)
        if songraw != previoussong: return
print('\033[?25l', end="")
while 1: os.system("clear"); start()
