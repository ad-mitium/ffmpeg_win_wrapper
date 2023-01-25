#!/usr/bin/env python3

amd={      
    'sub': '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v {gpu_codec} -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
nvidia={      
    'sub':  '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v {gpu_codec} -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
default_none={      
    'sub':  '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'sub_hevc':  '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en' ,
    'h264':  '-c:v {gpu_codec} -preset fast -crf 23 -c:a copy' ,
    'hevc':  '-c:v {gpu_codec} -preset fast -crf 23 -vtag hvc1 -c:a copy'
    }
copy_files={      
    'copy':  '-c:v copy -c:a copy -c:s copy' ,
    'copy_sub':  '-map 0:v -map 0:a -map 0:{stream}? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en'
    }
special={       # Default ffmpeg presets were adding distracting amounts of pixelation during transcoding, changed to yuv420p from nv12
    'special_sub': '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -rc vbr_latency -qmin 26 -pix_fmt yuv420p -b:v 0K -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en',
    'special_copy': '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -rc vbr_latency -qmin 26 -pix_fmt yuv420p -b:v 0K -vtag hvc1 -c:a copy -c:s copy',
    'special_trans': '-map 0:v -map 0:a -c:v {gpu_codec} -rc vbr_latency -qmin 26 -pix_fmt yuv420p -b:v 0K -vtag hvc1 -c:a copy '
}



# FFMPEG_OPTIONS_SPECIAL='-map 0:v -map 0:a -map 0:{stream}? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en'
