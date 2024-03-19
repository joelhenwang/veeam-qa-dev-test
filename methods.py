import hashlib
import logging
import pathlib
import shutil
import time
import os

def sync(src_path, replica_path, log_file_path, sync_interval):
    """ Sync every sync_interval seconds """
    
    # Configure the logger
    config_logger(log_file_path)
    print('Logger configured')
    
    while True:
        sync_folders(src_path, replica_path, log_file_path)
        time.sleep(sync_interval)
    
    

def config_logger (log_file):
    # Set up logging
    logging.basicConfig(filename=log_file, 
                        filemode='a+',
                        level=logging.INFO, 
                        datefmt='%d-%m-%y %H:%M:%S',
                        format='[%(asctime)s] - [%(levelname)s]: %(message)s')
    

def sync_folders (src_path, replica_path, log_file_path):
    """
    Synchronize the source folder with the replica folder
    """

    # Get list of files and folders in source folder
    # if not os.path.isdir(src_path):
    #     except(f'Source folder {src_path} does not exist')
        
    src_files = os.listdir(src_path)
    print(f'Source files: {src_files}')


    # Get list of files and folders in replica folder
    # If the folder does not exist, create it
    if not os.path.isdir(replica_path):
        os.makedirs(replica_path)
        logging.info(f'Replica folder not detected. Creating {replica_path} folder')
    
    replica_files = os.listdir(replica_path)
    print(f'Replica files: {replica_files}')


    for file in src_files:
        try:
            file_src_path = os.path.join(src_path, file)
            file_replica_path = os.path.join(replica_path, file)
            print()
            print(f'File: {file}')
            print(f'File src path: {file_src_path}')
            print(f'File replica path: {file_replica_path}')
            
            # If file is a folder
            if os.path.isdir(file_src_path):
                # If the folder is not in the replica tree, duplicate it
                # Else, recursively call the function to synchronize the subfolders
                if file not in replica_files:
                    shutil.copytree(file_src_path, file_replica_path, symlinks=True)
                    logging.info(f'Folder {file} copied')
                    print(f'Folder {file} copied')
                else:
                    src_subfolder_path = os.path.join(src_path, file)
                    replica_subfolder_path = os.path.join(replica_path, file)
                    sync_folders(src_subfolder_path, replica_subfolder_path, log_file_path)
            else:
                # If the file is not in the replica tree, copy it
                # else, compare the checksums of the files
                if file not in replica_files:
                    shutil.copy2(file_src_path, file_replica_path, follow_symlinks=True)
                    logging.info(f'File {file} copied')
                    print(f'File {file} copied')
                else:
                    # If the checksums are not equal, copy (ovewrite) the file
                    if not equal_checksums(file_src_path, file_replica_path):
                        shutil.copy2(file_src_path, file_replica_path, follow_symlinks=True)
                        replica_files.remove(file)
                        logging.info(f'File {file} copied')
                        print(f'File {file} copied')
        except Exception as e:
            logging.error(f'Error: {e}')
            print(f'Error: {e}')
            continue
        
        
    # If a file or folder is in the replica tree and not in the source tree, 
    # delete it from the replica tree
    for file in replica_files:
        if file not in src_files:
            try:
                file_replica_path = os.path.join(replica_path, file)
                
                if os.path.isdir(file):
                    shutil.rmtree(file_replica_path, ignore_errors=True)
                    logging.info(f'Folder {file} deleted')
                else:
                    pathlib.Path(file_replica_path).unlink()
                    logging.info(f'File {file} deleted')
            except Exception as e:
                logging.error(f'Error: {e}')
                print(f'Error: {e}')
                continue


 

def equal_checksums(src_path, replica_path):
    """ Compare the checksums of two files """
    with open(src_path, "rb") as f1, open(replica_path, "rb") as f2:
        return hashlib.sha256(f1.read()).hexdigest() == hashlib.sha256(f2.read()).hexdigest()

