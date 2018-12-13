#!/usr/bin/python3
#
# Script to convert XML files to Spark CSV 
#
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

if file_name == "Badges":				# Badges.xml.gz
	fields = ["Id","UserId","Name","Date","Class","TagBased"]
elif file_name == "Comments":			# Comments.xml.gz
	fields = ["Id","PostId","Score","Text","CreationDate","UserDisplayName","UserId"]
elif file_name == "PostHistory":		# PostHistory.xml.gz
	fields = ["Id","PostHistoryTypeId","PostId","RevisionGUID","CreationDate","UserId","UserDisplayName","Comment","Text"]
elif file_name == "PostLinks":			# PostLinks.xml.gz
	fields = ["Id","CreationDate","PostId","RelatedPostId","LinkTypeId"]
elif file_name == "Posts":				# Posts.xml.gz
	fields = ["Id","PostTypeId","AcceptedAnswerId","ParentId","CreationDate","Score","ViewCount","Body","OwnerUserId","OwnerDisplayName","LastEditorUserId","LastEditorDisplayName","LastEditDate","LastActivityDate","Title","Tag","AnswerCount","CommentCount","FavoriteCount"]
elif file_name == "Tags":				# Tags.xml.gz
	fields = ["Id","TagName","Count","ExcerptPostId","WikiPostId"]
elif file_name == "Users":				# Users.xml.gz
	fields = ["Id","Reputation","CreationDate","DisplayName","LastAccessDate","WebsiteUrl","Location","ProfileImageUrl","AboutMe","Views","UpVotes","DownVotes","Age","AccountId","EmailHash"]
elif file_name == "Votes":				# Votes.xml.gz
	fields = ["Id","PostId","VoteTypeId","CreationDate"]
else:
    print("There is no "+file_name+" parameters available")
    sys.exit()

# 

csv.register_dialect('csvSpark', delimiter=',', lineterminator='\n', escapechar='\\', quoting=csv.QUOTE_MINIMAL)


xml = etree.parse(xml_fname)

with open(csv_fname, "w") as f:
    writer = csv.DictWriter(f, fields, dialect='csvSpark', extrasaction="ignore")
    if temp_file == "xaa":
        writer.writeheader()
    for node in xml.iter("row"):
        writer.writerow(node.attrib)
