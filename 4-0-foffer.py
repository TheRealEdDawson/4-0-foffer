import subprocess
import re
import string
import sys
import requests
import requests.exceptions

# Checking that all the arguments were entered on the command line, exiting with a message if not.
def checkstart():
    if len(sys.argv) != 3:
        argumentsNotSet = 'Missing argument(s).\nUsage is like so:\nPython 4-0-foffer.py SITEMAP-FILENAME.TXT LOG-FILENAME.TXT'
        print (argumentsNotSet)
        sys.exit(1)

checkstart() # Check the command line arguments were passed
# Example usage: python scrape_n_spell.py http://docs.learnosity.com logfile.txt

siteMapFileName = sys.argv[1] # The sitemap filename that will be read to find URLs to check
logFileName = sys.argv[2] # Command-line argument that specifies the log file filename

# TO DO: Analyse that RAW HTML text and do some detections:
# 1. Detect a login page (indicating the page's permissions are restricted),

count = 0

logFile = open(logFileName, 'w') # Open the log file (in "write" mode, overwriting old one)

print ("\n4-0-Foffer: A site map crawler.\n") # Introduction message to console
logFile.write("4-0-Foffer: A site map crawler.\n") # Introduction message to log file

print("Processing sitemap file: \n", siteMapFileName) # Site name scraped to console
logFile.write("Processing sitemap file: \n") # Logging
logFile.write(siteMapFileName) # Logging

siteMap = open(siteMapFileName, 'r') # Open the sitemap file (as read-only)

# Loop to access all URLs in the site map text file
for line in siteMap:
    count = count + 1 # Count the number of page accesses.
    print('\n\nCount: ',count,'\n') # Logging
    countValue = ('\n\nCount: ' + str(count)) # Logging
    logFile.write(countValue) # Logging
    thisPage = line # read one line (a URL) from the site map
    #thisPage = siteMap.readline() # read one line (a URL) from the site map
    
    print("\nAccessing site: \n", thisPage) # Site name scraped to console
    logFile.write("\nAccessing site: ") # Site name scraped to disk
    logFile.write(thisPage) # Site name scraped to disk
    session = requests.session() # Create a session. (not required?)
    try: # Gracefully capture failures and report what happened.
        accessAttempt = requests.request("GET", thisPage, timeout=60, allow_redirects=False)
        print('Server responded:')
        logFile.write("Server responded:")
        print('HTTP status: ', accessAttempt.status_code)
        logFile.write("HTTP status: ")
        logFile.write(str(accessAttempt.status_code))
        if (accessAttempt.status_code==301):
            print('Redirected to:', accessAttempt.headers['Location'])
            logFile.write("Redirected to:")
            logFile.write(accessAttempt.headers['Location'])
    except requests.exceptions.ConnectionError as e:
        print("Error accessing page, exception follows: \n\n", e) 
        logFile.write("Error accessing page, exception follows: \n\n")
        logFile.write(str(e))

print ("\n\nProgram complete.\n\n") # Status to console
logFile.write("\n\nProgram complete.\n\n") # Status to disk

# TO DO: If 200 is returned, ensure that we're not serving up a legacy site URL or a login page

print ("\nOutput written to log file: ", logFileName)
logFile.write("\nOutput written to log file: ")
logFile.write(logFileName)

siteMap.close() # Close off the sitemap file
logFile.close() # Close off the log file

#End of file.
