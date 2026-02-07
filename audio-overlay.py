"""



ffmpeg -i trickshot.mp4 -c:v copy -an flipshot.mp4  

ffmpeg -y -i flipshot.mp4 -i trickshot-voice.mp3 \    
-filter_complex "[0:v]tpad=stop_mode=clone:stop_duration=999[v]" \
-map "[v]" -map 1:a:0 \
-shortest \
-c:v libx264 -c:a aac \
trickshot_output.mp4

ffmpeg -y -i trickshot_output.mp4 -i crowd-noises.mp3 \
-filter_complex "\
[1:a]afade=t=in:st=0:d=1,volume=0.25[a1]; \
[0:a][a1]amix=inputs=2:duration=longest[a] \
" \
-map 0:v -map "[a]" 
-c:v copy -c:a aac -shortest \
full-trickshot.mp4


"""