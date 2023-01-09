#!/usr/bin/env python3
# Authored by Timothy Mui 11/15/2022

import argparse,os,shutil
from pathlib import Path
from time import strftime
from lib import version as ver
from lib import colors
from lib.ffmpeg_options import amd,nvidia,default_none,copy_files,special
from lib.dest_folders import out_dir_dict,out_dir,report_folder,local_folder

##############################################################################
#####                                                                    #####
#####               Configurable variables for this script               #####
#####                                                                    #####
##############################################################################


GPU='None'   # For any GPU, change to AMD for AMD GPUs, change to NVIDIA for NVIDIA GPUs

extension='mp4'

##############################################################################
#####                                                                    #####
#####           End of configurable variables for this script            #####
#####                                                                    #####
#####          FFMPEG OPTIONS are located in ffmpeg_options.py           #####
#####         Destination folders are located in dest_folder.py          #####
#####             No configurable variables past this point              #####
#####                                                                    #####
##############################################################################


start_time= strftime('%H%M%S')
version_number = (0, 0, 2)
#GPU='AMD'    # Force to AMD GPUs, change to NVIDIA if needed

#########   Useful functions   #########
def joinpath(rootdir, targetdir):
    return os.path.join(os.sep, rootdir + os.sep, targetdir)

def exit_on_error():
        answer = input("Continue with default options? [y/N]  ").lower()
        if answer == 'y':
            print("Continuing with default options")
        else:
            print("Exiting.")
            raise SystemExit(0)
    
def hwtest():
    if HW_TEST == None:
        colors.print_blue("Default hardware options to be used")
    elif (HW_TEST[0] == '-'):
        global FFMPEG_HW_OPTIONS
        FFMPEG_HW_OPTIONS=HW_TEST
        colors.print_blue_no_cr ("Custom hardware options detected and the options are: \n   ")
        colors.print_green(FFMPEG_HW_OPTIONS)
    else:
        test_type='custom ffmepg hardware options'
        colors.print_red_error(test_type)
        colors.print_yellow(HW_TEST)
        exit_on_error()

def opttest(F_OPTIONS,Message):
    if OPT_TEST == None:
        colors.print_blue_no_cr(Message)
        colors.print_yellow (F_OPTIONS)
    elif (OPT_TEST[0] == '-'):
        global FFMPEG_OPTIONS
        FFMPEG_OPTIONS=OPT_TEST
        colors.print_blue_no_cr ("Custom options detected and the options are: \n   ")
        colors.print_green(FFMPEG_OPTIONS)
    else:
        test_type='custom ffmpeg options'
        colors.print_red_error(test_type)
        colors.print_yellow(OPT_TEST)
        exit_on_error()

def test_path(output_folder_path):
    if os.path.exists(os.path.dirname(output_folder_path)):
        # print(os.path.dirname(output_folder_path))
        pass
    else:
        Path(output_folder_path).mkdir( parents=True, exist_ok=True)

def copy_to_remote():
    if enabled_copy:
        test_path(full_out_path)
        shutil.copy(output_filename_ext, full_out_path)
    colors.print_cyan_no_cr(out_dir_name)
    print("", end =" ")
    colors.print_yellow_no_cr(output_filename_ext)
    print('{} copied to'.format('' if enabled_copy else ' would be'), end =" ")
    colors.print_yellow(full_out_path)

