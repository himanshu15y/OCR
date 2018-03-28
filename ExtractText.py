import sys
import webbrowser
import time
from PIL import Image
print(time.time())
from pytesseract import image_to_string
def filterFunc(s1):
	if len(s1)<2 or s1.strip()==("ELIMINATED"):
		return False
	else:
		return True;
imagepath=sys.argv[1]
numOfLines=int(sys.argv[2])
im=Image.open(imagepath)
print "path=",imagepath
print(im)
parsedString=image_to_string(im)
print("result from teserract",parsedString)
parsedStrArray=parsedString.split("\n")
print "parsed Array",parsedStrArray
parsedStrArray=filter(filterFunc,parsedStrArray)
print "Filtered Array",parsedStrArray
print("st index--",1,"end index--",(1+numOfLines))
outString=" ".join(parsedStrArray[1:1+numOfLines])
firstOption=" ".join(parsedStrArray[1:2+numOfLines])
secondOption=" ".join(parsedStrArray[1:1+numOfLines])+""+parsedStrArray[2+numOfLines]
thirdOption=" ".join(parsedStrArray[1:1+numOfLines])+""+parsedStrArray[3+numOfLines]
import re, string;
print("regex--",re.sub(r'[^\x00-\x7f]', r' ',outString))
outString=re.sub(r'[^\x00-\x7f]', r' ',outString)
firstOption=re.sub(r'[^\x00-\x7f]', r' ',firstOption)
secondOption=re.sub(r'[^\x00-\x7f]', r' ',secondOption)
thirdOption=re.sub(r'[^\x00-\x7f]', r' ',thirdOption)
print("Que is",outString)
print("1st option",firstOption)
print("2nd option",secondOption)
print("3rd option",thirdOption)
print(time.time())
webbrowser.open("https://www.google.co.in/search?q={}".format(outString))
webbrowser.open("https://www.google.co.in/search?q={}".format(firstOption))
webbrowser.open("https://www.google.co.in/search?q={}".format(secondOption))
webbrowser.open("https://www.google.co.in/search?q={}".format(thirdOption))
exit(0)
