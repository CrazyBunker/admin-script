import yaml, os
from ftplib import FTP
import platform, time

class download_from_ftp():

    def __init__(self, file):
        with open(file) as f:
            self.params = yaml.safe_load(f)
    def __connect_to_ftp__(self):
            self.ftp = FTP(self.addr)
            self.ftp.login(self.user, self.password)
            self.ftp.cwd(self.source)
    def __listFilesOnDst__(self):
        from os import walk
        f = []
        for (dirpath, dirnames, filenames) in walk(self.destination):
            f.extend(filenames)
            break
        return f

    def __getArchiveList__(self):
        listFilesOnFtp = self.ftp.nlst()[2:-1]
        listSub = list(set(listFilesOnFtp) - set(self.__listFilesOnDst__()))
        return listSub

    def __getArchives__(self):
        archive_list = self.__getArchiveList__()
        for archive in archive_list:
            local_filename = os.path.join(self.destination, archive)
            with open(local_filename, "wb") as lf:
                self.ftp.retrbinary("RETR " + archive, lf.write, 8 * 1024)
        return archive_list

    def download_archive(self):
        archive_list = []
        for server in self.params:
            self.addr = self.params[server]['address']
            self.user= self.params[server]['username']
            self.password = self.params[server]['password']
            self.source = self.params[server]['sources']
            self.destination = self.params[server]['destination']
            self.days = self.params[server]['days']
            self.__connect_to_ftp__()
            archive_list+= self.__getArchives__()
            self.removeOldArchive(self.destination, self.days)
        return archive_list

    def secondInDay(self,days):
        return 60 * 60 * 24 * days

    def creation_date(self, path_to_file):
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

    def removeOldArchive(self, destination, days):
        for file in self.__listFilesOnDst__():
             local_filename = os.path.join(destination, file)
             timestamp_to_deleted = self.secondInDay(days) + self.creation_date(local_filename)
             if timestamp_to_deleted <= time.time():
                 os.remove(local_filename)

if __name__ == "__main__":
    archives = download_from_ftp(os.path.join(os.path.dirname(__file__),'config.yaml'))
    list_archive = archives.download_archive()
    if not list_archive:
        print("No archives to download")
    else:
        print("Archives to download:")
        for list in list_archive:
            print(list)









