#!/usr/bin/env python3

keyname1='Local Dir'    # Reference key name
out_dir1='M:\Videos'    # Location of output directory to copy output file to
keyname2='Storage  '    # Reference key name
out_dir2='N:\Videos'    # Location of output directory to copy output file to

defaults={
    'GPU':'None',   # For any GPU, change to AMD for AMD GPUs, change to NVIDIA for NVIDIA GPUs
    'encode_rate':'23',     
    'extension':'mp4',
    'audio_stream':'0', # Default audio stream (first stream)
    'stream':'2',   # Default subtitle stream
    'option_wrap_width':100,
    'display_wrap_width':120,
    'filename_wrap_width':80,
    'foldername_wrap_width':80
}

out_dir_dict={     # If addtional output directories are needed, add here
    keyname1:out_dir1,
    keyname2:out_dir2
    }
out_dir=[          # If addtional output directories are needed, add here
    out_dir1,
    out_dir2
    ]

report_folder = 'Documents\Report Folder'    # Location to place report file
local_folder = 'Downloads'    # Location to store ffmpeg output before copying, output willnot be deleted
