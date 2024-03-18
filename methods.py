import logging
import pathlib
import shutil
import os
import time


def config_logger (log_file):
    # Set up logging
    logging.basicConfig(filename=log_file, 
                        level=logging.INFO, 
                        datefmt='%d-%m-%y %H:%M:%S',
                        format='[%(asctime)s] - [%(levelname)s]: %(message)s')

def sync_folder (src_path, replica_path, log_file_path, time_interval):
    """
    Synchronize the source folder with the replica folder
    """
    while True:
        try:
            # Get list of files and folders in source folder
            src_tree = os.listdir(src_path)

            # Get list of files and folders in replica folder
            replica_tree = []
            if not os.path.isdir(replica_path):
                os.makedirs(replica_path)
            else:
                replica_tree = os.listdir(replica_path)

            #TODO checksum of both trees first

            # Get list of files to be copied #TODO files only
            files_to_copy = [file for file in src_tree if file not in replica_tree]

            # Copy files
            for file in files_to_copy:
                #TODO if checksum
                copy_file(src_path, replica_path, file)

            # Get list of files to be deleted
            files_to_delete = [file for file in replica_tree if file not in src_tree]

            # Delete files
            for file in files_to_delete:
                delete_file(file, replica_path)

            # Wait for the next synchronization
            time.sleep(time_interval)

        except Exception as e:
            logging.error(f'{e}')

def copy_file(file, src_path, replica_path):
    src_file_path = os.path.join(src_path, file)
    replica_file_path = os.path.join(replica_file_path, file)
    shutil.copy2(src_file_path, replica_file_path, follow_symlinks=True)
    logging.info(f'COPY FILE - SRC: {src_file_path} ==> DEST: {replica_file_path}')
    

def delete_file(file, replica_path):
    replica_file_path = os.path.join(replica_path, file)
    pathlib.unlink(replica_file_path, missing_ok = False)
    logging.info(f'DELETE FILE - {replica_file_path}')

def copy_folder(folder, src_path, replica_path):
    pass

def delete_folder(folder, replica_path):
    pass
    

def check_file_hash_lite():
    pass

def check_file_hash_full():
    pass

