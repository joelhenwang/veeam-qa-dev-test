import hashlib
import logging
import pathlib
import shutil
import time
import os

def init_sync(src_path, replica_path, log_file_path, sync_interval):
    """ 
    One way folder synchronization every 'sync_interval' seconds

    Args:
    src_path (str): Source folder path
    replica_path (str): Replica folder path
    log_file_path (str): Log file path
    sync_interval (int): Synchronization interval in seconds

    Description:
    The function synchronizes the source folder with the replica folder every 'sync_interval' seconds.
    The synchronization process copies new files and folders from the source folder to the replica folder
    if they're non-existent in the replica folder.
    If a file is modified in the source folder, the file in the replica folder will be overwritten by the newer file.
    If a file or folder is deleted from the source folder, it will be deleted from the replica folder.

    """
    
    # Configure the logger
    config_logger(log_file_path)
    
    # Start the synchronization loop
    logging.info('INITIALIZING folder synchronization process...')
    logging.info(f'SOURCE folder: "{src_path}"')
    logging.info(f'REPLICA folder: "{replica_path}"')

    while True:
        sync_folders(src_path, replica_path, log_file_path)
        time.sleep(sync_interval)
    
    

def config_logger (log_file):
    """
    Configure the logger

    Args:
    log_file (str): Log file path

    Description:
    The function configures the logger to log messages to a file and to the console.
    Logs messages with the following format:
    [DD/MM/YY HH:MM:SS] - [LEVEL]: 'MESSAGE'

    """

    log_formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s]: %(message)s', 
                                  datefmt='%d/%m/%y %H:%M:%S')

    # Set up logging config
    logging.basicConfig(filename=log_file, 
                        filemode='a',
                        level=logging.INFO, 
                        datefmt='%d/%m/%y %H:%M:%S',
                        format='[%(asctime)s] - [%(levelname)s]: %(message)s')
    
    # Set a stream handler and set level to info
    console = logging.StreamHandler()
    console.setFormatter(log_formatter)
    console.setLevel(logging.INFO)

    # Add the handler to root logger
    logging.getLogger('').addHandler(console)
    

def sync_folders (src_path, replica_path, log_file_path):

    # Get list of files and folders in source folder
    if not os.path.isdir(src_path):
        logging.error(f'SOURCE folder "{src_path}" not found. TERMINATING PROCESS') 
        raise FileNotFoundError(f'SOURCE folder "{src_path}" not found.')  
    
    src_files = os.listdir(src_path)


    # Get list of files and folders in replica folder
    # If the folder does not exist, create it
    if not os.path.isdir(replica_path):
        logging.info(f'REPLICA folder not detected. Creating "{replica_path}" folder')
        os.makedirs(replica_path)  
    
    replica_files = os.listdir(replica_path)


    # Iterate through the files and folders in the source folder
    for file in src_files:
        try:
            file_src_path = os.path.join(src_path, file)
            file_replica_path = os.path.join(replica_path, file)

            # If file is a folder
            if os.path.isdir(file_src_path):
                # If the folder is not in the replica tree, duplicate it
                # Else, recursively call the function to synchronize the subfolders
                if file not in replica_files:
                    shutil.copytree(file_src_path, file_replica_path, symlinks=True, dirs_exist_ok=True)
                    logging.info(f'SUBFOLDER "{file_src_path}" copied to REPLICA')
                else:
                    src_subfolder_path = os.path.join(src_path, file)
                    replica_subfolder_path = os.path.join(replica_path, file)
                    sync_folders(src_subfolder_path, replica_subfolder_path, log_file_path)
            else:
                # If the file is not in the replica tree, copy it
                # else, compare the checksums of the files
                if file not in replica_files:
                    shutil.copy2(file_src_path, file_replica_path, follow_symlinks=True)
                    logging.info(f'FILE "{file_src_path}" copied to REPLICA')
                else:
                    # If the checksums are not equal, copy (ovewrite) the file
                    if not equal_checksums(file_src_path, file_replica_path):
                        logging.info(f'Detected changes in FILE "{file_src_path}". Copying file to REPLICA')
                        shutil.copy2(file_src_path, file_replica_path, follow_symlinks=True)
                        replica_files.remove(file)

        
        except Exception as e:
            logging.error(f'{e}')
            continue
        
    # Iterate through the files and folders in the replica folder
    # If a file or folder is in the replica tree and not in the source tree, 
    # delete it from the replica tree
    for file in replica_files:
        if file not in src_files:
            try:
                file_replica_path = os.path.join(replica_path, file)
                if os.path.isdir(file_replica_path):
                    shutil.rmtree(file_replica_path)
                    logging.info(f'SUBFOLDER "{file_replica_path}" deleted.')
                else:
                    pathlib.Path(file_replica_path).unlink()
                    logging.info(f'FILE "{file_replica_path}" deleted.')

            except Exception as e:
                logging.error(f'{e}')
                continue


 

def equal_checksums(src_path, replica_path):
    """ 
    Compare the checksums of two files 

    Args:
    src_path (str): Source file path
    replica_path (str): Replica file path

    Returns:
    bool: True if the checksums are equal, False otherwise

    Description:
    The function compares the checksums of the source file and the replica file.
    If the checksums are equal, the function returns True. Otherwise, it returns False.

    """
    with open(src_path, "rb") as f1, open(replica_path, "rb") as f2:
        return hashlib.sha256(f1.read()).hexdigest() == hashlib.sha256(f2.read()).hexdigest()
    
def equal_checksums_lite(src_path, replica_path):
    """ Compare the checksums of the first 2kb of two files """
    with open(src_path, "rb") as f1, open(replica_path, "rb") as f2:
        return hashlib.sha256(f1.read(2048)).hexdigest() == hashlib.sha256(f2.read(2048)).hexdigest()

