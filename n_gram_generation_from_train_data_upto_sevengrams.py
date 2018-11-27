from db import *
from gensim.models.phrases import Phrases, Phraser


def ngram_generation(high_count):

    docs=[]
    count=0
    train_data = revised_test_data_job_information.find({}, {"preprocessed_data": 1, "_id": 1})

    for data in train_data:
        if count>int(high_count):
            docs.append(data["preprocessed_data"].replace("u2026","").replace("e04a","").split())
        if count%5000==0:
            print(count)
        if count == int(high_count)+30000:
            break

        count+=1

    print(count)
    bigram = Phrases(docs, min_count=10, threshold=100, delimiter=b'_')
    bigrams = Phraser(bigram)
    print(count)
    trigram = Phrases(bigrams[docs], min_count=10, threshold=100, delimiter=b'_')
    trigrams = Phraser(trigram)
    print(count)
    fourgram = Phrases(trigrams[bigrams[docs]], min_count=5, threshold=100, delimiter=b'_')
    fourgrams = Phraser(fourgram)
    print(count)
    fivegram = Phrases(fourgrams[trigrams[bigrams[docs]]], min_count=5, threshold=100, delimiter=b'_')
    fivegrams = Phraser(fivegram)
    print(count)
    sixgram = Phrases(fivegrams[fourgrams[trigrams[bigrams[docs]]]], min_count=5, threshold=100, delimiter=b'_')
    sixgrams = Phraser(sixgram)
    print(count)
    sevengram = Phrases(sixgrams[fivegrams[fourgrams[trigrams[bigrams[docs]]]]], min_count=5, threshold=100, delimiter=b'_')
    sevengrams = Phraser(sevengram)

    c=0
    for sent in docs:
        if c%1000==0:
            print(c)
        c+=1

        for b in bigrams[sent]:
            if "_" in b:
                l = master_n_grams.find_one({"n_grams": b})
                if not l:
                    master_n_grams.insert_one({"n_grams": b,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": b},{"$set": {"count":str(count)}})

        for t in trigrams[bigrams[sent]]:
            if t.count("_") == 2 :
                if not l:
                    master_n_grams.insert_one({"n_grams": t,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": t},{"$set": {"count":str(count)}})

        for t in fourgrams[trigrams[bigrams[sent]]]:
            if t.count("_") == 3 :
                l = master_n_grams.find_one({"n_grams": t})
                if not l:
                    master_n_grams.insert_one({"n_grams": t,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": t},{"$set": {"count":str(count)}})

        for t in fivegrams[fourgrams[trigrams[bigrams[sent]]]]:
            if t.count("_") == 4 :
                l = master_n_grams.find_one({"n_grams": t})
                if not l:
                    master_n_grams.insert_one({"n_grams": t,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": t},{"$set": {"count":str(count)}})

        for t in sixgrams[fivegrams[fourgrams[trigrams[bigrams[sent]]]]]:
            if t.count("_") == 5 :
                l = master_n_grams.find_one({"n_grams": t})
                if not l:
                    master_n_grams.insert_one({"n_grams": t,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": t},{"$set": {"count":str(count)}})

        for t in sevengrams[sixgrams[fivegrams[fourgrams[trigrams[bigrams[sent]]]]]]:
            if t.count("_") == 6 :
                l=master_n_grams.find_one({"n_grams":t})
                if not l:
                    master_n_grams.insert_one({"n_grams": t,"count":"1"})
                if l:
                    count=int(l["count"])+1
                    master_n_grams.update_one({"n_grams": t},{"$set": {"count":str(count)}})

import plac
plac.call(ngram_generation)