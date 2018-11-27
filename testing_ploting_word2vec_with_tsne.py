from gensim.models import Word2Vec
from db import *
import re
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
def add_phrases():
    l = skills_extracted_ner.distinct("skill_name")
    list1 = []
    for i in l:
        lk = i.lower().split()
        lk="_".join(lk)
        if lk not in list1:
            list1.append(lk)
            #print(lk)
    l = skills_extracted_ner1.distinct("skill_name")
    for i in l:
        lk = i.lower().split()
        lk="_".join(lk)
        if lk not in list1:
            list1.append(lk)
    l=master_n_grams.distinct("n_grams")
    for i in l:
        list1.append(i)
    l = master_n_grams1.distinct("n_grams")
    for i in l:
        list1.append(i)
    l = master_n_grams2.distinct("n_grams")
    for i in l:
        list1.append(i)
            #print(lk)
    #list1.append("ruby")
    return list1

model=Word2Vec.load("word2vec_75000_jobs_min_count_3.model")
#model=Word2Vec.load("updates_word2vec_skills_model_20000_space.model")
print(model)
l=list(model.wv.vocab)
print("list:", l)
#print(model.similarity('python', 'java'))
print (model.most_similar("business_administrator"))
print (model.most_similar("customer_service"))
j=model.most_similar("data_science")
k=model.most_similar("project_quality_specialist")
l=model.most_similar("business_administrator")
vocab=[]
vocab.append("product_manager")
for i in model.most_similar("product_manager"):
    vocab.append(i[0])
    #vocab.append("product_manager")
'''
vocab.append("data_science")
for i in j:
    vocab.append(i[0])
'''
'''
vocab.append("business_administrator")
for i in l:
    vocab.append(i[0])
'''
'''
vocab.append("project_quality_specialist")
for i in k:
    vocab.append(i[0])
'''
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
X=model[vocab]
tsne_model=TSNE()
#tsne_model = TSNE(perplexity=50,learning_rate=500.0, n_components=2, init='pca', n_iter=4000, random_state=None)
new_values= tsne_model.fit_transform(X)

x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

plt.figure(figsize=(16, 16))
for i in range(len(x)):
    plt.scatter(x[i], y[i])
    plt.annotate(vocab[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
plt.show()
