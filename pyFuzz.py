#imports

from pydoc import replace
from time import sleep
import requests
import argparse
from colorama import Fore, Style

#version

print("pyFuzz v0.1 alpha")

#arguments

parser = argparse.ArgumentParser(description="Python tool for fuzzing")

parser.add_argument('-u', '--url', type=str, help='Url avec * pour signifier l endroit a fuzzer', required=True)
parser.add_argument('-n', '--numbers', type=str, help='la range de nombre séparé par un -', required=False)
parser.add_argument('-w', '--wordlist', type=str, help='le chemin de la wordlist', required=False)

args = parser.parse_args()

#error functions and requirements
def error():
    print("program aborted")

if not args.numbers and not args.wordlist :
    print("choose a wordlist or a digit range !")
    error()

if args.numbers and args.wordlist :
    print("choose of the two !")
    error()
    
if args.numbers:
    if len(args.numbers.split("-")) != 2:
        print("choose a range of two numbers !")
        error()

#variables

results = []

#fuzzing with wordlist part

def wordlist_fuzzing(url, wordlist):
    global results
    with open(wordlist, "r") as f:
        print("fuzzing start")
        sleep(1)
        for line in f:
            line = line.strip()
            req = url.replace("*", line)
            r = requests.get(req)
            if r.status_code == 200:
                print(Fore.GREEN + "[+] url valid : " + Style.RESET_ALL + req)
                results.append(req)
            else:
                print(Fore.RED + "[-] url invalid (", r.status_code,") : " + Style.RESET_ALL + req)
    print(Fore.MAGENTA + "\n" + "fuzzing end, results : " +results.__str__() + "\n" + Style.RESET_ALL)
    
#fuzzing with number range

def number_fuzzing():
    global results
    range_numbers = args.numbers.split("-")
    print("fuzzing start")
    sleep(1)
    for i in range(int(range_numbers[0]), int(range_numbers[1])+1):
        content = str(i)
        content = content.strip()
        req = args.url.replace("*", content)
        r = requests.get(req)
        if r.status_code == 200:
            print(Fore.GREEN + "[+] url valid : " + Style.RESET_ALL + req)
            results.append(req)
        else:
            print(Fore.RED + "[-] url invalid (", r.status_code,") : " + Style.RESET_ALL + req)
    print(Fore.MAGENTA + "\n" + "fuzzing end, results : " +results.__str__() + "\n" + Style.RESET_ALL)
    
        
#mains functions

def main():
    if args.wordlist :
        wordlist_fuzzing(args.url, args.wordlist)
    if args.numbers :
        number_fuzzing()
        

if __name__ == "__main__":
    main()