from __future__ import unicode_literals, print_function
from db import *
import random
from pathlib import Path
import random
import json
import spacy
from spacy.gold import GoldParse
from spacy.tagger import Tagger
from datetime import datetime
from new_skills_classify import *
from word2vec_skills import *
def train_ner(nlp, train_data, output_dir,drop_ratio):
    # Add new words to vocab
    for raw_text, _ in train_data:
        #print(raw_text,_)
        doc = nlp.make_doc(raw_text)
        for word in doc:
            _ = nlp.vocab[word.orth]
    random.seed(0)
    print(len(train_data))
    # You may need to change the learning rate. It's generally difficult to
    # guess what rate you should set, especially when you have limited data.
    nlp.entity.model.learn_rate = 0.001
    for itn in range(100):
        start=datetime.now()
        print(start)
        random.shuffle(train_data)
        loss = 0.
        for raw_text, entity_offsets in train_data:
            doc = nlp.make_doc(raw_text)
            gold = GoldParse(doc, entities=entity_offsets)
            nlp.tagger(doc)
            # As drop ratio tends to 0, all words in the corpus became that tag
            loss += nlp.entity.update(doc, gold, drop=float(drop_ratio))
        print(datetime.now()-start,itn)
        if loss == 0:
            break
    #end of training
    nlp.end_training()
    if output_dir:
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.save_to_directory(output_dir)
def train_data_preparation():
    count=0
    l = revised_train_data_job_information.find({})
    train_data1=[]
    train_data2=[]
    t=revised_test_data_job_information.find({})

    for i in l:
        if count %1000==0:
            print("train_data:",count)
        train_data1.append(i["preprocessed_data"])
        train_data2.append(i["hard_train_entities"])
        count+=1
    for i in t:
        if count==60000:
            break
        if count %1000==0:
            print("train_data:",count)
        train_data1.append(i["train_data"][0])
        train_data2.append(i["hard_train_entities"])
        count+=1

    train_data = zip(train_data1,train_data2)
    print("prepared train_data",len(train_data),len(train_data1))

    return train_data,train_data1

def build_ner_model(model_name, output_directory=None,drop_ratio=None):
    print("Loading initial model", model_name)
    nlp = spacy.load(model_name)
    if output_directory is not None:
        output_directory = Path(output_directory)
    print("started train data preparation")
    train_data,test_data=train_data_preparation()
    nlp.entity.add_label('TECHNICAL_SKILL')
    train_ner(nlp, train_data, output_directory,drop_ratio)
    test_ner(test_data,output_directory,drop_ratio)
    #classify_new_skills(drop_ratio)


def test_ner(test_data,output_directory,drop_ratio):
    i=0
    if output_directory:
        print("Loading from", output_directory)
        nlp2 = spacy.load('en', path=output_directory)
        nlp2.entity.add_label('TECHNICAL_SKILL')
        output_test_data=[]
        for data in test_data:
            doc2 = nlp2(data)
            if i%100==0:
                print("count:",i)
            i+=1
            for ent in doc2.ents:
                revised_skills_extracted.insert_one({"skill_name":ent.text})

    skills = skillsets_coll.find({"skill_type":"specific"})
    for skill in skills:
        revised_skills_extracted.insert_one({"skill_name": str(skill["name"]).lower()})


if __name__ == '__main__':
    import plac
    plac.call(build_ner_model)