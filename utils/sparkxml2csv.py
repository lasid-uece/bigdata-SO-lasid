#!/usr/bin/python3
#
# Script to convert XML files to Spark CSV 
# This script need to load al file in memory. For lasid50, lasid60 and lasid70 servers the max file length is almost 7.2GB
# Procedure:
#
# 1) Split the big dataset file in 7.2GB blocks. Take a long time, so, nohup is usefull. Posts.xml is a example.
#   $ nohup split -C 7200m Posts.xml &
# Split cut the file at the end of each line (after LF). It creates files with 7.2GB lenghth named: xaa, xab, xac, xad,....
#
# 2) The sparkxml2csv script need a correct XML file, with root tag. After split, it is necessary to include the absent tags.
# Check the correct tag in first file.
# The first file is OK, then, from the second to the last file, xab, xac,... Take a long time, so, nohup is usefull.
#   $ nohup sed -i '1i<posts>\' xab &
# The last file has the closing tag OK, then from first to last but one file, xaa, xab,... It is fast, nohup isn't necessary.
#   $ echo '</posts>' >> xaa
#
# 3) Now, star the conversion. Take a long time, so, nohup is usefull.
#   $ nohup ./sparkxml2csv.py Posts xaa &
# The new CSV file is xaa.csv
#
# 4) Finally, join all csv files:
#   $ cat xaa.csv xab.csv xac.csv xad.csv xae.csv xaf.csv xag.csv xah.csv xai.csv > Posts.csv
# The converted csv file is ready.

from lxml import etree
import csv
import sys
import os.path

file_name = sys.argv[1]
temp_file = sys.argv[2]

xml_fname = temp_file
csv_fname = temp_file+".csv"

if not os.path.exists(xml_fname):
    print("There is no "+xml_fname+" file")
    sys.exit()

if file_name == "Badges":		# Badges.xml
	fields = ["Id","UserId","Name","Date","Class","TagBased"]
elif file_name == "Comments":		# Comments.xml
	fields = ["Id","PostId","Score","Text","CreationDate","UserDisplayName","UserId"]
elif file_name == "PostHistory":	# PostHistory.xml
	fields = ["Id","PostHistoryTypeId","PostId","RevisionGUID","CreationDate","UserId","UserDisplayName","Comment","Text"]
elif file_name == "PostLinks":		# PostLinks.xml
	fields = ["Id","CreationDate","PostId","RelatedPostId","LinkTypeId"]
elif file_name == "Posts":		# Posts.xml
	fields = ["Id","PostTypeId","AcceptedAnswerId","ParentId","CreationDate","Score","ViewCount","Body","OwnerUserId","OwnerDisplayName","LastEditorUserId","LastEditorDisplayName","LastEditDate","LastActivityDate","Title","Tag","AnswerCount","CommentCount","FavoriteCount"]
elif file_name == "Tags":		# Tags.xml
	fields = ["Id","TagName","Count","ExcerptPostId","WikiPostId"]
elif file_name == "Users":		# Users.xml
	fields = ["Id","Reputation","CreationDate","DisplayName","LastAccessDate","WebsiteUrl","Location","ProfileImageUrl","AboutMe","Views","UpVotes","DownVotes","Age","AccountId","EmailHash"]
elif file_name == "Votes":		# Votes.xml
	fields = ["Id","PostId","VoteTypeId","UserId","CreationDate","BountyAmount"]
else:
    print("There is no "+file_name+" parameters available")
    sys.exit()

# 

csv.register_dialect('csvSpark', delimiter=',', lineterminator='\n', escapechar='\\', quoting=csv.QUOTE_MINIMAL)

xml = etree.parse(xml_fname)

with open(csv_fname, "w") as f:
    writer = csv.DictWriter(f, fields, dialect='csvSpark', extrasaction="ignore")
    if temp_file == "xaa":    # Only first temp file should have the csv header
        writer.writeheader()
    for node in xml.iter("row"):
        writer.writerow(node.attrib)
