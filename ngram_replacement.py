from db import *
docs=[]
count=0
try:
    unicode
except:
    unicode = str
train_data = student_resumes.find({})
n_grams=master_n_grams.find({})

#setting the occurence of n_grams as 3, reduces the noise
n_gram=[]
for i in n_grams:
    if int(i["count"])>=3:
        l=[int(i["count"]),i["n_grams"]]
        if l not in n_gram:
            n_gram.append(l)
n_gram.sort(reverse=True)

###sorting from seven_grams to one gram
final_gram=[]
for i in range(0,len(n_gram)):
    l=n_gram[i][1].count("_")
    k=n_gram[i][1]
    final_gram.append([l,k])
final_gram.sort(reverse=True)

#updating the preprocessed data to n_gram descrption
for data in train_data:
    job=data["preprocessed"]
    job_gram=[]
    for i in range(0,len(final_gram)):
        split_space=final_gram[i][1].split("_")
        join_split=" ".join(split_space)
        job=job.replace(join_split,final_gram[i][1])
        if job.count(final_gram[i][1])>=1:
            job_gram.append(final_gram[i][1])
    student_resumes.update_one({"_id": data["_id"]}, {"$set": {"n_grams": job_gram,"ngram_descrption":job}})
    if count%1000==0:
        print(count)
    count+=1