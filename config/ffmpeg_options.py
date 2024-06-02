#!/usr/bin/env python3

gpu_dict = {
    'amd':{      
        'sub': '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}' ,
        'sub_hevc':  '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en  {copy_attach}' ,
        'h264':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -c:a copy {copy_attach}' ,
        'hevc':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy {copy_attach}'
    },
    'nvidia':{      
        'sub':  '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}' ,
        'sub_hevc':  '-map:{vstream} 0:v -map 0:a -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}' ,
        'h264':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -c:a copy {copy_attach}' ,
        'hevc':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy {copy_attach}'
        },
    'default_none':{      
        'sub':  '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}' ,
        'sub_hevc':  '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}' ,
        'h264':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -c:a copy {copy_attach}' ,
        'hevc':  '-c:v:{vstream} {gpu_codec} -preset fast -crf {rate} -vtag hvc1 -c:a copy {copy_attach}'
    }
}
copy_files={      
    'copy':  '-c:v copy -c:a copy -c:s copy -c:t copy' ,
    'copysub':  '-map 0:v:{vstream} -map 0:a:{astream} -map 0:{sstream}? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en {copy_attach}'
    }
special={       # Default ffmpeg presets were adding distracting amounts of pixelation during transcoding, changed to yuv420p from nv12
    'special_sub': '-map 0:v:{vstream} -c:v {gpu_codec} {gpu_special_options} -qmin {rate} -pix_fmt {pix_fmt} -b:v 0K -vtag hvc1 -map 0:a:{astream} -c:a copy -map 0:{sstream}? -c:s mov_text -metadata:s:s:0 language=en {copy_attach}',
    'special_copy': '-map 0:v:{vstream} -c:v {gpu_codec} {gpu_special_options} -qmin {rate} -pix_fmt {pix_fmt} -b:v 0K -vtag hvc1 -map 0:a:{astream} -c:a copy -map 0:{sstream}? -c:s copy {copy_attach}',
    'special_trans': '-map 0:v:{vstream} -c:v {gpu_codec} {gpu_special_options} -qmin {rate} -pix_fmt {pix_fmt} -b:v 0K -vtag hvc1 -map 0:a -c:a copy -map 0:s? -c:s copy {copy_attach}'
}

gpu_special_options={
    'amd':'-rc vbr_latency',
    'nvidia':'-rc vbr',
    # 'nvidia':'-rc vbr_hq',
    'none':''

}

pixel_format={
    'amd':'yuv420p',        # At this time, 10 bit encoding is still unsupported for AMD GPUs
    'nvidia':'p010le',
    'none':'yuv420p'        # Not doing 10 bit without a GPU at this time, sorry no Intel support for QSV at this time due to lack of testing hardware
}

encode_codec_type={         # This snippet of code is not in use. See set_ffmpeg_conditions() in action_test_comamnd.py for actual codec usage
    'h264':{'amd':'h264_amf','nvidia':'h264_nvenc','none':'libx264'},
    'h265':{'amd':'hevc_amf','nvidia':'hevc_nvenc','none':'libx265'},
    '':{''}
}

    # 'special_sub': '-map 0:v -map 0:a -map 0:{stream}? -c:v {gpu_codec} -rc vbr_latency -qmin 26 -pix_fmt yuv420p -b:v 0K -vtag hvc1 -c:a copy -c:s mov_text -metadata:s:s:0 language=en',

# FFMPEG_OPTIONS_SPECIAL='-map 0:v -map 0:a -map 0:{stream}? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en'
