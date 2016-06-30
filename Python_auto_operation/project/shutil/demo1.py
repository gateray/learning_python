#!/usr/bin/env python
# coding: utf-8

import shutil

"""
shutil模块提供了多个高级别文件和文件集合的操作方法,特别是复制和删除.需要注意的是shutil.copy()和shutil.copy2()都不支持文件元数据的复制.

shutil.copyfileobj(fsrc, fdst[, length])
复制文件对象fsrc的内容到fdst文件对象,length用于指定缓冲区大小,如果为负数时,表示数据不经过chunks中转,为了内存开销的不可控,文件的数据会先
读取到chunks,再从chunks复制到目标.注意,如果fsrc对象的游标位置不在位置0,则只会复制游标位置到文件结束的内容.

shutil.copyfile(src, dst)
复制src文件名的(不包含元数据)内容到dst文件名.dst必须是完整的目标文件名;与shutil.copy()可以接收一个目录为目标不同.如果源和目标是相同的文
件,则抛出异常.目标路径必须可写,否则抛出IOError异常.如果目标文件已经存在,将会被替换. 不支持设备,管道这些特殊文件的复制.

shutil.copymode(src, dst)
复制源文件的权限位到目标文件,文件内容,属主,属组这些不受影响.

shutil.copystat(src, dst)
复制源文件的权限位,最后访问时间,修改时间和flags到目标文件.文件内容,属主,属组不受影响.

shutil.copy(src, dst)
复制源文件到目标,目标可以为文件或目录,如果目标为目录,则目标文件basename与源文件一样.权限位也会复制

shutil.copy2(src, dst)
与shutil.copy()类似,但会连元数据也一起复制,实际上只是在shutil.copy()后调用copystat().这跟unix下的cp -p类似

shutil.ignore_patterns(*patterns)
这个工厂函数可以作为copytree()函数的ignore参数进行回调,对于匹配任何一个使用通配符风格的patterns的文件都忽略

shutil.copytree(src, dst, symlinks=False, ignore=None)
递归复制src目录到目标dst,dst必须不存在.如果dst父目录缺失会自动创建.权限位和时间会使用copystat()复制, 单独文件使用shutils.copy2().如果
symlinks为true,源目录的符号连接文件在目标也会呈现为符号连接文件,如果为false或缺省,则会对源中的符号链接进行跟踪.如果给定ignore参数,
ignore参数引用的对象必须可调用,它能接收copytree()访问到的目录和它的内容(os.listdir()的返回).由于copytree()是递归调用的,可调用的
ignore对象在每个递归目录中都会调用一次.ignore对象调用完毕后返回一个相对于当前目录的目录和文件名的序列,序列中的文件或目录在复制过程中
将会被忽略.ignore_patterns()工厂函数已经提供了ignore对象的实现.以下是copytree()的实现:

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

shutil.rmtree(path[, ignore_errors[, onerror]])
递归删除目录树;path必须指定为一个目录(不能是目录的符号连接).如果ignore_errors为true,将忽略错误,ignore_errors为false或缺省时,错误将交
给onerror参数引用错误处理函数处理.其中onerror必须能接收function,path,excinfo三个参数.第一个参数function,是一个抛出异常的函数对象.第
二个参数是传递给function的路径名称.第三个参数是sys.exc_info()返回的异常信息

shutil.move(src, dst)
递归地移动文件或目录(src)到其他路径(dst).如果dst是一个存在的目录,src将移动到该目录底下.如果dst存在且不是一个目录,它可能会被重写,这个依赖
于os.rename().如果dst是位于当前文件系统上,将会使用os.rename(). 否则,src会使用shutil.copy2()复制到dst,然后src被删除

exception shutil.Error
这个exception收集了文件复制过程中的所有异常

下面是一些使用例子:
复制过程中忽略所有.pyc后缀的文件以及tmp开头的文件和目录
from shutil import copytree, ignore_patterns
copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))

使用ignore参数来添加日志记录
from shutil import copytree
import logging

def _logpath(path, names):
    logging.info('Working in %s' % path)
    return []   # nothing will be ignored

copytree(source, destination, ignore=_logpath)

利用shutil对文件进行归档压缩操作
shutil还能提供文件压缩,归档的能力.这些依赖于zipfile和tarfile模块
shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])
创建归档文件(如zip或tar)并返回它的文件名称.
base_name  包含路径的归档文件名称
format: 归档格式,包括:"zip","tar","bztar","gztar".
root_dir 指定对哪个目录下的内容进行归档,相当于chdir()到该目录,然后再归档他的内容,默认为当前目录
base_dir 指定从哪一级目录开始归档,默认为当前目录
owner,group  使用哪个用户和组创建归档文件,默认使用当前用户和组
shutil.get_archive_formats()
返回支持的归档格式: (name, description)的元组
下面是使用例子:
>>> from shutil import make_archive
>>> import os
>>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
>>> root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
>>> make_archive(archive_name, 'gztar', root_dir)

'/Users/tarek/myarchive.tar.gz'
The resulting archive contains:
$ tar -tzvf /Users/tarek/myarchive.tar.gz
drwx------ tarek/staff       0 2010-02-01 16:23:40 ./
-rw-r--r-- tarek/staff     609 2008-06-09 13:26:54 ./authorized_keys
-rwxr-xr-x tarek/staff      65 2008-06-09 13:26:54 ./config
-rwx------ tarek/staff     668 2008-06-09 13:26:54 ./id_dsa
-rwxr-xr-x tarek/staff     609 2008-06-09 13:26:54 ./id_dsa.pub
-rw------- tarek/staff    1675 2008-06-09 13:26:54 ./id_rsa
-rw-r--r-- tarek/staff     397 2008-06-09 13:26:54 ./id_rsa.pub
-rw-r--r-- tarek/staff   37192 2010-02-06 18:23:10 ./known_hosts


"""
