import sys,os
from datetime import datetime

string = sys.argv[1]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_date_time():
    now = datetime.now()
    w=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    #print 'Date and Time: ',dt_string
    #print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
    print(bcolors.WARNING + '\n' + string + bcolors.ENDC)
    print(bcolors.WARNING + dt_string + bcolors.ENDC)

print_date_time()
