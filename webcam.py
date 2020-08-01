#!/usr/bin/env python3.7.3-1

import dropbox
from dropbox.exceptions import ApiError, AuthError
import time
import datetime
import picamera
import sys, os
import subprocess

# Authorisation token, MUST BE ADDED OR THIS WON'T WORK
TOKEN = ''

# Format photo will be saved as e.g. jpeg
PHOTOFORMAT = 'jpeg'



# Create a camera object and capture image using generated filename
def camCapture(filename):
    
    subprocess.Popen(["fswebcam", filename + "." + PHOTOFORMAT])
    time.sleep(2)
    return filename + '.' + PHOTOFORMAT



# Generate timestamp string generating name for photos
def timestamp():
    tstring = datetime.datetime.now()
    print("Filename generated ...")
    return tstring.strftime("%Y%m%d_%H%M%S")



# Upload localfile to Dropbox
def uploadFile(localfile):

    # Check that access tocken added
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Missing access token. "
                 "try re-generating an access token from the app console at dropbox.com.")

    # Create instance of a Dropbox class, which can make requests to API
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console at dropbox.com.")

    # Specify upload path
    uploadPath = '/' + localfile

    # Read in file and upload
    with open(localfile, 'rb') as f:
        print("Uploading " + localfile + " to Dropbox as " + uploadPath + "...")

        try:
            dbx.files_upload(f.read(), uploadPath)
        except ApiError as err:
            # Check user has enough Dropbox space quota
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot upload; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()



# Delete file
def deleteLocal(file):
    os.system("rm " + file)
    print("File: " + file + " deleted ...")



def main():

    # Generate name for file based on current time
    filename = timestamp()

    # Capture photo
    file = camCapture(filename)


    # Upload file
    uploadFile(file)

    # Delete local file
    #deleteLocal(file)

    print("Done")



if __name__ == '__main__':
    main()