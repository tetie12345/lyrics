import subprocess as s
import os

output = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
song = [k[2:] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("tag artist") or i.startswith("tag title")]]]
time = int([k[-1] for k in [j.split() for j in [i for i in output.split('\n') if i.startswith("duration")]]][0])
print(time)
song = " ".join(song[1] + song[0])
if not os.path.isfile(f"/home/Floris/lyricist/cache/{song}.lrc"):
    s.call(['syncedlyrics', f"{song}", '--synced-only'], stdout=open(os.devnull, "w"))
    os.system(f'mv "{song}.lrc" ~/lyricist/cache/')
with open(f"/home/Floris/lyricist/cache/{song}.lrc", "r") as f:
    lyrics = [i.split() for i in f.read().split('\n')]
timings = [round(float(lyrics[i][0][4:-1]))+int(lyrics[i][0][1:3])*60 for i in range(len(lyrics))]
while 1:
    timing = s.run(['cmus-remote', '-Q'], stdout=s.PIPE).stdout.decode('utf-8')
    currenttime = int([k[-1] for k in [j.split() for j in [i for i in timing.split('\n') if i.startswith("position")]]][0])
    if currenttime in timings:
        print(' '.join(lyrics[timings.index(currenttime)]))
