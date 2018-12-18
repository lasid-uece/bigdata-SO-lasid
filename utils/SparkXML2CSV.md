# Script to convert XML files to Spark CSV 

## Introduction

This script convert XML files provided by Stack Overflow to CSV to use in Apache Spark environment. This XML format has the rows marked as *<row  parameter1=xxx parameter2=yyy >*. As the collumn field is a attribute most of XML parsers can't read correct. 

This script needs to load all file in RAM memory and it is necessary to split the XML files to maximum length. Fo lasid50, lasid60 and lasid70 servers the max file length is almost 7.2GB. For others, the max value should be tested.

## Procedure

In this example, the Posts.xml file is used.

1. Split the big XML dataset file in 7.2GB blocks. Take a long time, so, nohup is usefull. The split length is set to MBs, then 7.2GB = 7200 MB.
```
$ nohup split -C 7200m Posts.xml &
```
Split cut the file at the end of each line (after LF). It creates files with 7.2GB lenghth named: xaa, xab, xac, xad,....

2. The sparkxml2csv script need a correct XML file, with root tag. After split, it is necessary to include the absent tags.
Check the correct tag in first file.

The first file is OK, then, from the second to the last file, xab, xac,... Take a long time, so, nohup is usefull.
```
$ nohup sed -i '1i<posts>\' xab &
```
The last file has the closing tag OK, then from first to last but one file, xaa, xab,... It is fast, nohup isn't necessary.
```
$ echo '</posts>' >> xaa
```
3. Now, star the conversion. Take a long time, so, nohup is usefull.  Set the correct file name (without xml extension).
 ```  
$ nohup ./sparkxml2csv.py Posts xaa &
```
The new CSV file is xaa.csv

4. Finally, join all csv parts in one big file:
```
$ cat xaa.csv xab.csv xac.csv xad.csv xae.csv xaf.csv xag.csv xah.csv xai.csv > Posts.csv
```

The converted csv file is ready.
