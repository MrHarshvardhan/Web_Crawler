# Import modules
from multiprocessing import Manager
import os
import sys
import argparse
import requests
import warnings
import urllib.parse
import socket
import multiprocessing

warnings.filterwarnings("ignore")

# Animation banner
github_banner = """
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░▒▓████████▓▒░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓██████▓▒░        ░▒▓████████▓▒░▒▓███████▓▒░░▒▓████████▓▒░ ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░         ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░         ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
                                                                                                                                               
                                                                                                               V: 1.0.0
                                          :=+**##%%%%#*+=:.                               
                                       -*%@@@@@@@@@@@@@@@@%#+.                            
                                     =#@@@@@@@@@@@@@@@@@@@@@@%#=                          
                                   .#@@@@@@@@@@@@@@@@@@@@@@@@@@@%*:.::-======-:.          
                                  .%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*-       
                                  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%-     
                  .:-==++++++=-: :%@@@@@@@@%#+=--+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*    
             :=+#%@@@@@@@@@@@@@% -@@@@@@@@@%%%%%%+.+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*   
          -*%@@@@@@@@@@@@@@@@@@%:.%@@@@@@@@@@@@@@@=:%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-  
       .+%@@@@@@@@@@@@@@@@@@@@@@#.-%@@@@@@@@@@@@%+.#@@@@@@@@@@@@%#+----=*%@@@@@@@@@@@@@*  
     .*%@@@@@@@@@@@@@@@@@@@@@@@@@%=:=*%%@@@@%%#+:-%@@@@@@@@@@@@*.:*%%%%#--@@@@@@@@@@@@@%  
    :%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*+--------=*%@@@@@@@@@@@@@* -%@@@@@@%%@@@@@@@@@@@@@%  
   :%@%#+=--=+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%..%@@@@@@@@@@@@@@@@@@@@@@+  
   +=:         -%@@@@@@@@@@@%%#***#%@@@@@@@@@@@@@@@@@@@@@@@@@% :@@@@@@@@@@@@@@@@@@@@@@#   
                .%@@@@@@@%*-.:=+++=-:-#@@@@@@@@@@@@@@@@@@@@@@%- #@@@@@@@@@@@@@@@@@@@@*    
                 +@@@@@@#..*%@@@@@@@%#:-%@@@@@@@@@@@@@@@@@@@@@%:.#@@@@@@@@@@@@@@@@@#-     
                 :%@@@@# =%@@@@@@@@@@@% *@@@@@@@@@@@@@@@@@@@@@@%+.-#%@@@@@@@@@@@%*:       
                  *@@@@- %@@@@@@@@@@@@% *@@@@@@@@@@@@@@@@@@@@@@@@%+-:-=+***++=-.          
                   *@@@= %@@@@@@@@%@%#.-%@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+:                
                    :=** *@@@@@@@@%*--*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:                
                          *@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@+                 
                           :*%@@@@@@@@@@@@@@@@@@%=..+%@@@@@@@@@@@@@@@@%+                  
                              -*%%@@@@@@@@@@%#+:      -+%@@@@@@@@@@@%+.                   
                                 .:=+++++=-.             .-=+***++-.                                        
                                                                                   
"""

print(github_banner)

parser = argparse.ArgumentParser(description="Help Menu")

parser.add_argument(
    "function", help="`pull` or `check`")
parser.add_argument("--host", help="Domain/Host Name")
parser.add_argument(
    "--threads", help="The number of threads", default=5)
parser.add_argument(
    "--with-subs", help="`yes` or `no`", default=True)
parser.add_argument(
    "--loadfile", help="File location")
parser.add_argument(
    "-o", "--outputfile", help="Output file to save results")

args = parser.parse_args()

