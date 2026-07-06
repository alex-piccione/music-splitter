# Music Splitter

This is an utily to split large MP3 music files in smaller ones.  

When I find a nice compilation on YouTube and I download it, it is a single long mp3 file without separation between the songs.  
The single original file must be splitted in parts of fixed duration.  
The resulting mp3 files must have the Artist, Album and song Title set in the mp3 metadata,
so that the car MP3 player system can recognize it and act accordingly (put it together and play it in the right order).
  
Other times I have a FLAC file I need to convert to mp3.  
In some cases I have the .mp3u file that contains the right parts of the full file, sometimes not.  


## Setup
This program uses the [mp3splt](https://mp3splt.sourceforge.net/mp3splt_page/home.php) library.  
[TODO] Can I distribute it wit h the software?  
[TODO] Can it be auto-configured (download + unzip + setup)?  
It has to be downloaded and unzipped into the **/libs** folder.
The current version is 2.6.2; I downloaded and unzipped the Windows version.  
I have now _/libs/mp3splt_2.6.2_i386_ folder, and it contains the _mp3splt.exe_ file.  
Correct the _main.py_ file with the right folder name matching your downloaded version.  

## Extract mp3 from YouTube video
Using this websites I can extract the mp3:
- https://youtubemp3free.com/en
- https://sern.info/youtu.be



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
