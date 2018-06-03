import sys, json
from lib.directory_tools import *


def main():
    # configure logging
    import logging.config
    logging.config.fileConfig('config/log_config.ini')
    logger = logging.getLogger('root')
    logger.info('Logging Configured from {}'.format("config/log_config.ini"))

    # Config setup
    env = sys.argv[1] if len(sys.argv) > 2 else 'DEV'
    config_path = r'config/config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    if env == 'DEV':
        config = config['DEV']
        logging.info('Using DEV configuration')
    elif env == 'TEST':
        config = config['TEST']
        logging.info('Using TEST configuration')
    elif env == 'PROD':
        config = config['PROD']
        logging.info('Using PROD configuration')


    #Main Script
    for directory in config['DIRECTORIES']:
        logger.info("{} ####STARTING####".format(directory['INPUT_DIR']))
        dm = DirectoryTools(directory['INPUT_DIR'])
        logger.info("FileList: {}".format(dm.fileList))
        dm.get_total_size()
        dm.subset_by_creation_date(replace=True, time_span=10)
        if len(directory['ARCHIVE']) > 0:
            logger.info('Archiving {} to {}'.format(directory['INPUT_DIR'], directory['ARCHIVE']))
            dm.copy_files(destination=directory['ARCHIVE'])
        if directory['DELETE']:
            logger.info('Deleting files from {}'.format(directory['INPUT_DIR']))
            dm.delete_files()
        logger.info("{} ####COMPLETE####".format(directory['INPUT_DIR']))


if __name__ == "__main__":
    main()
