#!/usr/bin/env python3

action_description={
"desc" : f"""
Python script that wraps ffmpeg command to transcode a video file with a given file name into mp4 format. 

  Usage: ffmeg_win.py [action] [-opt='options'] <input file> <destination folder> <output filename> [report filename]   
  Examples: python3 ffmpeg_win.py transcode abc.mkv 'videos folder' abc -r report 
            python3 ffmpeg_win.py subtrans abc.mkv 'videos folder' abc 
            python3 ffmpeg_win.py transcode -opt '-map 0:v -map 0:a -map 0:2? -c:v hevc_amf -c:a copy -c:s mov_text -metadata:s:s:0 language=en' abc.mkv 'videos folder' abc   """ 
, 

"epi" : f"""    Action commands include (use -opt to specify unique options):
        subtrans        Transcode into h.264 format, defaults to 1st sub stream
        subtrans265     Transcode into h.265 format, defaults to 1st sub stream
        special_sub     Transcode into h.265 format, defaults to 1st sub stream, high quality video
        copy            Straight copy into mp4 container
        copysub265      Copy into mp4 container while transcoding to h.265 format, defaults to 1st sub stream
        special_copy    Transcode into h.265 format, defaults to 1st sub stream, high quality video, keeps original sub stream format
        special_trans   Transcode into h.265 format,  high quality video 
        trans265        Transcode into h.265 format 
        transcode       Transcode into h.264 format 
      *Note* special_copy defaults to .mkv (hard coded)
 """ 
 }
