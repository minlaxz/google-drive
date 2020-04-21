from __future__ import print_function
from datetime import datetime
import os.path,sys,predef
import makeAuth as auth
import generalHandler as hand

def getTimestampLabel():
    return "BACKUP_"+datetime.now().strftime('%d_%b_%Y__%X').replace(":","_")
	#return "BACKUP_"+time.strftime("%x").replace("/","-")+"_"+time.strftime("%X")+"_"+str(int(round(time.time())))

def zip_this(directory):
    if not os.path.exists(directory):
        print('no folder found to backup.')
        sys.exit()
    print("Creating ZIP folder to upload...")
    zipFileName = getTimestampLabel()+".zip"
    os.system("zip -r "+zipFileName+" "+directory)
    print("ZIP folder created: "+zipFileName+"\n")
    return zipFileName # 'Backup_20_Apr_2020__00_22_18.zip'

def user(handJob):
    u = input('upload? y/n :')
    if (u=='y' or u=='Y'):
        handJob.upload()
    else:
        handJob.destroy()
        handJob.fileName = None
        sys.exit()

def main():
    service = auth.get_service()
    print('Authenticated.')

    zipFileName = zip_this(predef.FOLDER_TO_ZIP_DIRECTORY)
    print('zipped name->{0}'.format(zipFileName))

    # let's go to constructor!
    handJob = hand.Job(fileName=zipFileName, service=service) # this is not ```handjob``` tho
    user(handJob)

if __name__ == "__main__":
    main()
