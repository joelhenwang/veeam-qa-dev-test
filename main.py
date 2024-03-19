import argparse
from methods import sync

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Folder synchronization program')

    # Source folder path
    parser.add_argument('--source', type=str, required=True, help='Source folder path')

    # Replica folder path
    parser.add_argument('--replica', type=str, required=True, help='Replica folder path')

    # Log file path
    parser.add_argument('--log-file-path', type=str, required=True, help='Log file path')

    # Synchronization Time interval
    parser.add_argument('--sync-interval', type=int, required=True, help='Synchronization interval in seconds')

    # Parse arguments
    args = parser.parse_args()

    sync(args.source, args.replica, args.log_file_path, args.sync_interval)