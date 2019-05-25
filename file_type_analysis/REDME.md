### Description
A script for calculating the size of files with grouping by file extension, a list with a mapping is taken from a csv file with a separator;

Uses configuration file in yaml format, sample file:

~~~~~~~~
dir_for_analys1:
  index: index.txt
  map:
    - file
    - path1
    - path2
    - orig
  type_file: zip
  dir: /home/qq/tmp/store
~~~~~~~~
Used keywords:
index, map, type_file, dir

**index:** The path to the file in CVS format with a separator ";"
For example:
~~~~~~~~
"file1";5000;231;"name1.zip"
"file2";2000;2212;"name1.tar"
"file3";3000;23141;"name2.zip"
"file4";4000;2421;"name2.tar"
~~~~~~~~

**map:**: Points to a CSV structure and contains the keywords: **file**, **path**, **orig**
 * **file** - the name of the file on the disk
 * **path** - the subdirectory in which the file is located, several path values ​​are allowed, for example, path1, path2
 * **orig** - the original file name

**type_file**: File extension on the disk, if not specified in the csv \
**dir**: Path to the root directory where files are located

### The result of the team:
~~~~~~~~
[=============================================================] 100%
zip: 4.0 KB
tar: 8.0 KB
~~~~~~~~
