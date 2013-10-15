g-tracker-phenny
=================

description:
------------
Modified phenny bot for irc.installgentoo.com. Some modules have been cut out due to abuse and some custom modules (described below) have been added.

pretty sure these are broken now, hopefully one day I can get them fixed.

all credit goes to talib.

dependencies:
-------------
* python
* [phenny](http://inamidst.com/phenny)
* some python libraries I cannot remember...

ftp module:
-----------
* display server uptime
* display free disk space to admin users
* search the ftp server's raw directories and return results to channel
* search 4chan's /rs/ board


(eventually could get away from searching the actual direcories, if we could get the python script that sends the directory listings to mysql, would also be faster)


tracker module:
---------------
(was written for the old tracker (torrent trader))
* search torents
* display top 10 torrents
* display latest torrents
* announce newest user


like I said hopefully one day I can get these fixed =[
