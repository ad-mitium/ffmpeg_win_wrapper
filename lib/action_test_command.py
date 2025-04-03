#!/usr/bin/env python3

import textwrap

def opttest(F_OPTIONS,Message,Custom_Options):
    if Custom_Options == None:
        colors.print_green_no_cr(Message)
        colors.print_yellow (textwrap.fill(text=F_OPTIONS, width=defaults['option_wrap_width'], subsequent_indent='        '))
    elif (Custom_Options[0] == '-'):
        global FFMPEG_OPTIONS
        FFMPEG_OPTIONS=Custom_Options
        colors.print_green_no_cr ("Custom options detected and the options are: \n   ")
        colors.print_yellow(textwrap.fill(text=FFMPEG_OPTIONS, width=defaults['option_wrap_width'], subsequent_indent='        '))
    else:
        test_type='custom ffmpeg options'
        colors.print_red_error(test_type)
        colors.print_yellow(textwrap.fill(text=Custom_Options, width=defaults['option_wrap_width'], subsequent_indent='        '))
        exit_on_error()

def action_test(action, GPU_brand, vid_stream, aud_stream, sub_stream, extension, enc_rate, cust_options, append_attach):

    FFMPEG_SET_OPTIONS, encode_format, gpu_options = set_ffmpeg_conditions(action, GPU_brand)
    # print(encode_format)

    #########   Determine transcode action   #########
    colors.print_white_no_cr(action+":")
    if (action == 'special_copy'): 
        extension = 'mkv'       # This special case breaks MP4 container conventions, save as mkv instead
        FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
            vstream=vid_stream,pix_fmt=pixel_format[GPU_brand],astream=aud_stream,sstream=sub_stream,rate=enc_rate,gpu_codec=encode_format,gpu_special_options=gpu_options,copy_attach=append_attach)
        Message="Special HEVC transcode and subtitle copy option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message, cust_options)
    else:
        if (action == 'special_sub'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,pix_fmt=pixel_format[GPU_brand],astream=aud_stream,sstream=sub_stream,rate=enc_rate,gpu_codec=encode_format,gpu_special_options=gpu_options,copy_attach=append_attach)
            Message="Special subtitle HEVC option request detected and the options are: \n   "
        elif (action == 'special_trans'): 
            extension = 'mkv'       # This special case breaks MP4 container conventions, save as mkv instead
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,pix_fmt=pixel_format[GPU_brand],astream=aud_stream,rate=enc_rate,gpu_codec=encode_format,gpu_special_options=gpu_options,copy_attach=append_attach)
            Message="Special HEVC transcode option request detected and the options are: \n   "
        elif (action == 'copy'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(copy_attach=append_attach)
            Message="Copy option request detected and the options are: \n   "
        elif (action == 'copysub'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,astream=aud_stream,sstream=sub_stream,copy_attach=append_attach)
            Message="Copy subtitle HEVC option request detected and the options are: \n   "
        elif (action == 'subtrans'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,astream=aud_stream,sstream=sub_stream,rate=enc_rate,gpu_codec=encode_format,copy_attach=append_attach)
            Message="Subtitle H.264 option request detected and the options are: \n   "
        elif (action == 'subtrans265'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,astream=aud_stream,sstream=sub_stream,rate=enc_rate,gpu_codec=encode_format,copy_attach=append_attach)
            Message="Subtitle HEVC option request detected and the options are: \n   "
        elif (action == 'trans265'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,rate=enc_rate,gpu_codec=encode_format,copy_attach=append_attach)
            Message="Transcode HEVC option request detected and the options are: \n   "
        elif (action == 'transcode'): 
            FFMPEG_OPTIONS=FFMPEG_SET_OPTIONS.format(
                vstream=vid_stream,rate=enc_rate,gpu_codec=encode_format,copy_attach=append_attach)        
            Message="Transcode H.264 option request detected and the options are: \n   "

        else:
            raise SystemExit("No action command offered or invalid action command!  Exiting.")
        opttest(FFMPEG_OPTIONS, Message, cust_options)
    
    # Diagnostic dialogue to display action specific changes
    if (action == 'special_copy') or (action == 'special_trans'):
        colors.print_green_no_cr ('Extension is now set to')
        colors.print_red(extension) 
    else:
        colors.print_green_no_cr ('Extension is set to')
        colors.print_red(extension) 
    # Diagnostic dialog to display GPU specific changes
    if (GPU_brand == 'nvidia') and (action in ('special_copy','special_sub','special_trans')) :
        colors.print_green_no_cr ('Pixel format is set to')
        colors.print_red(pixel_format[GPU_brand])
    elif (action in ('special_copy','special_sub','special_trans')):
        colors.print_green_no_cr ('Pixel format is set to')
        colors.print_red(pixel_format[GPU_brand])
    return(FFMPEG_OPTIONS,extension)

def set_ffmpeg_conditions(action_command,GPU_brand):
    encode_type='libx264'

    # Configure FFMPEG Options before processing action command
    if (GPU_brand in 'amd'):
        gpu_options=gpu_special_options['amd']
        gpu_key= 'amd'
    elif GPU_brand in 'nvidia':
        gpu_options=gpu_special_options['nvidia']
        gpu_key= 'nvidia'
    else:
        gpu_options=gpu_special_options['none']
        gpu_key= 'default_none'
    
    if (action_command in ('transcode','subtrans')):
        encode_type='libx264'
        if (action_command == 'transcode'):
            F_OPTIONS=gpu_dict[gpu_key]['h264']
        else:
            F_OPTIONS=gpu_dict[gpu_key]['sub']

    elif (action_command in ('trans265','subtrans265')):
        encode_type='libx265'
        if (action_command == 'trans265'):
            F_OPTIONS=gpu_dict[gpu_key]['hevc']
        else:
            F_OPTIONS=gpu_dict[gpu_key]['sub_hevc']

    elif (action_command in ('copy','copysub')):
        F_OPTIONS=copy_files[action_command]

    elif (action_command in ('special_copy','special_sub','special_trans')):
        if GPU_brand == 'amd':
            encode_type = 'hevc_amf'
        elif GPU_brand == 'nvidia':
            encode_type = 'hevc_nvenc'
        else:
            encode_type = 'libx265'
        F_OPTIONS=special[action_command]
    else:
        F_OPTIONS='Invalid options'    # If none of the action commands are given, send malformed options message
    # print (action_command,F_OPTIONS)  # Diagnostics

    return(F_OPTIONS,encode_type,gpu_options)

def get_multi_sub(Custom_Options):
    subs=[]
    for i in Custom_Options:
        subs.append(i)
        # print (i)
    if Custom_Options == None:
        colors.print_green_no_cr("No Custom Options")
        colors.print_yellow (textwrap.fill(text=type(subs), width=defaults['option_wrap_width'], subsequent_indent='        '))
    elif "-" and "," in Custom_Options:
        global FFMPEG_OPTIONS
        colors.print_green_no_cr ("'-' and ',' detected, splitting to individual streams: \n   ")
        colors.print_yellow(textwrap.fill(text=str(subs), width=defaults['option_wrap_width'], subsequent_indent='        '))
    elif "-" in Custom_Options:
        global FFMPEG_OPTIONS
        colors.print_green_no_cr ("'-' detected, splitting to individual streams: \n   ")
        colors.print_yellow(textwrap.fill(text=str(subs), width=defaults['option_wrap_width'], subsequent_indent='        '))
    elif "," in Custom_Options:
        global FFMPEG_OPTIONS
        colors.print_green_no_cr ("',' detected, appending individual streams: \n   ")
        colors.print_yellow(textwrap.fill(text=str(subs), width=defaults['option_wrap_width'], subsequent_indent='        '))
    else:
        test_type='custom ffmpeg options'
        # colors.print_red_error(test_type)
        colors.print_yellow(textwrap.fill(text=test_type+"Input: "+Custom_Options, width=defaults['option_wrap_width'], subsequent_indent='        '))
        # exit_on_error()

    # print (subs)
    return (subs)

if (__name__ == '__main__'):
    import sys
    from pathlib import Path
    import colors
    # sys.path.append(str(Path().absolute())+'/'+'config')   # allows for finding ffmpeg_options.py
    from ..config.ffmpeg_options import gpu_dict,copy_files,special,gpu_special_options,pixel_format,encode_codec_type
    from ..config.dest_folders import defaults

    def exit_on_error():    # Circular import of colors.py when pulling in common_functions.py
        answer = input("Continue with default options? [y/N]  ").lower()
        if answer == 'y':
            print("Continuing with default options")
        else:
            print("Exiting.")
            raise SystemExit(0)

    # multi_subs = "1-4"
    # multi_subs = "1,2,4"
    multi_subs = "1-4,6"

    sub_results = get_multi_sub(multi_subs)
    # print(f'In: [{multi_subs}]  Out: [{sub_results}]')

    append_attach = '-map 0:t? -c:t copy'
    video_stream=0
    audio_stream=0
    subtitle_stream=2
    encode_rate=23
    extension='mp4'
    OPT_TEST=None

    enabled_gpu=input("Please enter GPU type ('amd','nvidia'): ")
    if enabled_gpu not in ('amd','nvidia'):
        enabled_gpu = 'none'
    print('Invalid GPU type, defaulting to',end=' ')
    colors.print_red(enabled_gpu)
    action_command=input("Please enter an action command ('special_copy','special_sub','special_trans','copy','copysub','subtrans','subtrans265','transcode','trans265'): ")
    # print(action_command)
    if action_command not in ('special_copy','special_sub','special_trans','copy','copysub','subtrans','subtrans265','transcode','trans265'):
        action_command == ''

    conditions, encode_format, gpu_options=set_ffmpeg_conditions(action_command, enabled_gpu)
    print('From set ffmpeg conditions: ',encode_format,conditions,gpu_options)

    options, extension = action_test(action_command, enabled_gpu, video_stream, audio_stream, subtitle_stream, extension, encode_rate, OPT_TEST,append_attach)
    # print(f'[{options}] [{extension}]')
    
else:
    import lib.colors as colors
    from config.ffmpeg_options import gpu_dict,copy_files,special,gpu_special_options,pixel_format,encode_codec_type
    from lib.common_functions import exit_on_error
    from config.dest_folders import defaults
