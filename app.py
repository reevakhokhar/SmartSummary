from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
from googlesearch import search
from nltk.corpus import stopwords
import os
from flask import Flask, flash, request, redirect, url_for, render_template
import numpy as np
from nltk import tokenize
from operator import itemgetter
import math
import nltk
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


app = Flask(__name__)

# basic page render


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/summarizer')
def test():
    return render_template('summarizer.html')


@app.route('/script')
def script():
    return render_template('script.html')

# once a value is submitted on the form woo


@app.route('/readout', methods=['POST'])
def readout():
    textscript = request.form['text']
    return render_template('readout.html', textscript=textscript)


@app.route('/submit', methods=['POST'])
def submit():
    # getting the text
    transcript = request.form['text']
    doc = remove_stopwords(transcript)
    print(doc)

    total_words = doc.split()
    total_word_length = len(total_words)
    # print(total_word_length)

    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)

    # calculating the term frequency score
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

    def check_sent(word, sentences):
        final = [all([w in x for w in word]) for x in sentences]
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    idf_score.update((x, math.log(int(total_sent_len)/y))
                     for x, y in idf_score.items())

    tf_idf_score = {key: tf_score[key] *
                    idf_score.get(key, 0) for key in tf_score.keys()}
    # print(tf_idf_score)

    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(),
                      key=itemgetter(1), reverse=True)[:n])
        return result

    # getting the word
    top_5_words = get_top_n(tf_idf_score, 6)

    # importing google
    from googlesearch import search

    keys = top_5_words.keys()

    list = []
    for key in keys:
        list.append(key)

    print(list)

    key1 = list[0]
    key2 = list[1]
    key3 = list[2]
    key4 = list[3]
    key5 = list[4]

    # youtube vid search
    import urllib.request
    import re
    import ssl

    def searchVideoForKeyword(searchKeyword):
        allvideos = ''
        allEmbedLinks = []
        if len(searchKeyword.split(" ")) > 1:
            searchKeyword = searchKeyword.replace(" ", "+")

        searchKeyword = searchKeyword.replace("!web ", "")
        url = "https://www.youtube.com/results?search_query=" + searchKeyword
        gcontext = ssl.SSLContext()
        html = urllib.request.urlopen(url, context=gcontext)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        allvideos = ("https://www.youtube.com/embed/" + video_ids[0])

        return allvideos

    websitelink = []
    for j in list:
        for i in search(j, tld='com', lang='en', num=3, stop=3, pause=0.5):
            linked_list = [i]
            print(linked_list)
            print('isthistheweb')
            websitelink.append(i)

    websitelink1 = []
    websitelink2 = []
    websitelink3 = []
    websitelink4 = []
    websitelink5 = []

    for i in range(3):
        websitelink1.append(websitelink[i])
        websitelink2.append(websitelink[i+3])
        websitelink3.append(websitelink[i+6])
        websitelink4.append(websitelink[i+9])
        websitelink5.append(websitelink[i+12])

    # #gives the youtube video link(embed)
    youtube_link = []
    for word in list:

        youtube_link.append(searchVideoForKeyword(word))

    yt1 = youtube_link[0]
    yt2 = youtube_link[1]
    yt3 = youtube_link[2]
    yt4 = youtube_link[3]
    yt5 = youtube_link[4]

    youtube_list = []

    def get_keyword():
        dict = {}
        linked_list = []
        for x in list:
            yt = searchVideoForKeyword(x)
            dict[x] = yt

    return render_template('result.html', key1=key1, key2=key2, key3=key3, key4=key4, key5=key5, doc=doc, yt1=yt1, yt2=yt2, yt3=yt3, yt4=yt4, yt5=yt5, websitelink=websitelink, list=list, websitelink1=websitelink1, websitelink2=websitelink2, websitelink3=websitelink3, websitelink4=websitelink4, websitelink5=websitelink5)


if __name__ == '__main__':
    app.run()
