# One way folder synchronization

#### This program performs one-way synchronization between two folders, one source and one replica.
* The synchronization occurs periodically and for every period the program checks for changes in the source folder aswell as in the replica folder.
* If a file is added, modified or deleted in the source folder, the program will update the replica folder to match the source folder.
* The program uses the SHA256 hash of files to determine if a file needs to be updated in the replica folder.
* The folder paths, synchronization interval and log file path are provided to the program using command line arguments and are required in order to run the program.

## Requirements

* Python 3.x
* Libraries: argparse, hashlib, logging, pathlib, shutil, time, os

## Usage

```
python main.py [--source SOURCE_FOLDER_PATH] [--replica REPLICA_FOLDER_PATH] [--log-file-path LOG_FILE_PATH] [--sync-interval SYNC_TIME_INTERVAL]
```

- `--source`: Path to the source folder.
- `--replica`: Path to the replica folder.
- `--log-file-path`: Path to the log file.
- `--sync-interval`: Synchronization interval in seconds.
