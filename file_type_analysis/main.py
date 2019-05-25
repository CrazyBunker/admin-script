import yaml, os, re, sys

class analysis_file():
    def __iter__(self):
        return self
    def __init__(self,file):
        with open(file) as f:
            self.params = yaml.safe_load(f)
        self.counter = 0
    def next(self):
        if self.counter < len(self.params):
            i = list(self.params)[self.counter]
            self.indexfile = self.params[i]['index']
            self.map = self.params[i]['map']
            self.unpack_map = self.__construct_filename__()
            self.type_file = self.params[i]['type_file']
            self.dir = self.params[i]['dir']
            self.counter += 1
            return 1
        else:
            raise StopIteration

    def read_extensions(self):
        a = dict()
        max = self.count_lines(self.indexfile)
        with open(self.indexfile,'r') as indefile:
            count = 0
            for line in indefile:

                string = line.split(";")
                ext = re.match(r'.*\.(.*)\"$', string[self.unpack_map['orig']]).groups(1)[0]
                path = '/'.join([self.dir] + [string[i] for i in self.unpack_map['path']] + \
                                [string[self.unpack_map['filename']].replace('"','')+'.'+self.type_file])
                if os.path.isfile(path):
                    if not ext in a:
                        a[ext] = 0
                    else:
                        a[ext] += os.path.getsize(path)
                self.progress(count, max)
                count += 1


        return a
    def __construct_filename__(self):
        path = sorted([ i for i in range(len(self.map)) if 'path' in self.map[i] ])
        filename = self.map.index('file')
        orig = self.map.index('orig')
        return {"path": path, "filename":filename, "orig": orig }

    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    def count_lines(self, filename, chunk_size=1 << 13):
        with open(filename) as file:
            return sum(chunk.count('\n') for chunk in iter(lambda: file.read(chunk_size), ''))
    def progress(self,i,max):
        i = int(100/max * i)
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-100s] %d%%" % ('=' * i, i))
        if i >= 90:
            sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == "__main__":
    a = analysis_file(os.path.join(os.path.dirname(__file__),'config.yaml'))
    for i in a:
        extension = a.read_extensions()
        for ext in extension:
            print("%s: %s"%(ext,a.convert_bytes(extension[ext])))
