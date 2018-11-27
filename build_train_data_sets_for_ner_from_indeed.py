from indeed import IndeedClient
from db import *
import urllib2
from bs4 import BeautifulSoup
import re
import json
client1 = IndeedClient("client number" )
from datetime import datetime
from db import *
try:
    unicode
except:
    unicode=str

def get_train_data_tuple(text, sample_entity_dict,skill_type):
    result = {'entities': []}
    for entity in sample_entity_dict:
        for token in sample_entity_dict[entity]:
            token1 = re.escape(token)
            for m in re.finditer(unicode(token1), text, re.IGNORECASE):
                result['entities'].append((m.start()+1, m.end()-1, skill_type))

    return result

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

def remove_punct(lk):
    lk1 = lk.lower().replace("\\n", " ").replace("\n", " ").replace(" n "," ")
    punctuations = '''!()-[]{};:'"\<>,=/?@$%^&*_~|'''
    lk2 = ""
    for char in lk1:
        if char not in punctuations:
            lk2 = lk2 + char
        else:
            lk2 = lk2 + " "

    lk2=lk2.replace("u201c","").replace("u201d","").replace(" i "," ").replace(" p "," ").replace("xf3n"," ").replace(" m "," ").replace(" f "," ").replace(" s "," ").replace(" n "," ").replace("u2018","").replace(" u "," ").replace("u2014","").replace("amp", "").replace("xb7", "").replace("xc2", "").replace("u2013",
                                                                                                         "").replace(
            "xe9", "").replace("u2022", "").replace("u2019", "").replace(" s ", " ").replace(" e ", " ").replace(" a ",
                                                                                                                 " ")


    return re.sub(" +", " ", lk2)


specific_skills=skillsets_coll.find({"skill_type":"specific"})
hard_skills=[]
for skill in specific_skills:
    skill_p=remove_punct(skill["name"])
    hard_skills.append(" "+skill_p+" ")


hard_entity_dict = {"skills":hard_skills}

specific_skills=skillsets_coll.find({"skill_type":"generic"})
soft_skills=[]
for skill in specific_skills:
    skill_p=remove_punct(skill["name"])
    soft_skills.append(" "+skill_p+" ")


soft_entity_dict = {"skills":soft_skills}

specific_skills=skillsets_coll.find({})

def job_extract(search_response,skill,k):
    try:
        req = urllib2.Request(str(search_response['results'][k]['url']))
        response = urllib2.urlopen(req)
        data = response.read()
        soup = BeautifulSoup(data)
        try:
            mydivs = soup.findAll("div", {"class": "jobsearch-JobComponent-description icl-u-xs-mt--md"})
            lk = striphtml(str(mydivs))
            try:
                lk2=remove_punct(lk)
                get_data = get_train_data_tuple(lk2, hard_entity_dict,"TECHNICAL_SKILL")
                get_data1 = get_train_data_tuple(lk2, soft_entity_dict,"SOFT_SKILL")

            except:
                get_data = get_train_data_tuple(lk2, hard_entity_dict,"TECHNICAL_SKILL")
                get_data1 = get_train_data_tuple(lk2, soft_entity_dict,"SOFT_SKILL")
        except:
            try:
                mydivs = soup.findAll("div")
                lk = striphtml(str(mydivs))

                try:
                    lk2 = remove_punct(lk)
                    get_data = get_train_data_tuple(lk2, hard_entity_dict, "TECHNICAL_SKILL")
                    get_data1 = get_train_data_tuple(lk2, soft_entity_dict, "SOFT_SKILL")
                except:
                    get_data = get_train_data_tuple(lk2, hard_entity_dict, "TECHNICAL_SKILL")
                    get_data1 = get_train_data_tuple(lk2, soft_entity_dict, "SOFT_SKILL")
            except:
                lk = striphtml(data)
                try:
                    lk2 = remove_punct(lk)
                    get_data = get_train_data_tuple(lk2, hard_entity_dict, "TECHNICAL_SKILL")
                    get_data1 = get_train_data_tuple(lk2, soft_entity_dict, "SOFT_SKILL")
                except:
                    get_data = get_train_data_tuple(lk2, hard_entity_dict, "TECHNICAL_SKILL")
                    get_data1 = get_train_data_tuple(lk2, soft_entity_dict, "SOFT_SKILL")


        revised_test_data_job_information.insert_one({"preprocessed_data":lk2,"url":search_response['results'][k]['url'],"skill_name":skill.lower(), "soft_train_data":get_data1,"hard_train_data":get_data,"soup_processed_data":lk.lower(),"raw_data":data.lower()})
    except:
        print ("error",k)

from multiprocessing.pool import ThreadPool as Pool
from threading import Thread
import time

i=0
technical_skills=[]
for skill in specific_skills:
    technical_skills.append(skill["name"])

def get_job_information(skill):
    skill=remove_punct(skill)
    l=revised_test_data_job_information.find_one({"skill_name":skill})
    if not l:
        try:
            start = datetime.now()

            params = {
            'l': "united states",
            'userip': "1.2.3.4",
            'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit': 25,
            'start':35
            }
            ws = skill.strip().lower().split()
            keyword = "+".join(ws)
            params['q'] = keyword

            search_response = client1.search(**params)
            pool = Pool(len(search_response['results']))
            threads=[]
            for k in range(0, len(search_response['results'])):
                t = Thread(target=job_extract, args=[search_response,skill,k])
                threads.append(t)
                t.start()


            for t in threads:
                t.join()

            end=datetime.now()
            print("time:",(end-start),"skillname:",skill,"total jobs present:",search_response['totalResults'])
        except:
            print("error", skill, len(search_response["results"]))

pool = Pool(len(technical_skills))

threads=[]
for qe in range(0, len(technical_skills)):
    try:
        t1 = Thread(target=get_job_information, args=[technical_skills[qe]])
        threads.append(t1)
        t1.start()

        #print(technical_skills[qe],qe)
        for t1 in threads:
            t1.join()
    except:
        print("error",qe,technical_skills[qe])
