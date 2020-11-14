import os
from argparse import ArgumentParser
import __main__ as main
from zipfile import ZipFile, BadZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time

start = time()
_logo = """\033[2J\033[H\033[J  ____  _        _____             __  
 /_  / (_)__    / ___/______ _____/ /__
  / /_/ / _ \  / /__/ __/ _ `/ __/  '_/
 /___/_/ .__/  \___/_/  \_,_/\__/_/\_\ 
      /_/
"""
_banner = _logo+"""Zip file Cracker with brute force the password
Author : RandsX@22XploiterCrew
E-Mail : dev@22xploitercrew.my.id
"""

def openlist(listname):
    file_list = []
    try:
        file = open(listname, 'r')
        file = file.readlines()
        for line in file:
            file_list.append(line.replace("\n", ""))
        return file_list
    except FileNotFoundError:
        print("Error")
        
def completed(file, password):
    global start, _banner
    print(_banner)
    duration = time() - start
    duration = round(duration) % 60
    print("Successfully cracked zip file with time \"{} seconds\"".format(duration))
    print('='*50)
    print("File     :", os.path.basename(file.filename))
    print("Password :", password)
    print('='*50)
    os._exit(0)
        
def crackZip(fileZip, password):
    password = bytes(password, "utf-8")
    try:
        fileZip.extractall(pwd=password)
        completed(fileZip, password.decode("utf-8"))
    except:
        return "Bad password : " + password.decode("utf-8")
        
print(_banner)
parser = ArgumentParser(
        prog=os.path.basename(main.__file__),
        usage="python3 %(prog)s filepath -W/--wordlist [-v VERBOSE]"
    )
parser.add_argument("file", type=str, help="the location of your \"zip\" file")
parser.add_argument("-v", "--verbose", action="store_true", help="show the cracking process")
parser.add_argument("-W", "--wordlist", metavar="", help="your wordlist passwords", required=True)
args = parser.parse_args()

try:
    zip = ZipFile(args.file)
    processed = []
    wordlist = openlist(args.wordlist)
    with ThreadPoolExecutor() as executor:
        for password in wordlist:
            processed.append(executor.submit(crackZip, zip, password))
        for process in as_completed(processed):
            if args.verbose:
                print(process.result())
            else:
                print("\rPlease Wait . . .", flush=True, end='')
    
except BadZipFile:
    print("[ERROR] \"{}\" Bad Zip File".format(args.file))
except FileNotFoundError as err:
    print("[ERROR] file \"{}\" not exists in {}".format(os.path.basename(args.file), os.path.dirname(args.file)))
except Exception as error:
    print(error)
