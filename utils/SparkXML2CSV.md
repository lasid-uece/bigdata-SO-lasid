# Script to convert XML files to Spark CSV 

## Introduction

This script convert XML files, provided by Stack Overflow, to CSV, to be used in Apache Spark environment. This XML format has the rows marked as *<row  parameter1=xxx parameter2=yyy >*. As the collumn field is a attribute most of XML parsers can't read correct. 

This script needs to load all file in RAM memory and it is necessary to split the XML files to maximum length. Fo lasid50, lasid60 and lasid70 servers the max file length is almost 7.2GB. For others, the max value should be checked.

## Procedure

In this example, the Posts.xml file is used.

### Configure the script if needed.

The script is prepared to convert all Stack Overflow XML files. To change the parameters names that should be read, change the field list, for example:

```
if file_name == "Posts":		# Posts.xml
	fields =["Id","PostTypeId","AcceptedAnswerId","ParentId",...,"FavoriteCount"]
```

### Split the big XML file

Split the big XML dataset file in 7.2GB blocks. Take a long time, so, nohup is usefull. The split length is set to MBs, then 7.2GB = 7200 MB.
```
$ nohup split -C 7200m Posts.xml &
```
Split cut the file at the end of each line (after LF). It creates files with 7.2GB lenghth named: xaa, xab, xac, xad,....

### Complete the XML tag in splited files (parts)

The sparkxml2csv script need a correct XML file, with root tag. After split, it is necessary to include the absent tags in all files. Only the first part has the openning *<tag>* and only the last part has the closing *</tag>*.

Check the root tag in first file. In the example the root tag is *<posts>*.

The openning tag in first file is OK, then, from the second to the last file is necessary to include the *<tag>* in xab, xac,... Take a long time, so, nohup is usefull.

```
$ nohup sed -i '1i<posts>\' xab &
```

The last file has the closing tag OK, then from first to last but one file  is necessary to include the *</tag>* in xaa, xab,... It is fast, nohup isn't necessary.

```
$ echo '</posts>' >> xaa
```

### Start the conversion file by file

Now, start the conversion.  Set the correct file name (without xml extension) and the file you want to convert. Take a long time, so, nohup is usefull.

```  
$ nohup ./sparkxml2csv.py Posts xaa &
```
The new CSV file is xaa.csv

### Join all CSV files in one

Finally, join all csv parts in one big file (from xaa.csv to xaz.csv). Take a long time, so, nohup is usefull.

```
$ nohup cat xa?.csv > Posts.csv &
```

The convertion of xml to csv file is done.
