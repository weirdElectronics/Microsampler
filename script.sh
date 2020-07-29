#!/bin/sh
inotifywait -m -e close_write waveform.wav |
    while read -r audio _; do
	ffmpeg -i $audio -filter_complex \
	       "[0:a]aformat=channel_layouts=mono,\
 	       showwavespic=s=128x64:colors=white[fg];\
 	       color=s=128x64:color=black[bg];\
 	       [bg][fg]overlay,\
	       drawbox=x=(iw-w)/2:y=(ih-h)/2:w=iw:h=1:color=white"\
	       -frames:v 1 -y output.png
    done

