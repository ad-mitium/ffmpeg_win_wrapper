# FFMPEG for Windows Wrapper

A wrapper for FFMPEG on Windows because I cannot stand the command line interface offered by FFMPEG. There is such a thing as being too complex when you need to use it repeatedly for the same task!  DO, however, ignore the fact that I wrote nearly 500 lines of code to "avoid" this.

Currently defaults to MP4 format for greater compatibility.

I am not an expert on FFMPEG, so please don't ask for help on that front. And while I created this for Windows, it *can* be used on linux if you change the folder location variables in dest_folder.py

## Usage

This script uses FFMPEG to transcode a video from one format to another, whether it be a straight copy from one video container to another (currently MP4), transcode from one format to another, transcode a video with subtitles to another format or transcode a video using customized options provided in the commandline. Once the video is transcoded, it will copy the new video to a pre-specified location(s).

User configurable options exist to tailor its behavior and destination locations.  All user configurable variables are located in the `config` folder.

    dest_folders    contains all options for extension type, GPU type, subtitle stream, destination folders, etc.
    ffmpeg_options  contains all options related to how to encode video files based on action commands

At any point, using the -opt flag will override whatever the default transcode action that was provided.

### **Code execution as follows:**

    python3 ffmpeg_win_wrapper <Action> <Input File> <Destination folder> <Output Filename>

### **Examples:**

Executing

    python3 -g NVidia subtrans input.mkv folder_path "My Video" 
    python3 -hw '-hwaccel d3d11va -hwaccel_device 1 ' transcode input.mkv folder "My Video" 
    python3 copysub265 input.mkv "folder path" "My Video" 
    python3 subtrans -opt '-c:v copy -c:a copy' input.mkv "folder path" "My Video" 

Note that for the last example, ffmpeg will be executed as:

    ffmpeg -i input.mkv -c:v copy -c:a copy "folder path" "My Video.mp4"

And it will not use the default subtitle transcoding options:

    ffmpeg -i input.mkv -map 0:v -map 0:a -map 0:2? -c:v libx264 -preset fast -crf 23 -c:a copy -c:s mov_text -metadata:s:s:0 language=en "folder path" "My Video.mp4"

### **Using flags:**

The following optional flags are:

    -d, --disable-dict          Disable dictionary for mutliple copy locations
    -dlc, --disable-local-dir   Disable local output directory, save in current folder
    -dtc, --tc_disable          Disables transcoding (For debugging)
    -e, --ext                   Choose extension to convert to, default is MP4
    -g, --gpu                   Choose GPU hardware to convert with, default is None
    -hw, --ffmpeg-hardware      Optional hardware related options before input file
    -nc, --disable-copy-file    Disables copying to folder(s)
    -opt, --ffmpeg-option       Override default options for custom options  
    -r, --report-file           Output files copied to file (Deprecated)
    -rate, --encode-rate        Set encode rate, default is 23
    -s, --sub-stream            Select subtitle stream, defaults to 2
    -v, --version               Outputs current version
    
    -h, --help                  Ouputs helpful(maybe?) usage information for this script

### **Available Actions**

Action commands include (use -opt to specify unique options):

    subtrans        Transcode into h.264 format, defaults to 1st sub stream
    transcode       Transcode into h.264 format
    subtrans265     Transcode into h.265 format, defaults to 1st sub stream
    trans265        Transcode into h.265 format
    copy            Straight copy into mp4 container
    copysub         Copy into mp4 container, copies subtitle stream, defaults to 1st sub stream
    special_copy    Transcode into h.265 format with variable quality video, keeps original sub stream format, defaults to 1st sub stream
    special_sub     Transcode into h.265 format with variable quality video, defaults to 1st sub stream
    special_trans   Transcode into h.265 format with variable quality video
  *Note* special_copy defaults to .mkv (hard coded)
  
## Pitfalls to be aware of

* You need to download a Windows compiled version for FFMPEG from ffmpeg.org (I'm using the one linked to gyan.dev)
* At this time, the **script will overwrite** any file with the same name at the output location.  (It is this way by design)
* If you receive an error message regarding a missing output_file, check to see if one of the other required parameters are missing, usually it is the action command or destination folder that is forgotten
* If you are using linux, AMD amf drivers don't exist, use default (None) or modify ffmpeg_options.py to use VAAPI
* When using the command prompt, use double quotes (") to surround text with spaces (or use PowerShell as Microsoft want you to)
  
### Required to use this script *(Aside from Python 3)*

TermColor

* pip install termcolor

## To Do

* Add "special" high quality video settings for intel and nvidia gpus after testing (Hardware needed)
* Add flag to indicate either H.264 or HEVC format transcoding to eliminate multiple options for similar settings (code reduction)
* Add flag to indicate special variable rate transcoding (Partially completed)
* ~~Fix inelegant stream # handling~~
* ~~Add ability to insert stream channel instead of defaulting to first sub stream~~
* Reduce the number of locations to update when adding new actions, currently four locations in three separate files need to be changed
* TBD
