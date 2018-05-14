
import logging
import os





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def warning(file,message):
    print(bcolors.WARNING + file +  " WARNING: " + bcolors.ENDC + message)

def info(file,message):
    print(bcolors.UNDERLINE + file + " INFO:" + bcolors.ENDC + " " + message)

def header(file, message):
    print(bcolors.HEADER + file + " MESSAGE:" + bcolors.ENDC + " " + message)

 