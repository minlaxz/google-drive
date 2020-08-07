from googleapiclient.http import MediaFileUpload
import conn,sys,predef,os
class Job:
    def __init__(self, this_one, this_service, this_flag, this_case):
        if not conn.check():
            print('Internet connection needed.')
            sys.exit()
        self.fileName = this_one
        self.service = this_service
        self.flag = this_flag
        self.case=this_case
        self.folderID = _get_folder_id(self.service, self.flag, self.case)
        print('ready to upload {0}'.format(self.folderID))
    
    def zipThis(self):
        pass
    
    def upload(self):
        print('uploading file->{0} to folder->{1} '.format(self.fileName, self.folderID))
        file_metadata = {
  		'name' : self.fileName,
  		'parents': [ self.folderID ]
	        }
        media = MediaFileUpload(self.fileName, mimetype='application/zip', resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='name,id').execute()
        print('file uploaded {0}, {1}'.format(file.get('id'), file.get('name')))
        self.destroy()
    
    def destroy(self):
        self.fileName = None
        os.system("rm -f "+self.fileName)

    

def _get_folder_id(service,flag,case):
    if (flag=="dataset"):
        G_FOLDER=predef.G_DATASET+case
    elif (flag=="backup"):
        G_FOLDER=predef.GDRIVE_FOLDER_NAME
    else:
        print("UnknOwn ErrOR!")
        exit()
    results = service.files().list(q="name='"+G_FOLDER +"'",
                            spaces='drive',
                            fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])
    if items:
       folderID = items[0]['id']
    else:
        folder_metadata = {
            'name' : predef.GDRIVE_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
            }
        folder = service.files().create(body=folder_metadata,fields='id').execute()
        folderID = folder.get('id')
    return folderID