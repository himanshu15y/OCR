import sys
import webbrowser
import os
import time
from PIL import Image
import re, string;
from pytesseract import image_to_string
import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
partialMatch=0
perfectMatch=0
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKRED = '\033[1;31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = "\033[0;0m"
class locationOfText:
    '''1line,1lineElim,'''
    posAr=[[400,1500,150,900]]

def filterFunc(s1):
    if len(s1) < 2 or s1.strip() in ("ELIMINATED"):
        return False
    else:
        return True;
def preprocess_Image(imagepath):
    image=cv2.imread(imagepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    grayFileName = "temp_file.jpg"
    cv2.imwrite(grayFileName, gray)
    return grayFileName

def getString(tesseractOutput,st_ind,end_ind):
    #print "Finding Question"
    parsedStrArray = tesseractOutput.split("\n")
    parsedStrArray = filter(filterFunc, parsedStrArray)
    print "filtered parsedStrArray",parsedStrArray
    outString = " ".join(parsedStrArray[st_ind:end_ind])
    outString = re.sub(r'[^\x00-\x7f]', r' ', outString)
    outString = re.sub(r'[^\s\w]|_+', ' ',outString).strip()
    return outString
def tesseractOutput(imagepath):
    im = Image.open(imagepath)
    # print "path=", imagepath
    tesseractOutput = image_to_string(im)
    return tesseractOutput

def findText(imagepath, numOfLines):
    atime = time.time()
    print(atime)
    # im = Image.open(imagepath)
    resultFromTesseract=tesseractOutput(imagepath)
    print "output of ques Tess",resultFromTesseract.split("\n")
    ques=getString(resultFromTesseract,1,1+numOfLines)
    print "Question is ",ques
    print "path=", imagepath
    # print(im)
    image = cv2.imread(imagepath)
    # crop_img = img[y:y+h, x:x+w]
    # print image.shape
    y = locationOfText.posAr[0][0]
    z = locationOfText.posAr[0][1]
    a = locationOfText.posAr[0][2]
    b = locationOfText.posAr[0][3]
    crop_img = image[y:z, a:b]
    CroppedFileName = "Cropped_temp_file.jpg"
    cv2.imwrite(CroppedFileName, crop_img)
    #cv2.imshow("cropped", crop_img)
    croppedFileTessOutput=tesseractOutput(CroppedFileName)
    print "CroppedFileTessOutput",croppedFileTessOutput.split("\n")
    #cv2.waitKey(0)
    print "Options are:-"
    firstOption=getString(croppedFileTessOutput,numOfLines,numOfLines+1)
    print "1--",firstOption
    secondOption=getString(croppedFileTessOutput,numOfLines+1,numOfLines+2)
    print "2--",secondOption
    thirdOption=getString(croppedFileTessOutput,numOfLines+2,numOfLines+3)
    print "3--",thirdOption
    '''firstOption = re.sub(r'[^\x00-\x7f]', r' ', firstOption)
    firstOption = re.sub(r'[^\s\w]|_+', '',firstOption).strip()
    secondOption=re.sub(r'[^\x00-\x7f]', r' ',secondOption)
    secondOption = re.sub(r'[^\s\w]|_+', r' ', secondOption).strip()
    thirdOption=re.sub(r'[^\x00-\x7f]', r' ',thirdOption)
    thirdOption = re.sub(r'[^\s\w]|_+', r' ', thirdOption).strip()'''
    url = "https://www.google.co.in/search?q={}".format(ques)
    btime = time.time()
    print "time taken to extract--",btime-atime
    searchText(url, [firstOption,secondOption,thirdOption])
    #searchText(url, secondOption)
    #searchText(url, thirdOption)
    '''parsedString = image_to_string(im)
    print("result from normal image teserract", parsedString)
    grayFileName = preprocess_Image(CroppedFileName)
    imGray = Image.open(grayFileName)
    parsedStringGray = image_to_string(imGray)
    print("result from grey image teserract", parsedStringGray)
    imCropped = Image.open(CroppedFileName)
    parsedStringCropped = image_to_string(imCropped)
    getString(CroppedFileName,0,1)
    print("result from Cropped image teserract", parsedStringCropped)
    parsedStrArray = parsedString.split("\n")
    # print "parsed Array", parsedStrArray
    parsedStrArray = filter(filterFunc, parsedStrArray)
    # print "Filtered Array", parsedStrArray
    # print("st index--", 1, "end index--", (1 + numOfLines))
    outString = " ".join(parsedStrArray[1:1 + numOfLines])
    firstOption = " ".join(parsedStrArray[1:2 + numOfLines])
    # secondOption=" ".join(parsedStrArray[1:1+numOfLines])+""+parsedStrArray[2+numOfLines]
    # thirdOption=" ".join(parsedStrArray[1:1+numOfLines])+""+parsedStrArray[3+numOfLines]
    # print("regex--", re.sub(r'[^\x00-\x7f]', r' ', outString))
    outString = re.sub(r'[^\x00-\x7f]', r' ', outString)
    firstOption = re.sub(r'[^\x00-\x7f]', r' ', firstOption)
    # secondOption=re.sub(r'[^\x00-\x7f]', r' ',secondOption)
    # thirdOption=re.sub(r'[^\x00-\x7f]', r' ',thirdOption)
    # print("Que is", outString)
    # print("1st option",firstOption)
    # print("2nd option",secondOption)
    # print("3rd option",thirdOption)
    print(btime - a)
    outString = "What kind of creature is a Bombay Duck?"
    url = "https://www.google.co.in/search?q={}".format(outString)
    '''
    # searchText(url, "duck fish")
    # searchText(url,secondOption)
    # searchText(url,thirdOption)
    # webbrowser.open("https://www.google.co.in/search?q={}".format(outString))
    # webbrowser.open("https://www.google.co.in/search?q={}".format(firstOption))
    # webbrowser.open("https://www.google.co.in/search?q={}".format(secondOption))
    # webbrowser.open("https://www.google.co.in/search?q={}".format(thirdOption))
    # exit(0)
    # try:
    #     os.remove(CroppedFileName)
    # except:
    #     print "unable to delete"
    ctime = time.time()
    print "Search Time ",ctime-btime
    print "total time ",ctime-atime


perfectMatches=[""]
partialMatches=[""]
def find_text(lines, words):
    global perfectMatch
    global partialMatch
    global perfectMatches
    global partialMatches
    # print "finding line",words
    z=0
    words = str(words).split(" ")
    len1=len(words)

    for line in re.split(r"\.|\?|\!", lines):
        bool1=False
        line = line.lower()
        line = re.sub(r'[^\x00-\x7f]', r' ',line)
        m=0
        for word in words:
            word=word.lower()
            #print("word is",word)
            if word in line:
                m+=1
                bool1=True
                temp=word
        if bool1:
            if m==len1:
                perfectMatch+=1
                perfectMatches.append(line.replace("\n"," "))
                #print "perfectMatch--",line.replace("<br>"," ").replace("\n"," ")
                # print "perfectMatches--",perfectMatches
            else:
                partialMatch+=1
                partialMatches.append(line.replace("\n", " "))
                # print "partialMatch--", line.replace("<br>"," ").replace("\n"," ")
        if perfectMatch>1:
            break
        elif partialMatch>2:
            break
def searchText(url, keywords):
    global perfectMatch
    global partialMatch
    global perfectMatches
    global partialMatches
    # print "url,keyword"
    # print url, " and ", keywords
    partialMatchbool = False
    perfectMatchbool = False
    z = 0
    page1 = requests.get(url)
    # print page1.status_code
    soup1 = bs(page1.content, 'html.parser')
    badges = soup1.find_all('div')  # ,attrs={'class':"s"})#, attrs={'class': "f hJND5c TbwUpd"})
    # print(badges)
    # span=badges.find_all('span',class_="st")
    # print(span)
    m=0
    output=[]
    for keyword in keywords:
        perfectMatch=0
        partialMatch=0
        if m==0:
            color=bcolors.HEADER
        elif m==1:
            color=bcolors.OKGREEN
        elif m==2:
            color=bcolors.OKBLUE
        print "color is ",m
        m+=1
        partialMatches=[]
        perfectMatches=[]
        for div1 in badges:
            for span in div1.find_all('span', class_="st"):  # , recursive=False):
                # print "inside loop",span
                # cv2.waitKey(0)
                # print "span text",span.gettext
                if span is not None:
                    find_text(str(span), keyword)
                if perfectMatch>2:
                    break;
            if perfectMatch > 2:
                break;
        if len(perfectMatches)>0:
            print "answer is",color+keyword+bcolors.RESET
            for perfectMatch1 in perfectMatches:
                temp=str(perfectMatch1)
                for word in str(keyword).split(" "):
                    temp=temp.replace(word.lower(),color+word.lower()+bcolors.RESET)
                print temp
	    output.append("answer is "+color+keyword+bcolors.RESET)
        elif len(partialMatches) > 0:
            print "answer may be",bcolors.UNDERLINE+keyword+bcolors.RESET
            for partialMatch1 in partialMatches:
                temp=str(partialMatch1)
                for word in str(keyword).split(" "):
                    temp=temp.replace(word.lower(),color+word.lower()+bcolors.RESET)
                print temp
	    output.append("answer may be "+bcolors.WARNING+bcolors.UNDERLINE+keyword+bcolors.RESET)
                #if keyword.lower() in str(span).lower():
                #    z += 1
                    # print(z,"--",span)
	for answer in output:
		print answer
    '''for div in soup.body.find_all('div', attrs={'class': 'badges'})
    # print soup1.find_all('a')[0:2]
    for para in soup1.find_all('span',class_="st"):
        print z,para.get_text
        z+=1
        for line in re.split(r"\.|\?|\!|\, ",para.get_text()):
            #print "here",song.get_text()
            if (keyword in line):
                #print song['href']
                print line
'''
imagepath=sys.argv[1]
numOfLines=int(sys.argv[2])
findText(imagepath, numOfLines)

