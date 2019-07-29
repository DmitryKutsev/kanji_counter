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
def freq_from_one_file(file, word):
    print(os.getcwd())
    midashi_file = open(file, 'r',encoding='Utf-8')
    midashi_text = midashi_file.read()
    segmenter = tinysegmenter.TinySegmenter()
    all_japanese_symbols = r'[\u3041-\u3096\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u30A0-\u30FF]+'
    stop_re = r'[\u3041-\u3096]'
    tokens_list = []
    for i in segmenter.tokenize(midashi_text):
        if not re.fullmatch(stop_re, i) and re.search(all_japanese_symbols, i):
            # если это НЕ одиночный символ ХИРАГАНЫ, и при этом есть любой символ каны(включая хирагану)
            #print(i)
            tokens_list.append(i)
    midashi_nltk = nltk.Text(tokens_list)
    #test_concordance = midashi_nltk.concordance('社員')
    midashi_fdist = nltk.FreqDist(midashi_nltk)
    print(midashi_fdist.most_common(5))
    filename = file.split('\\')[-1]
    midashi_file.close()
    return str('Word frequency in downloaded topics: ') + str(midashi_fdist[word])

#freq_from_one_file('07.12.2019__shakai.txt', '首相')



def today_shakai_topiks():
    today = datetime.date.today().strftime("%m.%d.%Y")
    if not os.path.exists("/etc/hosts"):
        os.mkdir(os.getcwd() + '\\shakai_topics')
    input_file = os.getcwd() + '\\shakai_topics\\' + today + '__shakai.txt'
    #foldiers for topics sorted by date
    input_handle = open(input_file, 'w', encoding="utf-8")

    midashi_dict = {}
    shinbun_shakai = urlopen('https://mainichi.jp/shakai/')
    shakai_bs = bs(shinbun_shakai , 'html.parser')
    midashi_list = shakai_bs.find('ul',{"class":"list-typeD"})
    print(midashi_list)
    for li in midashi_list.find_all('li'):
        midashi_text = li.find('span',{"class":"midashi"}).text
        midashi_date = li.find('p', {"class": "date"}).text
        midashi_href = li.find('a', href=True)['href']
        input_handle.write('Date: ' + midashi_date + '   Midashi:'+ midashi_text + '   Link:  ' + midashi_href + '\n')
        #print(midashi_text, midashi_date)
        midashi_dict.update({midashi_text: midashi_date})

    for key, value in midashi_dict.items():
        print(key, value, "\n")

    print(len(midashi_dict))
    today = datetime.date.today().strftime("%m/%d/%Y")
    print(today)
    input_handle.close()
#today_shakai_topiks()

def dict_one_symbol(inp_kanji):
    for kanji in list(inp_kanji):
        print("\n\n\n", "KANJI ", kanji, " MEANINGS: ", "\n\n\n")
        url = 'https://kanjiapi.dev/v1/words/'
        kanji = urllib.parse.quote(kanji)
        full_url = url + kanji
       #kanji_link = url + str(kanji)
        data = urllib.request.urlopen(full_url).read()
        #result = data.decode()
        result = json.loads(data)
        print(result)
        for i in result:
            for j in i['meanings']:
                for k in j['glosses']:
                    print(k)

        #print(i['meanings'])
    #print(type(result))
#dict_one_symbol("北海道")

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