from urllib.request import urlopen
from urllib.parse import urlencode
import urllib
from bs4 import BeautifulSoup as bs
import re
import datetime
import tinysegmenter
from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
import nltk
import json
####Юникод для японских регулярок!!!!####
#[\u3041-\u3096]-Hiragana
# [\u30A0-\u30FF] - Katakana(?)
#[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A] - Kanji(?)
######


#https://kanjiapi.dev/ - найденный словарь иероглифов, из него божно вытащить и значение для слова из нескольких иероглифов!
#https://pypi.org/project/tinysegmenter/ - найденный токенизатор(вроде хороший)

def tokenize_stopping(sentence):
    segmenter = tinysegmenter.TinySegmenter()
    all_japanese_symbols = r'[\u3041-\u3096\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u30A0-\u30FF]+'
    stop_re = r'[\u3041-\u3096]'
    tokens_list = []
    for i in segmenter.tokenize(sentence):
        if not re.fullmatch(stop_re, i) and re.search(all_japanese_symbols, i):
            #если это НЕ одиночный символ ХИРАГАНЫ, и при этом есть любой символ каны(включая хирагану)
            print(i)
            tokens_list.append(i)


def translate_in_yarxi(input_kanji):
    path = os.getcwd() + '\\geckodriver.exe'
    addon_path = os.getcwd() + '\\proxy_auth.xpi'
    time.sleep(1)
    wd = webdriver.Firefox(executable_path=path)
    wd.install_addon(addon_path, temporary=True)
    wd.get("https://yarxi.ru/")
    time.sleep(2)
    wd.find_element_by_css_selector('input[id="Reading"]').send_keys(input_kanji)
    time.sleep(2)
    wd.find_element_by_css_selector('input[id="Reading"]').send_keys(Keys.ENTER)
    time.sleep(10)
    wd.quit()
#translate_in_yarxi('面会')



#здесь токенизация содержится не отдельной функцией(надоб зафиксить)
def freq_from_one_file(word):
    fdist = 0
    midashi_fdist = 0
    path = os.getcwd() + '\\shakai_topics'
    tokens_list = []
    if os.path.exists(path):
        for i in os.listdir(path):
            midashi_file = open(path + '\\' + i, 'r',encoding='Utf-8')
            midashi_text = midashi_file.read()
            segmenter = tinysegmenter.TinySegmenter()
            all_japanese_symbols = r'[\u3041-\u3096\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u30A0-\u30FF]+'
            stop_re = r'[\u3041-\u3096]'
            for i in segmenter.tokenize(midashi_text):
                if not re.fullmatch(stop_re, i) and re.search(all_japanese_symbols, i):
                    # если это НЕ одиночный символ ХИРАГАНЫ, и при этом есть любой символ каны(включая хирагану)
                    tokens_list.append(i)

            midashi_nltk = nltk.Text(tokens_list)
            midashi_fdist = nltk.FreqDist(midashi_nltk)
            midashi_file.close()
            fdist = fdist + midashi_fdist[word]
        print(tokens_list)
        print(fdist)
        return str('Word frequency in downloaded topics: ') + str(midashi_fdist[word])
    else:
        return str('Word frequency in downloaded topics: ') + str(0)

#freq_from_one_file('07.12.2019__shakai.txt', '首相')
#freq_from_one_file('北九州')

def if_today_exists():
    today = datetime.date.today()
    filename = str(today) + '.txt'
    path = os.getcwd() + '\\shakai_topics'
    earlier_topics_list = []
    #print(topics_list)
    if filename in os.listdir(path):
        print(1)
        return True
    else:
        print(0)
        return None
#if_today_exists()

def all_topics():
    path = os.getcwd() + '\\shakai_topics'
    return os.listdir(path)

all_topics()


def earlier_topics():
    today = datetime.date.today()
    filename = str(today) + '.txt'
    path = os.getcwd() + '\\shakai_topics'
    earlier_topics_list = []
    #print(topics_list)
    for i in os.listdir(path):
        if i != filename:
            earlier_topics_list.append(i)
    #print(earlier_topics_list)
    return earlier_topics_list
