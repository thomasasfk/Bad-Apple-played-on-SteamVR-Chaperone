#!/bin/bash

FPS=12
BA_URL=https://youtu.be/FtutLA63Cp8
FRAMES_DIRECTORY=ba
FRAME_PREFIX=badapple

py -m pip install opencv-python Pillow youtube-dl
py -m youtube_dl -f 394 $BA_URL -o bad_apple_original.mp4
ffmpeg -i bad_apple_original.mp4 -filter:v fps=$FPS bad_apple_new.mp4

# remove ba directory if it exists.
if [ -d $FRAMES_DIRECTORY ]; then
    rm -rf $FRAMES_DIRECTORY
fi

py video_to_chaperone.py bad_apple_new.mp4 $FRAMES_DIRECTORY $FRAME_PREFIX 0.05 32 32
cd ba # directory containing bad apple frames.
amt=$(ls | wc -l) # amount bad apple frames.
cd ..
# this was the dir of my build result.
./chaperone_renderer/x64/Debug/chaperone_renderer.exe $amt $FRAMES_DIRECTORY $FRAME_PREFIX
