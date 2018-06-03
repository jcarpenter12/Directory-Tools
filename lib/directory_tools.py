import os
import time
from filelock import FileLock
import logging
import shutil

logger = logging.getLogger('directory_tools')


class DirectoryTools:
    directory = None
    fileList = None

    def __init__(self, _directory):
        if os.path.isdir(str(_directory)):
            self.directory = _directory
        else:
            logger.exception("Directory \"%s\" does not exist" % _directory)
        self.get_files(replace=True)

    def get_files(self, replace=False):
        file_list = list()
        for root, dirs, files in os.walk(str(self.directory), topdown=True):
            for name in files:
                file_list.append(os.path.abspath(os.path.join(root, name)))
        if replace:
            self.fileList = file_list
            return self.fileList
        else:
            return file_list

    def get_total_size(self):
        total_size = 0
        for f in self.fileList:
            total_size += os.path.getsize(f)
        logger.info('Total Size of {} = {}'.format(self.fileList, total_size / 1000))
        return total_size / 1000

    def subset_by_creation_date(self, replace=False, time_span=None):
        file_list = list()
        for f in self.fileList:
            if os.path.getctime(f) < time.time() - time_span:
                file_list.append(f)
                logger.debug(f)
        if replace:
            self.fileList = file_list
            return self.fileList
        else:
            return file_list

    def delete_files(self):
        for f in self.fileList:
            # acquire lock
            lock = FileLock(f + ".lock")

            with lock as r:
                if r is not None:
                    try:
                        os.remove(f)
                        logger.info('File "{}" deleted'.format(f))
                    except OSError as e:
                        logger.exception(e)
                else:
                    logger.warning("Lock could not be acquired for %s" % f)

    def copy_files(self, destination=None):
        logger.debug(self.fileList)
        if not os.path.isdir(str(destination)):
            logger.warning('{} does not exist, creating directory'.format(str(destination)))
            os.mkdir(str(destination))
        for f in self.fileList:
            # acquire lock
            lock = FileLock(f + ".lock")

            with lock as r:
                if r is not None:
                    try:
                        shutil.copy2(f, destination)
                    except OSError as e:
                        logger.exception(e)
                    else:
                        logger.info('File "{}" copied to "{}"'.format(f,destination))
                else:
                    logger.warning("Lock could not be acquired for %s" % f)

    ###TODO
    # def subset_by_extension(self, replace=False, extIgnoreList=[], fileIgnoreList=[]):
    #     fileList = list()
    #
    #     for files in self.fileList:
    #         # files[:] = [f for f in files if f not in fileIgnoreList]
    #         if len(extIgnoreList) > 0:
    #             files[:] = [f for f in files if not
    #             f.endswith(tuple(ext for ext in extIgnoreList))]
    #         for name in files:
    #             fileList.append(name)
    #     if replace:
    #         self.fileList = fileList
    #         return self.fileList
    #     else:
    #         return fileList
