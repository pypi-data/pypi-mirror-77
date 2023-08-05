#!/usr/bin/python
# coding:utf-8
try:
    import subprocess
    import zipfile
    import platform
    import os
except Exception as err:
    from core.exception import AwdExceptions
    raise AwdExceptions(str(err))



class ZipObj():

    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path
        if os.path.exists(self.dst_path):
            os.remove(self.dst_path)

    def enCrypt(self, passwd='123456', nopass=False, deleteSource=False):
        """
	        压缩加密，并删除原数据, window系统调用rar程序, 默认不删除原文件
            linux等其他系统调用内置命令 zip -P123 tar self.src_path
        """

        if platform.system() == "Windows":
            cmd = ['rar', 'a', '-p%s' % passwd, self.dst_path, self.src_path]
            if nopass:
                del cmd[2]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable=r'C:\Program Files\WinRAR\WinRAR.exe')
            p.wait()

            if os.path.exists(self.dst_path):
                return True

            cmd = ['7z', 'a', '-p%s' % passwd, '-y', self.dst_path, self.src_path]

            if nopass:
                del cmd[2]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable=r'C:\Program Files\7-Zip\7z.exe')
            p.wait()

            if os.path.exists(self.dst_path):
                return True
            return False

        else:
            cmd = ['7z', 'a', '-p%s' % passwd, '-y', self.dst_path , self.src_path]

            if nopass:
                del cmd[2]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()

            if os.path.exists(self.dst_path):
                return True

            if os.path.isdir(self.src_path):
                os.chdir(self.src_path)
                self.src_path = './'
            else:
                fileName, filePath = os.path.basename(self.src_path),os.path.dirname(self.src_path)
                os.chdir(filePath)
                self.src_path = fileName

            cmd = ['zip', '-r', '-P %s' % passwd, self.dst_path, self.src_path]

            if nopass:
                del cmd[2]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()

            if os.path.exists(self.dst_path):
                return True
            return False

        if deleteSource:
            if os.path.isdir(self.src_path):
                os.removedirs(self.src_path)
            else:
                os.remove(self.src_path)

    # def deCrypt(self):
    #     """
    #     使用之前先创造ZipObj类
    #     解压文件
    #     """
    #     zfile = zipfile.ZipFile(self.filepathname + ".zip")
    #     zfile.extractall(r"zipdata", pwd=passwd.encode('utf-8'))

def zipEnc(src_path,dst_path='',passwd='123456',nopass=False,deleteSource=False):
    if len(dst_path) == 0:
        dst_path = src_path+'.zip'

    createZipFile = ZipObj(src_path, dst_path)
    createOk = createZipFile.enCrypt(passwd,nopass,deleteSource)
    if createOk:
        return True
    return False