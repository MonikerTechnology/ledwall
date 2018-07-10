
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

def warning(file,*args):
    print(bcolors.WARNING , file ,  " WARNING: " , bcolors.ENDC , end='')
    for i in args:
        print(i,end=' ')
    print()

def info(file,*args):
    print(bcolors.UNDERLINE , file, " INFO:" , bcolors.ENDC , end='') 
    for i in args:
        print(i,end=' ')
    print()
  

def header(file, *args):
    print(bcolors.HEADER , file , " MESSAGE:" , bcolors.ENDC , " " , end='')
    for i in args:
        print(i,end=' ')
    print()
 