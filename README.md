# Lyricist

a simple tool for displaying lyrics synced to the cmus player.

## disclaimers

1. Lyricist was built for my personal use, and may not fit within your setup.
2. Lyricist currently only works with the cmus music player.
3. Lyricist I do **not** make the lyrics for these songs, they are sourced from other places by an external library. if it is fucked up, or it does not exist, **i can't fix it**.

## installation

installation should be quite simple, clone this repository:

```
git clone https://tetie12345/lyricist.git
cd lyricist
```

from there, running the program with python should work.

`python lyrics.py`

the program may attempt to install any missing packages that it needs, and will start after finishing

### adding to path

if you want to add lyricist to your path
> why the fuck would you want this in your path but sure
simply make the file executable, and put it in your path

```
sudo chmod +x lyrics.py
ln -s lyrics.py /usr/bin/lyricist
```

from there you should restart your terminal session, and you should be good to go
