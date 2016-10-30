from sys import argv
import os;
home_dir = '/Users/Dave/GitHub/Scripts/Python/exp/testDir'


mylist = open("output.txt", 'r')
for folder in mylist:
	folder = folder.strip()
	newFolder = home_dir+'/'+folder
	print "Folder name " +newFolder
	if not os.path.exists(newFolder):
		os.makedirs(str(newFolder))
		os.chdir(newFolder)
mylist.close()