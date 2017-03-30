from sys import argv
import os;
home_dir = '/Users/Dave/github/movies'


mylist = open("/Users/Dave/Desktop/new.txt", 'r')
for folder in mylist:
	folder = folder.strip()
	newFolder = home_dir+'/'+folder
	print "Folder name " +newFolder
	if not os.path.exists(newFolder):
		os.makedirs(str(newFolder))
		os.chdir(newFolder)
mylist.close()