def waybackurlsFunction(host, with_subs):
    if with_subs:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{host}/*&output=list&fl=original&collapse=urlkey"
    else:
        url = f"http://web.archive.org/cdx/search/cdx?url={host}/*&output=list&fl=original&collapse=urlkey"
    requestsVariable = requests.get(url)
    if args.outputfile:
        openFileVariable = open(args.outputfile, "w")
        openFileVariable.write(requestsVariable.text.strip())
        openFileVariable.close()
    print(requestsVariable.text.strip())


def checkGivvenDomainNameFunction(url):
    global timeOutGlobalVariable
    if url == "":
        return
    url = url.replace(":80/", "/").replace(":443/", "/")
    if not url.startswith("http"):
        url = f"http://{url}"
    domainName = urllib.parse.urlparse(url).netloc.split(":")[0]
    if domainName in timeOutGlobalVariable:
        return
    try:
        requestVariablTwo = requests.head(
            url, verify=False, timeout=0.25)
    except requests.exceptions.Timeout:
        timeOutGlobalVariable.append(domainName)
        return
    except requests.exceptions.ConnectionError:
        timeOutGlobalVariable.append(domainName)
        return
    if str(requestVariablTwo.status_code)[0] == "3" and url.startswith("http://") and requestVariablTwo.headers["Location"].startswith("https://"):
        try:
            requestVariablTwo = requests.head(
                f"https{url[4:]}", verify=False, timeout=0.25)
        except requests.exceptions.Timeout:
            return
    statusCodeVariable = requestVariablTwo.status_code
    if statusCodeVariable == 404:
        return
    if "Content-Length" in list(requestVariablTwo.headers.keys()):
        cLength = requestVariablTwo.headers["Content-Length"]
    else:
        cLength = "Unknown"
    if "Content-Type" in list(requestVariablTwo.headers.keys()):
        cType = requestVariablTwo.headers["Content-Type"]
    else:
        cType = "Unknown"
    if str(statusCodeVariable)[0] == "3":
        rUrl = requestVariablTwo.headers["Location"]
        print(", ".join([url, str(statusCodeVariable), cLength, cType, rUrl]))
        if args.outputfile:
            writeQueueVariable.put(
                ", ".join([url, str(statusCodeVariable), cLength, cType, rUrl])+"\n")
    else:
        print(", ".join([url, str(statusCodeVariable), cLength, cType]))
        if args.outputfile:
            writeQueueVariable.put(
                ", ".join([url, str(statusCodeVariable), cLength, cType])+"\n")


def checkGivvenDomainNameFunctionValidDomain(endpoints):
    validDomains = []
    invalidDomainNames = []
    validEndpoints = []
    for endpoint in endpoints:
        endpoint = endpoint.strip().strip("\r").strip("").strip("")
        try:
            parsedUrl = urllib.parse.urlparse(endpoint)
            domainName = parsedUrl.netloc.split(":")[0]
            if domainName in validDomains:
                validEndpoints.append(endpoint)
                continue
            elif domainName in invalidDomainNames:
                continue
            try:
                socket.gethostbyname(domainName)
                validDomains.append(domainName)
                validEndpoints.append(endpoint)
            except:
                invalidDomainNames.append(domainName)
        except:
            continue
    return validEndpoints


def writterFunction(fileToWrite):
    while True:
        line = writeQueueVariable.get(True)
        if line == None:
            break
        fileToWrite.write(line)


Manager = multiprocessing.Manager()
timeOutGlobalVariable = Manager.list()
writeQueueVariable = Manager.Queue()
pool = multiprocessing.Pool(args.threads)
if args.function == "pull":
    if args.host:
        print('\nFetching URLs, It"s take some time Please Wait...\n')
        waybackurlsFunction(args.host, args.with_subs)
    elif args.loadfile:
        for line in open(args.loadfile).readlines():
            waybackurlsFunction(line.strip(), args.with_subs)

elif args.function == "checkGivvenDomainNameFunction":
    if args.loadfile:
        try:
            if args.outputfile:
                outputfile = open(args.outputfile, "w", 0)
                p = multiprocessing.Process(
                    target=writterFunction, args=(outputfile,))
                p.start()
            endpoints = checkGivvenDomainNameFunctionValidDomain(
                open(args.loadfile).readlines())
            pool.map(checkGivvenDomainNameFunction, endpoints)
            if args.outputfile:
                writeQueueVariable.put(None)
                p.join()
                outputfile.close()
        except IOError as error:
            print("Sorry, File not found!")
            sys.exit(1)
        except KeyboardInterrupt as error:
            print("Killing processes.")
            pool.terminate()
            sys.exit(1)
        except Exception as error:
            print(f"An error occurred: {error}")

    elif not sys.stdin.isatty():
        try:
            if args.outputfile:
                outputfile = open(args.outputfile, "w", 0)
                p = multiprocessing.Process(
                    target=writterFunction, args=(outputfile,))
                p.start()
            endpoints = checkGivvenDomainNameFunctionValidDomain(
                sys.stdin.readlines())
            pool.map(checkGivvenDomainNameFunction, endpoints)
            if args.outputfile:
                writeQueueVariable.put(None)
                p.join()
                outputfile.close()
        except IOError as error:
            print(f"An error occurred: {error}")
            print("File not found!")
            sys.exit(1)
        except KeyboardInterrupt as error:
            print("Killing processes.")
            pool.terminate()
            sys.exit(1)
        except Exception as error:
            print(f"An error occurred: {error}")
    else:
        print("Please either specify a file.")
        exit()
