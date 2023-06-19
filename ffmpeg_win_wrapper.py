#!/usr/bin/env python3
# Authored by Timothy Mui 11/15/2022

import argparse,os
from pathlib import Path
from time import strftime
from lib import version as ver
from lib import colors
import textwrap 
from config.dest_folders import out_dir_dict,out_dir,report_folder,local_folder,defaults
from lib.action_description import action_description as act_desc
from lib.common_functions import check_num,exit_on_error,joinpath,probetest,test_path,copy_to_remote
from lib.action_test_command import action_test

##############################################################################
#####                                                                    #####
#####          FFMPEG OPTIONS are located in ffmpeg_options.py           #####
#####         Destination folders are located in dest_folder.py          #####
#####             No configurable variables past this point              #####
#####                                                                    #####
##############################################################################


start_time= strftime('%H%M%S')
version_number = (0, 1, 00)
#GPU='AMD'    # Force to AMD GPUs, change to NVIDIA if needed

#########   Useful functions   #########
def hwtest():
    if HW_TEST == None:
        colors.print_blue("Default hardware options to be used")
    elif (HW_TEST[0] == '-'):
        global FFMPEG_HW_OPTIONS
        FFMPEG_HW_OPTIONS=' '+HW_TEST
        colors.print_green_no_cr ("Custom hardware options detected and the options are: \n   ")
        colors.print_yellow(textwrap.fill(text=FFMPEG_HW_OPTIONS, width=defaults['option_wrap_width'], subsequent_indent='        '))
    else:
        test_type='custom ffmepg hardware options'
        colors.print_red_error(test_type)
        colors.print_yellow(textwrap.fill(text=HW_TEST, width=defaults['option_wrap_width'], subsequent_indent='        '))
        exit_on_error()



##############################################################################
##############################################################################
#####                                                                    #####
#####                       Main code begins here                        #####
#####                                                                    #####
##############################################################################
##############################################################################

home_dir=Path.home()    # No need to change this
base_outdir=joinpath(str(home_dir),local_folder)  # Location to save output to before copying
FFMPEG_HW_OPTIONS=""

#########   Command line interaction for user supplied variables   #########
# provide description and version info
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=act_desc['desc']
, 
epilog=act_desc['epi']
 )
