# Music Splitter

When I found a nice on Youitube I  want to play in in my car by a USB stick.  
I can download the mp3 file from you Tube.   
I can then copy it on a USB stick and use in the car.  
The problem is that it is a single file and you cannot move around, not easily.  
The single original file must be splitted in parts of fixed duration.  
The resulting mp3 files must have the Artist and Title and Album set in mp3 metadata,
so that the application of the car can recognize it and act accordingly (put it togheter and play it in the right order).

Other time I have a FLAC file I need to convert to mp3.  
In some cases I have the .mp3u file that contains the right parts of the full file, sometimes not.  

## Setup
This program uses the _mp3splt_ library.  
It has to be downloaded and unzipped into the /libs folder.
For example, current version is 2.6.2 and I downloaded and unzipped the Windows version.   
I have now _/libs/mp3splt_2.6.2_i386_ folder, and it contains the _mp3splt.exe_ file.  
Correct the _main.py_ file with the right folder name matching your downloaded version.  

## Extract mp3 from YouTube video
Using this websites I can extract the mp3:
- https://youtubemp3free.com/en

Some of them are limited in duration or does not work properly sometines.

## Split FLAC files


This **mp3splt library** can be used: https://mp3splt.sourceforge.net/mp3splt_page/home.php
> split by a fixed time length

I put the Windows .exe in the _libs/mp3splt_2.6.2_i386_ folder.

```python
import os

mp3splt_path = "./libs/mp3splt_2.6.2_i386/mp3splt.exe"
mp3_filename = "my-file.mp3"

os.system(f"{mp3splt_path} {mp3_filename}")
```

Where the fuck is the documentation?



## CUE file

.cue file example:
```
PERFORMER "Various Artists"
TITLE "Ambient Lounge  - Vol. 5 - CD 1"
FILE "Ambient Lounge - Vol. 5 - CD 1.mp3" MP3
  TRACK 01 AUDIO
    TITLE "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    PERFORMER "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Groove Armada - Lovebox"
    PERFORMER "Groove Armada - Lovebox"
    INDEX 01 05:24:10
  TRACK 03 AUDIO
    TITLE "4 Hero - Hold it down"
    PERFORMER "4 Hero - Hold it down"
    INDEX 01 11:01:01
```
