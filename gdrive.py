from __future__ import print_function
from datetime import datetime
import os.path,sys,predef
import makeAuth as auth
import generalHandler as hand
import argparse

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
    handJob.upload() if u=='y' or u=='Y' else handJob.destroy()

# def process_this(path):
#     service = auth.get_service()
#     print('Authenticated.')
    
#     #zipFileName = zip_this(predef.FOLDER_TO_ZIP_DIRECTORY)
#     #print('zipped name->{0}'.format(zipFileName))

#     # let's go to constructor!
#     handJob = hand.Job(fileName=path, service=service) # this is not ```handjob``` tho
#     user(handJob)

def main():
    parser = argparse.ArgumentParser(description='laxz G-drive uploader-MLdataset or Backup')
    parser.add_argument('-m','--mode',default = None ,required=True, 
        help='select Mode how laxz G-drive runs. dataset, backup')
    args = parser.parse_args()
    
    if(args.mode == "dataset"):
        case = input('dataset case-? : ')
        dataset_path = predef.DATASET+'/'+case

        if(os.path.exists(dataset_path)):
            os.system("zip -r /home/laxz/custom.zip "+dataset_path)
            user(hand.Job("/home/laxz/custom.zip", auth.get_service(), args.mode, case))

        else:
            print('path 404.')
            exit()
    else:
        print('Not an option.')

if __name__ == "__main__":
    main()