parser.add_argument('action_command', help='''Enter action option such as "transcode" for transcode or "copy" for copying to mp4 container. See all actions below.''')
parser.add_argument('input_file', help='''Enter input file name to encode/transcode''')
parser.add_argument('dest_folder', help='''Enter ouput folder path surrounded by \' \' ''')
parser.add_argument('output_file', help='''Enter output file name without extension''')
parser.add_argument('-as','--audio-stream', default=defaults['audio_stream'], help='''Select audio stream, defaults to first stream''') 
parser.add_argument('-c','--check-file', action='store_true',help='''Probe file for encoded information''') 
parser.add_argument('-ddt','--disable-dict', action='store_false',help='''Disable copy to remote folder using dictionary''') 
parser.add_argument('-dlc','--disable-local_dir', action='store_false',help='''Disable local ouput directory, save in current folder''') 
parser.add_argument('-dtc','--tc-disable', action='store_false',help='''Disable transcoding (For debugging)''') 
parser.add_argument('-e','--ext', default=defaults['extension'],help='''Choose extension to convert to, default is 'MP4' ''') 
parser.add_argument('-g','--gpu', default=defaults['GPU'],help='''Choose GPU manufacturer to use, default is 'None' ''') 
parser.add_argument('-hw','--ffmpeg-hardware', help='''Custom ffmpeg hardware options, options must be wrapped in apostrophes (-hw 'options') ''')
parser.add_argument('-nc','--disable-copy-file', action='store_false',help='''Enable copy to remote folder (Output folder path still required)''') 
parser.add_argument('-opt','--ffmpeg-option', help='''Custom ffmpeg options, options must be wrapped in apostrophes (-opt 'options') 
Options should start with a - (see examples below)''') 
parser.add_argument('-r','--encode-rate', default=defaults['encode_rate'],help='''Encode rate, default is 23''') 
parser.add_argument('-rep','--report-file', help='''Enter STDIO report file name (deprecated)''') 
parser.add_argument('-ss','--sub-stream', default=defaults['stream'], help='''Select subtitle stream, defaults to 2''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_number)), help='show the version number and exit')
parser.add_argument('-vs','--video-stream', default=defaults['video_stream'], help='''Select video stream, defaults to 0''') 
args = parser.parse_args()

action=args.action_command.lower()
input_filename=str(args.input_file)
output_file=args.output_file
output_path=args.dest_folder
# extension=args.ext.lower()

if not (args.report_file is None):
    base_report_dir=joinpath(str(home_dir),report_folder)  # Location to place report file
    report_file_name=args.report_file
    stdout_file_name=report_file_name+'.out'
    stdout_file=os.path.join(base_report_dir , stdout_file_name)
    stderr_file_name=report_file_name+'.err'
    stderr_file=os.path.join(base_report_dir , stderr_file_name)
    report_file_names=[stderr_file,stdout_file]
    test_path(base_report_dir)

enabled_copy=args.disable_copy_file
enabled_dict=args.disable_dict
enabled_GPU=args.gpu.lower()
enabled_local_copy=args.disable_local_dir
enabled_transcode=args.tc_disable

test_path(base_outdir,enabled_copy)

PROBE_TEST=args.check_file

# colors.print_red_no_cr("Probe test is")
# colors.print_green(PROBE_TEST)
probetest(input_filename,PROBE_TEST)    # Exits after probing file, does not move forward past this point

colors.print_blue_no_cr('{}'.format('' if PROBE_TEST else 'Transcoding... \n'))

colors.print_green_no_cr ('GPU is')
colors.print_red_no_cr(args.gpu+'  ')

# Custom stream handling
subtitle_stream=check_num(args.sub_stream)
audio_stream=check_num(args.audio_stream)
video_stream=check_num(args.video_stream)

colors.print_green_no_cr ('Video stream is')
colors.print_red_no_cr(video_stream+'  ')
colors.print_green_no_cr ('Audio stream is')
colors.print_red_no_cr(audio_stream+'  ')
colors.print_green_no_cr ('Subtitle stream is')
colors.print_red_no_cr(subtitle_stream+'  ')

# Encode rate handling
rate=check_num(args.encode_rate)

colors.print_green_no_cr ('Encode rate is')
colors.print_red(rate)

# Dictionary use status
# if not enabled_dict:
#     colors.print_red("Dictionary disabled")   # For debugging

OPT_TEST=args.ffmpeg_option
HW_TEST=args.ffmpeg_hardware

hwtest()

# print(OPT_TEST)   # For debugging

# Check action command requested
FFMPEG_OPTIONS, extension = action_test(action,args.gpu.lower(),video_stream,audio_stream,subtitle_stream,args.ext.lower(),rate,OPT_TEST)

########   Echo back info provided   ########
#print ('Input filename is', end =" ")
#colors.print_yellow(input_filename)
#print ('Output folder path is', end=" ")
#colors.print_yellow(output_path)
#print ('Output filename is', end=" ")
if enabled_local_copy:
    output_filename_ext=os.path.join(base_outdir,output_file+'.'+extension)
    #colors.print_red(output_filename_ext)
else:
    output_filename_ext=output_file+'.'+extension
#colors.print_yellow(output_filename_ext)
#print ('GPU is', end=" ")
#colors.print_red(enabled_GPU)


#########   Transcode file   #########
command='ffmpeg -hide_banner' + FFMPEG_HW_OPTIONS +  ' -i '+ '"'+ input_filename +'" '+ FFMPEG_OPTIONS +' "'+ output_filename_ext +'" '
if enabled_transcode:
    os.system(command)
curr_time=strftime('%H%M%S')
colors.print_blue("Transcoding is complete.")

# print ("Command to execute is:", command)
colors.cprint ("Command executed was:\n    ", 'green', attrs=['bold'], end=' ')
colors.print_yellow(textwrap.fill(text=command, width=defaults['display_wrap_width'], subsequent_indent='        '))

colors.print_white_no_cr ('  Input filename is: ')
colors.print_yellow(textwrap.fill(text=input_filename, width=defaults['display_wrap_width'], subsequent_indent='      '))

colors.print_white_no_cr('  New file is named: ')
colors.print_yellow(textwrap.fill(text=output_filename_ext, width=defaults['display_wrap_width'], subsequent_indent='      '))

########   Display transcode usage time   ########
elapsed_time= int(curr_time) - int(start_time)
colors.cprint("Start time: ", 'green', attrs=['bold'], end =" ")
colors.print_yellow_no_cr(start_time)
colors.cprint("  Completed time: ", 'green', attrs=['bold'], end =" ")
colors.print_yellow_no_cr(curr_time)
colors.cprint("  Elasped time: ", 'green', attrs=['bold'], end =" ")
colors.print_yellow(elapsed_time)

########   Copying file to destination   ########
colors.print_blue("Copying files to remote location.\r")

if enabled_dict:
    # colors.print_red("Dictionary in use")
    for out_dir_name, out_dir_path in out_dir_dict.items():
        copy_start_time= strftime('%H%M%S')
        # print (out_dir_name)
        # print (out_dir_path)
        full_out_path=joinpath(out_dir_path,output_path)
        test_path(full_out_path,enabled_copy)
        copy_to_remote(out_dir_name,full_out_path,output_filename_ext,enabled_copy)
        copy_end_time= strftime('%H%M%S')
        copy_elapsed_time= int(copy_end_time) - int(copy_start_time)
        colors.cprint("  Copy time: ", 'green', attrs=['bold'], end =" ")
        colors.print_yellow(copy_elapsed_time)

else:
    colors.print_red("Dictionary disabled")
    for out_dir_path in out_dir:
        copy_start_time= strftime('%H%M%S')
        out_dir_name=out_dir_path
        # print (out_dir_name)
        # print (out_dir_path)
        full_out_path=joinpath(out_dir_path,output_path)
        test_path(full_out_path,enabled_copy)
        copy_to_remote(out_dir_name,full_out_path,output_filename_ext,enabled_copy)
        copy_end_time= strftime('%H%M%S')
        copy_elapsed_time= int(copy_end_time) - int(copy_start_time)
        colors.cprint("  Copy time: ", 'green', attrs=['bold'], end =" ")
        colors.print_yellow(copy_elapsed_time)
# print("\r.")

colors.print_blue("\rCopying completed")

# Print out output file size
if enabled_transcode:   # Don't stat filesize if you didn't transcode the file
    file_size = os.stat(output_filename_ext)
    colors.print_white(f'File size is {file_size.st_size  / (1024 * 1024):,.3f} MB')
    
# Print out report filenames
# for name in report_file_names:
#     print(name)

# print (action, input_filename, output_file, stdout_file, output_path)     # For debugging