def action_test():
    #########   Determine transcode action   #########
    global FFMPEG_OPTIONS
    if (action == 'subtrans'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SUB
        Message="Subtitle option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'subtrans265'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SUB_HEVC
        Message="Subtitle HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'special_sub'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SPECIAL_SUB
        Message="Special subtitle transcode option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'special_trans'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SPECIAL_TRANS
        Message="Special transcode option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'copy'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_COPY
        Message="Copy option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'copysub265'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_COPY_SUB_HEVC
        Message="Copy subtitle HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'trans265'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_HEVC
        Message="Transcode HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'transcode'): 
        Message="Transcode H.264 option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
            
    else:
        raise SystemExit("No action option offered!  Exiting.")




##############################################################################
##############################################################################
#####                                                                    #####
#####                       Main code begins here                        #####
#####                                                                    #####
##############################################################################
##############################################################################

home_dir=Path.home()    # No need to change this
base_dir=joinpath(str(home_dir),report_folder)  # Location to place report file
base_outdir=joinpath(str(home_dir),local_folder)  # Location to save output to before copying

test_path(base_dir)
test_path(base_outdir)

#########   Command line interaction for user supplied variables   #########
# provide description and version info
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
Python script that wraps ffmpeg command to transcode a video file with a given file name into mp4 format. 

  Usage: ffmeg_win.py [action] [-opt='options'] <input file> <destination folder> <output filename> [report filename]   
  Examples: python3 ffmpeg_win.py transcode abc.mkv 'videos folder' abc report 
            python3 ffmpeg_win.py subtrans abc.mkv 'videos folder' abc report
            python3 ffmpeg_win.py transcode -opt '-map 0:v -map 0:a -map 0:2? -c:v hevc_amf -c:a copy -c:s mov_text -metadata:s:s:0 language=en' abc.mkv 'videos folder' abc report   ''', 
epilog='''    Action commands include (use -opt to specify unique options):
        subtrans        Transcode into h.264 format, defaults to 1st sub stream
        subtrans265     Transcode into h.265 format, defaults to 1st sub stream
        special_sub     Transcode into h.265 format, defaults to 1st sub stream, high quality video
        copy            Straight copy into mp4 container
        copysub265      Copy into mp4 container while transcoding to h.265 format, defaults to 1st sub stream
        special_trans   Transcode into h.265 format,  high quality video 
        trans265        Transcode into h.265 format 
        transcode       Transcode into h.264 format 
 ''')
parser.add_argument('action_command', help='''Enter action option such as "transcode" for transcode or "copy" for copying to mp4 container. See all actions below.''')
parser.add_argument('input_file', help='''Enter input file name to encode/transcode''')
parser.add_argument('dest_folder', help='''Enter ouput folder path surrounded by \' \' ''')
parser.add_argument('output_file', help='''Enter output file name without extension''')
parser.add_argument('-d','--disable-dict', action='store_false',help='''Disable copy to remote folder using dictionary''') 
parser.add_argument('-dlc','--disable-local_dir', action='store_false',help='''Disable local ouput directory, save in current folder''') 
parser.add_argument('-dtc','--tc-disable', action='store_false',help='''Disable transcoding (For debugging)''') 
parser.add_argument('-e','--ext', default=extension,help='''Choose extension to convert to, default is 'MP4' ''') 
parser.add_argument('-g','--gpu', default=GPU,help='''Choose GPU manufacturer to use, default is 'None' ''') 
parser.add_argument('-hw','--ffmpeg-hardware', help='''Custom ffmpeg hardware options, options must be wrapped in apostrophes (-hw 'options') ''')
parser.add_argument('-nc','--disable-copy-file', action='store_false',help='''Enable copy to remote folder (Output folder path still required)''') 
parser.add_argument('-opt','--ffmpeg-option', help='''Custom ffmpeg options, options must be wrapped in apostrophes (-opt 'options') 
Options should start with a - (see examples below)''') 
parser.add_argument('-r','--report-file', help='''Enter STDIO report file name (deprecated)''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_number)), help='show the version number and exit')
args = parser.parse_args()

action=args.action_command.lower()
input_filename=str(args.input_file)
output_file=args.output_file
output_path=args.dest_folder
ext=args.ext

if not (args.report_file is None):
    report_file_name=args.report_file
    stdout_file_name=report_file_name+'.out'
    stdout_file=os.path.join(base_dir , stdout_file_name)
    stderr_file_name=report_file_name+'.err'
    stderr_file=os.path.join(base_dir , stderr_file_name)
    report_file_names=[stderr_file,stdout_file]

enabled_copy=args.disable_copy_file
enabled_dict=args.disable_dict
enabled_GPU=args.gpu.lower()
enabled_local_copy=args.disable_local_dir
enabled_transcode=args.tc_disable

print ('GPU is', end=" ")
colors.print_red(args.gpu)

# if not enabled_dict:
#     colors.print_red("Dictionary disabled")   # For debugging

OPT_TEST=args.ffmpeg_option
HW_TEST=args.ffmpeg_hardware

FFMPEG_HW_OPTIONS=""

test_path(output_path)
hwtest()

FFMPEG_OPTIONS_COPY= copy_files ['copy']
FFMPEG_OPTIONS_COPY_SUB_HEVC= copy_files ['copy_sub_hevc']
if enabled_GPU in 'amd':
    FFMPEG_OPTIONS_SUB= amd['sub']
    FFMPEG_OPTIONS_SUB_HEVC= amd['sub_hevc']
    FFMPEG_OPTIONS= amd['h264']
    FFMPEG_OPTIONS_HEVC= amd['hevc']
elif enabled_GPU in 'nvidia':
    FFMPEG_OPTIONS_SUB= nvidia['sub']
    FFMPEG_OPTIONS_SUB_HEVC= nvidia['sub_hevc']
    FFMPEG_OPTIONS= nvidia['h264']
    FFMPEG_OPTIONS_HEVC= nvidia['hevc']
else:
    FFMPEG_OPTIONS_SUB= default_none['sub']
    FFMPEG_OPTIONS_SUB_HEVC= default_none['sub_hevc']
    FFMPEG_OPTIONS= default_none['h264']
    FFMPEG_OPTIONS_HEVC= default_none['hevc']

# FFMPEG_OPTIONS_SPECIAL="-map 0:v -map 0:a -map 0:2? -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=en"
FFMPEG_OPTIONS_SPECIAL_SUB=special['special_sub']
FFMPEG_OPTIONS_SPECIAL_TRANS=special['special_trans']

# print(OPT_TEST)   # For debugging

action_test()   # Check what action user wanted

########   Echo back info provided   ########
#print ('Input filename is', end =" ")
#colors.print_yellow(input_filename)
#print ('Output filename is', end=" ")
if enabled_local_copy:
    output_filename_ext=os.path.join(base_outdir,output_file+'.'+ext)
    #colors.print_red(output_filename_ext)
else:
    output_filename_ext=output_file+'.'+ext
#colors.print_yellow(output_filename_ext)
#print ('GPU is', end=" ")
#colors.print_red(enabled_GPU)


#########   Transcode file   #########
command='ffmpeg -hide_banner ' + FFMPEG_HW_OPTIONS +  ' -i '+ '"'+ input_filename +'" '+ FFMPEG_OPTIONS +' "'+ output_filename_ext +'" '
if enabled_transcode:
    os.system(command)
curr_time=strftime('%H%M%S')
colors.print_blue("Transcoding is complete.")

# print ("Command to execute is:", command)
colors.cprint ("Command executed was:\n    ", 'green', attrs=['bold'], end=' ')
colors.print_yellow(command)

print ('  Input filename is: ', end =" ")
colors.print_yellow(input_filename)

print('  New file is named: ', end=" ")
colors.print_yellow(output_filename_ext)

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
        # print (out_dir_name)
        # print (out_dir_path)
        full_out_path=joinpath(out_dir_path,output_path)
        copy_to_remote()
else:
    colors.print_red("Dictionary disabled")
    for out_dir_path in out_dir:
        out_dir_name=out_dir_path
        # print (out_dir_name)
        # print (out_dir_path)
        full_out_path=joinpath(out_dir_path,output_path)
        copy_to_remote()
# print("\r.")

colors.print_blue("\rCopying completed")

# Print out report filenames
# for name in report_file_names:
#     print(name)

# print (action, input_filename, output_file, stdout_file, output_path)     # For debugging

