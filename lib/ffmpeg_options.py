#!/usr/bin/env python3

amd={      
    'sub': '-map 0:v -map 0:a -map 0:2? -c:v h264_amf -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:2? -c:v hevc_amf -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v h264_amf -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v hevc_amf -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
nvidia={      
    'sub':  '-map 0:v -map 0:a -map 0:2? -c:v h264_nvenc -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:2? -c:v hevc_nvenc -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v h264_nvenc -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v hevc_nvenc -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
default_none={      
    'sub':  '-map 0:v -map 0:a -map 0:2? -c:v libx264 -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:2? -c:v libx265 -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v libx264 -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v libx265 -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
copy_files={      
    'copy':  '-c:v copy -c:a copy' ,
    'copy_sub_hevc':  '-map 0:v -map 0:a -map 0:2? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en'
    }


# FFMPEG_OPTIONS_SPECIAL='-map 0:v -map 0:a -map 0:2? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en'
