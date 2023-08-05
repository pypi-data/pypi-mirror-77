import os
from glob import glob
from time import time

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.cache_classes.cache_data_file import CacheDataFile
from cache_gs.interfaces.super_cache import SuperCache
from cache_gs.utils.timestamp import section_key_hash


class FileCache(SuperCache):

    CACHE_SECTION = '__file_cache'
    LAST_PURGE = '__last_purge'

    def setup(self):
        self._string_connection = os.path.abspath(
            self._string_connection.split('://')[1])
        if not os.path.isdir(self._string_connection):
            subpath = os.path.dirname(self._string_connection)
            if not os.path.isdir(subpath):
                raise FileNotFoundError(self._string_connection)
            self.log_info(
                'Creating cache folder [%s]', self._string_connection)
            os.makedirs(self._string_connection)

        if self._check_need_purge():
            self.purge_expired()

    def _get_value(self, section, key, default=None) -> CacheData:
        data = CacheData(section, key, None, 0, data_serialized=True)
        filename = self._file_name(data, False)
        cdf = CacheDataFile()
        if cdf.load(filename):
            return cdf.data

        return CacheData(section, key, default, 0)

    def _set_value(self, data):
        filename = self._file_name(data, True)
        cdf = CacheDataFile(cache_data=data)
        return cdf.save(filename)

    def _delete_value(self, data):
        filename = self._file_name(data, False)
        if os.path.isfile(filename):
            os.unlink(filename)
        return not os.path.isfile(filename)

    def purge_expired(self):
        subfolders = [
            folder
            for folder in glob(os.path.join(self._string_connection, '*'))
            if os.path.isdir(folder)]
        expired_count = 0
        for subfolder in subfolders:
            subsubfolders = [
                folder
                for folder in glob(os.path.join(subfolder, '*'))
                if os.path.isdir(folder)
            ]
            for subsubfolder in subsubfolders:
                expired_count += self._purge_expired_folder(subsubfolder)

            self._remove_empty_folder(subfolder)
        self.set_value(self.CACHE_SECTION, self.LAST_PURGE, str(int(time())))
        return expired_count

    def _check_need_purge(self) -> bool:
        """ Returns True if last purge occurred more than one day ago """
        last_purge = self.get_value(
            section=self.CACHE_SECTION,
            key=self.LAST_PURGE,
            default='0'
        )
        if not last_purge.isnumeric():
            self.set_value(self.CACHE_SECTION, self.LAST_PURGE, '0')
            last_purge = 0
        else:
            last_purge = int(last_purge)

        return last_purge < time()-86400

    def _purge_expired_folder(self, folder):
        cache_files = [
            file
            for file in glob(os.path.join(folder, '*'))
            if os.path.isfile(file)
        ]
        expired_count = 0
        for cache_file in cache_files:
            cdf = CacheDataFile(cache_file)
            if not cdf.data or cdf.data.expired:
                expired_count += 1

        self._remove_empty_folder(folder)

        return expired_count

    def _remove_empty_folder(self, folder):
        if len(glob(os.path.join(folder, '*'))) == 0:
            os.rmdir(folder)

    def _file_name(self, data: CacheData, create_folder: bool):
        filename = section_key_hash(data.section, data.key)
        dirname = os.path.join(self._string_connection,
                               filename[:2], filename[2:4])
        if create_folder and not os.path.isdir(dirname):
            self.log_debug('Creating cache folder [%s]', dirname)
            os.makedirs(dirname)
        return os.path.join(dirname, filename)
