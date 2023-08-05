import logging
import os
import fcntl
import gzip

from logging.handlers import RotatingFileHandler
from shutil import copyfile


class MultiprocessingHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        self.need_zip = kwargs.pop('need_zip', False)
        self.compresslevel = kwargs.pop('compresslevel', 9)
        super().__init__(*args, **kwargs)
        self.__lock_pool = {}
        self.__lock_filename = os.path.join(os.path.dirname(self.baseFilename, ), '.loglockfile')
        # 使用该handler的前提是打开文件的模式是 'a'
        assert self.mode == 'a'


    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        f = None
        try:
            # 建议在初始化的时候将这个锁文件的目录初始化好,避免每次拼接,这里为了方便就写在这里了

            # 为了加快打印速度,我们也可以做一个文件池来存储已经打开的文件的文件描述符,
            # 但是需要使用本进程的id作为唯一的key来保证这个文件是本进程打开的而不是从父进程继承的
            f = self.__lock_pool.get(os.getpid())
            if f == None:
                f = open(self.__lock_filename, 'wb')
                self.__lock_pool[os.getpid()] = f
            # 加锁
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            # 首先写入文件以获取到文件的大小
            logging.FileHandler.emit(self, record)
            if self.shouldRollover(record):
                self.doRollover()

        except Exception:
            self.handleError(record)
        finally:
            if f:
                # 解锁
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def rotate(self, source, dest):
        if self.need_zip:
            with gzip.open(dest, 'wb', ) as f_gz:
                with open(source, 'rb') as f_source:
                    f_gz.write(f_source.read())
        else:
            copyfile(source, dest)
        # clear the log file
        with open(source, 'wb'):
            pass

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
                                                        i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            if self.need_zip:
                dfn = self.rotation_filename(self.baseFilename + ".1.gz")
            else:
                dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()
