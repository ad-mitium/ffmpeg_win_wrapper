#!/usr/bin/env python3
from termcolor import colored, cprint

def print_black(text):
    cprint( text, 'black', attrs=['bold'])

def print_green_no_cr(text):
    cprint( text, 'black', attrs=['bold'], end=" ")

def print_blue(text):
    cprint( text, 'blue', attrs=['bold'])

def print_blue_no_cr(text):
    cprint( text, 'blue', attrs=['bold'], end=" ")

def print_cyan(text):
    cprint( text, 'cyan', attrs=['bold'])

def print_cyan_no_cr(text):
    cprint( text, 'cyan', attrs=['bold'], end=" ")

def print_green(text):
    cprint( text, 'green', attrs=['bold'])

def print_green_no_cr(text):
    cprint( text, 'green', attrs=['bold'], end=" ")

def print_magenta(text):
    cprint( text, 'magenta', attrs=['bold'])

def print_magenta_no_cr(text):
    cprint( text, 'magenta', attrs=['bold'], end=" ")

def print_red_error(msg_string):
    text="Uh oh. Logic error in "+str(msg_string)
    cprint( text, 'red', 'on_cyan', attrs=['bold','blink'])
    
def print_red(text):
    cprint( text, 'red', attrs=['bold'])

def print_red_no_cr(text):
    cprint( text, 'red', attrs=['bold'], end=" ")

def print_white(text):
    cprint( text, 'white', attrs=['bold'])

def print_white_no_cr(text):
    cprint( text, 'white', attrs=['bold'], end=" ")

def print_yellow(text):
    cprint( text, 'yellow', attrs=['bold'])

def print_yellow_no_cr(text):
    cprint( text, 'yellow', attrs=['bold'], end ="")

def print_orange(text):     # Appears to be orangish in the terminal, ymmv
    cprint( text, 'yellow')

def print_orange_no_cr(text):     # Appears to be orangish in the terminal, ymmv
    cprint( text, 'yellow', end ="")
