import pandas as pd
import os
import preprocessor as p
import string
from nltk.tokenize import TweetTokenizer
from emoji import demojize
import re

tokenizer = TweetTokenizer()

def normalizeToken(token):
    lowercased_token = token.lower()
    if token.startswith("@"):
        return " "
    elif token.startswith("#"):
        return " "
    elif lowercased_token.startswith("http") or lowercased_token.startswith("www"):
        return " "
    elif len(token) == 1:
        return demojize(token)
    else:
        if token == "’":
            return "'"
        elif token == "…":
            return "..."
        else:
            return token

def normalizeTweet(tweet):

    normTweet = tweet.replace("cannot ", " ").replace("n't ", " ").replace("n 't ", " ").replace("ca n't", " ").replace("ai n't", " ")
    normTweet = normTweet.replace("'m ", " 'm ").replace("'re ", " 're ").replace("'s ", " 's ").replace(" i'll ", " ").replace("'d ", " 'd ").replace("'ve ", " 've ")
    normTweet = normTweet.replace(" p . m .", "  p.m.") .replace(" p . m ", " p.m ").replace(" a . m .", " a.m.").replace(" a . m ", " a.m ")
    normTweet = normTweet.replace("RT ", "").replace("rt ", "")
    
    normTweet = normTweet.translate((str.maketrans('','',string.punctuation)))

    tokens = tokenizer.tokenize(normTweet.replace("’", "").replace("…", " "))
    tokens = [word for word in tokens if len(word)>1]
    tokens = [x for x in tokens if not (x.isdigit() 
                                         or x[0] == '-' and x[1:].isdigit())]

    normTweet = " ".join([normalizeToken(token) for token in tokens])    
    
    return " ".join(normTweet.split())
def generate_texts(mon):
    directory = "covid-project/keyword_based_dataset_no_dup/" + mon+'/'

    output_dir = "covid-project/"+'refined_hate/'+ mon+'/'
    
   
    for filename in os.listdir(directory):
        if(filename.endswith('.csv')):

            df = pd.read_csv(directory+filename, encoding='utf-8', usecols = [2, 1], header = None)
            df = df[df[1] > '3'] # Hate tweets
            del df[1]
            df[2] = [normalizeTweet(item) for item in df[2]]
            df.drop_duplicates(subset =[2], keep = False, inplace = True)

            with open(output_dir+filename[:-4]+'.txt', 'w', encoding='utf-8') as f:
                for item in df[2]:
                    f.write("%s\n" % item)
                    # print("%s\n" % item)

    return 0

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']

for mon in months:
    df = generate_texts(mon)
    directory = "covid-project/keyword_based_dataset_no_dup/" + mon+'/'
    
    with open(mon+'_files.txt', 'w', encoding='utf-8') as f:
        for filename in os.listdir(directory):
            if(filename.endswith('.csv')):
                f.write("%s.txt\n" % filename[:-4])
                print("%s.txt\n" % filename[:-4])


