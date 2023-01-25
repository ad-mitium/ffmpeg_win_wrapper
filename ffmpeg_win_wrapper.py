#!/usr/bin/env python3
# Authored by Timothy Mui 11/15/2022

import argparse,os,shutil
from pathlib import Path
from time import strftime
from lib import version as ver
from lib import colors
from lib.ffmpeg_options import amd,nvidia,default_none,copy_files,special
from lib.dest_folders import out_dir_dict,out_dir,report_folder,local_folder
from lib.action_description import action_description as act_desc

##############################################################################
#####                                                                    #####
#####               Configurable variables for this script               #####
#####                                                                    #####
##############################################################################


GPU='None'   # For any GPU, change to AMD for AMD GPUs, change to NVIDIA for NVIDIA GPUs

extension='mp4'

stream=2

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
version_number = (0, 0, 8)
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
    
def check_num(num): # Sanity test for input
    limit=10        # Don't dwell on failure forever
    for i in (range(limit, -1, -1)):
        if i > 0:
            try: 
                int(num)
                # print("Valid integer: ", num)
                return num
            except ValueError:
                num=input("Please enter a valid integer: ")
                i=i-1
        else:
            raise SystemExit('Too many failures to enter a valid integer, exiting.')

def hwtest():
    if HW_TEST == None:
        colors.print_blue("Default hardware options to be used")
    elif (HW_TEST[0] == '-'):
        global FFMPEG_HW_OPTIONS
        FFMPEG_HW_OPTIONS=HW_TEST
        colors.print_green_no_cr ("Custom hardware options detected and the options are: \n   ")
        colors.print_yellow(FFMPEG_HW_OPTIONS)
    else:
        test_type='custom ffmepg hardware options'
        colors.print_red_error(test_type)
        colors.print_yellow(HW_TEST)
        exit_on_error()

def opttest(F_OPTIONS,Message):
    if OPT_TEST == None:
        colors.print_green_no_cr(Message)
        colors.print_yellow (F_OPTIONS)
    elif (OPT_TEST[0] == '-'):
        global FFMPEG_OPTIONS
        FFMPEG_OPTIONS=OPT_TEST
        colors.print_green_no_cr ("Custom options detected and the options are: \n   ")
        colors.print_yellow(FFMPEG_OPTIONS)
    else:
        test_type='custom ffmpeg options'
        colors.print_red_error(test_type)
        colors.print_yellow(OPT_TEST)
        exit_on_error()

def test_path(output_folder_path):
    if os.path.exists((output_folder_path)):
        # print(os.path.dirname(output_folder_path))
        # print(output_folder_path," exists")
        pass
    else:
        # print(output_folder_path," does not exist")
        if enabled_copy:
            Path(output_folder_path).mkdir( parents=True, exist_ok=True)

def copy_to_remote():
    if enabled_copy:
        test_path(full_out_path)
        shutil.copy(output_filename_ext, full_out_path)
    colors.print_cyan_no_cr(out_dir_name)
    print("", end =" ")
    colors.print_yellow_no_cr(output_filename_ext)
    print('{} copied to'.format('' if enabled_copy else ' would be'), end =" ")
    colors.print_white(full_out_path)