#earlier_topics()


def shakai_topiks_by_date():
    today = datetime.date.today()
    date = str(today)
    path = os.getcwd() + '\\shakai_topics'
    if not os.path.exists(path):
        os.mkdir(path)
    input_file = path + '\\' + date + '.txt'
    input_file_name = date + '.txt'
    topic_list = []
    if input_file_name not in os.listdir(path):
        input_handle = open(input_file, 'w', encoding="utf-8")
        counter = 0
        page_number = 1
        while counter == 0:
            shinbun_shakai = urlopen('https://mainichi.jp/shakai/' + str(page_number))
            shakai_bs = bs(shinbun_shakai , 'html.parser')
            midashi_list = shakai_bs.find('ul',{"class":"list-typeA"})
            re_string = r'(?P<year>[0-9]{4}).(?P<mounth>[0-9]{2}).(?P<day>[0-9]{2})'
            if re.match(re_string, date):
                input_compare = re.match(re_string, date)
                input_year = input_compare.group('year')
                input_mounth = input_compare.group('mounth')
                input_day = input_compare.group('day')
            #print(midashi_list)
            num = 0
            for i in midashi_list:
                num +=1
                #print(i)
                midashi_topic = i.findNext('span', {"class": "midashi"}).text + '\n'
                if num%2 == 0:
                    pass
                try:
                    cycle_compare = re.match(re_string, i.findNext('span', {"class": "date"}).text)
                    if cycle_compare.group('year') == input_year and cycle_compare.group('day') == input_day and cycle_compare.group('mounth') == input_mounth:
                        #print(i.findNext('span', {"class": "date"}).text)
                        if num % 2 == 0:
                            input_handle.write(midashi_topic)
                            #print(midashi_topic)
                            topic_list.append(midashi_topic)
                    else:
                        counter = 1
                except AttributeError:
                    print("there is no text")
            page_number += 1
        input_handle.close()
        #print(topic_list)
        return topic_list
    else:
        topic_list.append('TODAY TOPICS HAVE ALREADY PARSED:')
        input_handle = open(input_file, 'r', encoding="utf-8")
        for i in input_handle:
            #print('exists')
            #print(i)
            topic_list.append(i)
        #print(topic_list)
        return topic_list

#shakai_topiks_by_date()




def dict_mult_symbol(inp_kanji):
    print(inp_kanji)
    url = 'https://kanjiapi.dev/v1/words/'
    kanji = urllib.parse.quote(inp_kanji[0])
    full_url = url + kanji
   #kanji_link = url + str(kanji)
    try:
        data = urllib.request.urlopen(full_url).read()
    except urllib.error.HTTPError:
        result_string = "KANJI NOT FOUND"
        print(result_string)
        result_list = [result_string, result_string]
        return result_list
    #result = data.decode()
    result = json.loads(data)
    #print(result)
    result_pron_string = ''
    result_trancl_string = ''
    result_list = []
    result_string = ''
    translations_string = ''
    for i in result:
        for j in i['variants']:
            if j['written'] and j['written'] == inp_kanji:
               # print(j)
                #print('PRONOUNCUNG: ', j['pronounced'])
                #print("MEANINGS: ", i['meanings'][0]['glosses'])
                pron = '\nPRONOUNCING: ' + str(j['pronounced'])
                result_pron_string = result_pron_string +  ', ' + str(j['pronounced'])
                result_trancl_string = result_trancl_string + ', ' + str(i['meanings'][0]['glosses'])[1:-1]
                print(i['meanings'][0]['glosses'])
                for translates in i['meanings'][0]['glosses']:
                    translations_string = translations_string + translates + ', '

                result_string = result_string + pron + "\nTRANSLATION: " + translations_string[0:-2]
                result_list = [result_pron_string[1:], result_trancl_string[2:-1] + '.']
                #print(result_list)
    if len(result_trancl_string) > 1:
        print(result_pron_string)
        return result_list
    else:
        result_string = "KANJI NOT FOUND"
        result_list = [result_string, result_string]
        return result_list
#dict_mult_symbol("ппп")