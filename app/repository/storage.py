import os
from app.repository.fb import storageBucket, ROOT_DIR
from firebase_admin.exceptions import NotFoundError

class MyStorageBucket:
    
    def __init__(self) -> None:
        self.main_directory = "storage"
    
    def get_file(self, key:str):
        blob = storageBucket.blob(f"storage/{key}")
        file_name = f"{ROOT_DIR}/build/{key}"
        try:
            blob.download_to_filename(file_name)
        except NotFoundError as e:
            return e.cause
        return file_name
    
    def delete_tmp(self, file_name:str):
        #delete the file from binaries
        os.remove(os.path.abspath(file_name))
