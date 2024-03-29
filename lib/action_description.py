#!/usr/bin/env python3

action_description={
"desc" : f"""
Python script that wraps ffmpeg command to transcode a video file with a given file name into mp4 format. 

  Usage: ffmeg_win.py [action] [-opt='options'] <input file> <destination folder> <output filename> [report filename]   
  Examples: python3 ffmpeg_win.py transcode abc.mkv 'videos folder' abc -rep report 
            python3 ffmpeg_win.py subtrans abc.mkv 'videos folder' abc 
            python3 ffmpeg_win.py transcode -opt '-map 0:v -map 0:a -map 0:2? -c:v hevc_amf -c:a copy -c:s mov_text -metadata:s:s:0 language=en' abc.mkv 'videos folder' abc   """ 
, 

"epi" : f"""    Action commands include (use -opt to specify unique options):
        subtrans        Transcode into h.264 format, defaults to 1st sub stream
        transcode       Transcode into h.264 format 
        subtrans265     Transcode into h.265 format, defaults to 1st sub stream
        trans265        Transcode into h.265 format 
        copy            Straight copy into mp4 container
        copysub         Copy into mp4 container, copies sub stream, defaults to 1st sub stream
        special_copy    Transcode into h.265 format with variable quality video, keeps original sub stream format, defaults to 1st sub stream
        special_sub     Transcode into h.265 format with variable quality video, defaults to 1st sub stream
        special_trans   Transcode into h.265 format with variable quality video 
      *Note* Both special_copy and special_trans default to .mkv (hard coded)
 """ 
 }
