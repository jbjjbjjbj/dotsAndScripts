import sys
import os



with open('copyStuff.txt') as f:
	for line in f:
		stuff = line.replace('\n', '').split(' ')
		if(stuff[0] != "" and stuff[1] != ""):
			if(sys.argv[1] == 'in'):
				os.system("rm -r -v " + stuff[1])
				if(os.path.isdir(os.path.abspath(stuff[0]))):
					os.system("mkdir " + stuff[1])
					os.system("cp -r -v " + stuff[0] + "/* " + stuff[1])
				else:
					os.system("cp -v " + stuff[0] + " " + stuff[1])

			elif(sys.argv[1] == 'out'):
				os.system("rm -r -v " + stuff[0] + ".bak")
				os.system("mv -v " + stuff[0] + " " + stuff[0] + ".bak")
				if(os.path.isdir(os.path.abspath(stuff[1]))):
					os.system("mkdir " + stuff[0])
					os.system("cp -r -v " + stuff[1] + "/* " + stuff[0])
				else:
					os.system("cp -v " + stuff[1] + " " + stuff[0])


if(sys.argv[1] == "commit"):
	os.system("git add *")
	os.system("git status")
	msg = input("Commit message: ")
	os.system("git commit -m '" + msg + "'")
	os.system("git pull")
	os.system("git push")

