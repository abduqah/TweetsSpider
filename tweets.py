import json
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
#j = json.load(open('raw_data0').read().rstrip().split('\n'))
j = []
with open('raw-data') as f:
    d = f.read().rstrip().split('\n')
    while '' in d:
        d.remove('')
    for i in d:
        j.append(json.loads(i))

print(len(j))
result = []
for item in j:
    dict = {}
    dict['T'] = item.get('created_at')
    dict['ID'] = item.get('user').get('id')
    dict['USR'] = item.get('user').get('name')
    dict['TEXT']= item.get('text')
    dict['LOCATION'] = item.get('user').get('location')
    dict['MENTIONS'] = item.get('entities').get('user_mentions')
    dict['HASHT'] = item.get('entities').get('hashtags')
    result.append(dict)

print(len(result))
s = ''
hasht = []
with open('results', 'a') as f:
    f.write('Time\t\t\t\tUSER LOCATION\t\t\t\tTWEET ID\t\t\t\tUSER NAME\t\t\t\tTWEET\t\t\t\tMentions\t\t\t\t#Mentions\t\t\t\tHashtags\t\t\t\t#Hashtags\n')
    for d in result:
        f.write(str(d['T'])+'\t\t'+str(d['LOCATION'])+'\t\t'+str(d['ID'])+'\t\t'+ str(d['USR']+'\t\t'+str(d['TEXT'])))
        c = 0
        for m in d['MENTIONS']:
            c += 1
            #mj = json.load(m)
            f.write('\t' + m.get('name') + '\t')
        f.write(str(c)+'\t\t')
        c = 0
        for m in d['HASHT']:
            c += 1
            f.write('\t' + m.get('text') + '\t')
        f.write(str(c)+'\t\t\n')

doc = tb(s)
bloblist = [doc]

for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))