def action_test():
    #########   Determine transcode action   #########
    global FFMPEG_OPTIONS
    if (action == 'subtrans'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SUB.format(stream=stream,gpu_codec=GPU_type_264)
        Message="Subtitle H.264 option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'subtrans265'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SUB_HEVC.format(stream=stream,gpu_codec=GPU_type_265)
        Message="Subtitle HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'special_sub'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SPECIAL_SUB.format(stream=stream,gpu_codec=GPU_type_265)
        Message="Special subtitle HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'special_copy'): 
        global ext 
        ext = 'mkv'       # This special case breaks MP4 container conventions, save as mkv instead
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SPECIAL_SUB_COPY.format(stream=stream,gpu_codec=GPU_type_265)
        Message="Special HEVC transcode and subtitle copy option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
        colors.print_green_no_cr ('Extension is now set to')
        colors.print_red(ext)
    elif (action == 'special_trans'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_SPECIAL_TRANS.format(gpu_codec=GPU_type_265)
        Message="Special HEVC transcode option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'copy'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_COPY
        Message="Copy option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'copysub'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_COPY_SUB_HEVC.format(stream=stream)
        Message="Copy subtitle HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'trans265'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS_HEVC.format(gpu_codec=GPU_type_265)
        Message="Transcode HEVC option request detected and the options are: \n   "
        opttest(FFMPEG_OPTIONS, Message)
    elif (action == 'transcode'): 
        FFMPEG_OPTIONS=FFMPEG_OPTIONS.format(gpu_codec=GPU_type_264)        
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
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=act_desc['desc']
, 
epilog=act_desc['epi']
 )
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
parser.add_argument('-s','--sub-stream', default=stream, help='''Select subtitle stream, defaults to 2''') 
parser.add_argument('-v','--version', action='version', version='%(prog)s {}'.format(ver.ver_info(version_number)), help='show the version number and exit')
args = parser.parse_args()

action=args.action_command.lower()
input_filename=str(args.input_file)
output_file=args.output_file
output_path=args.dest_folder
ext=args.ext.lower()

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

colors.print_blue('Transcoding...')

colors.print_green_no_cr ('GPU is')
colors.print_red(args.gpu)

# Inelegant stream handling
stream=args.sub_stream

stream=check_num(stream)

colors.print_green_no_cr ('Subtitle stream is')
colors.print_red(stream)

# if not enabled_dict:
#     colors.print_red("Dictionary disabled")   # For debugging

OPT_TEST=args.ffmpeg_option
HW_TEST=args.ffmpeg_hardware

FFMPEG_HW_OPTIONS=""

hwtest()

FFMPEG_OPTIONS_COPY= copy_files ['copy']
FFMPEG_OPTIONS_COPY_SUB_HEVC= copy_files ['copy_sub']
if enabled_GPU in 'amd':
    GPU_type_264='h264_amf'
    GPU_type_265='hevc_amf'
    FFMPEG_OPTIONS_SUB= amd['sub']
    FFMPEG_OPTIONS_SUB_HEVC= amd['sub_hevc']
    FFMPEG_OPTIONS= amd['h264']
    FFMPEG_OPTIONS_HEVC= amd['hevc']
elif enabled_GPU in 'nvidia':
    GPU_type_264='h264_nvenc'
    GPU_type_265='hevc_nvenc'
    FFMPEG_OPTIONS_SUB= nvidia['sub']
    FFMPEG_OPTIONS_SUB_HEVC= nvidia['sub_hevc']
    FFMPEG_OPTIONS= nvidia['h264']
    FFMPEG_OPTIONS_HEVC= nvidia['hevc']
else:
    GPU_type_264='libx264'
    GPU_type_265='libx265'
    FFMPEG_OPTIONS_SUB= default_none['sub']
    FFMPEG_OPTIONS_SUB_HEVC= default_none['sub_hevc']
    FFMPEG_OPTIONS= default_none['h264']
    FFMPEG_OPTIONS_HEVC= default_none['hevc']

FFMPEG_OPTIONS_SPECIAL_SUB=special['special_sub']
FFMPEG_OPTIONS_SPECIAL_SUB_COPY=special['special_copy']
FFMPEG_OPTIONS_SPECIAL_TRANS=special['special_trans']

# print(OPT_TEST)   # For debugging

action_test()   # Check what action user wanted

########   Echo back info provided   ########
#print ('Input filename is', end =" ")
#colors.print_yellow(input_filename)
#print ('Output folder path is', end=" ")
#colors.print_yellow(output_path)
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

colors.print_white_no_cr ('  Input filename is: ')
colors.print_yellow(input_filename)

colors.print_white_no_cr('  New file is named: ')
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
        test_path(full_out_path)
        copy_to_remote()
else:
    colors.print_red("Dictionary disabled")
    for out_dir_path in out_dir:
        out_dir_name=out_dir_path
        # print (out_dir_name)
        # print (out_dir_path)
        full_out_path=joinpath(out_dir_path,output_path)
        test_path(full_out_path)
        copy_to_remote()
# print("\r.")

colors.print_blue("\rCopying completed")

# Print out report filenames
# for name in report_file_names:
#     print(name)

# print (action, input_filename, output_file, stdout_file, output_path)     # For debugging

