#!/usr/bin/env python
# coding: utf-8
# 基于继承的代码重用

import os
import shutil
import zipfile
import sys

class ZipProcessor:
    def __init__(self, zipname):
        self.zipname = zipname
        self.temp_directory = "unzipped-{}".format(zipname[:-4])

    def _full_filename(self, filename):
        return os.path.join(self.temp_directory, filename)

    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def unzip_files(self):
        os.mkdir(self.temp_directory)
        zip = zipfile.ZipFile(self.zipname)
        try:
            zip.extractall(self.temp_directory)
        finally:
            zip.close()

    def zip_files(self):
        file = zipfile.ZipFile(self.zipname, 'w')
        for filename in os.listdir(self.temp_directory):
            file.write(self._full_filename(filename), filename)
        shutil.rmtree(self.temp_directory)

class ZipReplace(ZipProcessor):
    def __init__(self, filename, search_string, replace_string):
        super().__init__(filename)
        self.search_string = search_string
        self.replace_string = replace_string

    def process_files(self):
        for filename in os.listdir(self.temp_directory):
            with open(self._full_filename(filename)) as infile, \
                    open(self._full_filename(filename),'w') as outfile:
                outfile.write(infile.read().replace(self.search_string, self.replace_string))

if __name__ == '__main__':
    zr = ZipReplace(*sys.argv[1:4]).process_zip()