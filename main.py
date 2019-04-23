import yaml, os
from ftplib import FTP, error_perm
import platform

def loadConfiguration(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    try:
        address = templates['address']
        username = templates['username']
        password = templates['password']
        src = templates['backup_src']
        dst = templates['backup_dst']

    except:
        return '','','','','',''
    else:
        return address,username,password,src,dst

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


class ftpGetFiles():
    def __init__(self, param):
        addr,user,password,self.src,self.dst = param
        self.ftp = FTP(addr)
        self.ftp.login(user,password)
        self.ftp.cwd(self.src)

    def __listFilesOnDst__(self):
        from os import walk
        f = []
        for (dirpath, dirnames, filenames) in walk(self.dst):
            f.extend(filenames)
            break
        return f

    def __getArchiveList__(self):
        listFilesOnFtp = self.ftp.nlst()[2:-1]
        listSub = list(set(listFilesOnFtp) - set(self.__listFilesOnDst__()))
        return listSub

    def getArchives(self):
        return_list = self.__getArchiveList__()
        for archive in return_list:
            local_filename = os.path.join(self.dst, archive)
            lf = open(local_filename, "wb")
            self.ftp.retrbinary("RETR " + archive, lf.write, 8 * 1024)
        return return_list
    def removeOldArchive(self):
        for file in self.__listFilesOnDst__():
             local_filename = os.path.join(self.dst, file)
             print(creation_date(local_filename))

if __name__ == "__main__":
    files = ftpGetFiles(loadConfiguration('info.yaml'))
    for log in files.getArchives():
        print(log)
    print(files.removeOldArchive())