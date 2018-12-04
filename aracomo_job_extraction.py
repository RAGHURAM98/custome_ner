from indeed import IndeedClient
from db import *
import urllib2
from bs4 import BeautifulSoup
import re
import json
import spacy

from datetime import datetime
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

def remove_punct(lk):
    lk1=[]
    for i in lk.lower().split():
        l = (i.encode("ascii", "ignore")).decode("utf-8")
        if "\\" not in l:
            lk1.append(l)
    lk1 = " ".join(lk1)
    punctuations = '''!()-[]{};:'"\<>.,=/?@$%^&*_~|'''
    lk2 = ""
    for char in lk1:
        if char not in punctuations:
            lk2 = lk2 + char
        else:
            lk2 = lk2 + " "

    return re.sub(" +", " ", lk2)

l=["https://apply.aramco.jobs/jobs/1171776?lang=en-us","https://apply.aramco.jobs/jobs/1141996?lang=en-us"]
for url in l:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    soup = BeautifulSoup(data)
    #print(soup.text)
    div1=soup.findAll("h1",{"class":"job-title"})
    divs=striphtml(str(div1))
    divs1=remove_punct(divs)
    print divs1
    div1=soup.findAll("div",{"class":"jibe-job-description job-description"})
    divs=striphtml(str(div1))
    divs=remove_punct(divs)
    #print divs
    f=open(str(divs1)+"soft_skills.txt","a")
    f1=open(str(divs1)+"technical_skills.txt","a")
    job_descrption=divs1+" "+divs


    aracomo_jobs.insert_one({
                            "job_descrption":job_descrption,
                            "job_title":divs1,
                            "url":url,
                            "raw_data":data
                            })

