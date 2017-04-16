from bs4 import BeautifulSoup
import codecs
import re
from glob import glob
from constant import (ANEW_HINDI_PATH,
                      ADVERB_HINDI_PATH,
                      MODEL_PATH,
                      ADVERB_MODEL_DATA,
                      VALENCE_MEAN_INDEX,
                      VALENCE_SD_INDEX,
                      AROUSAL_MEAN_INDEX,
                      AROUSAL_SD_INDEX,
                      VALENCE_MEAN,
                      VALENCE_SD,
                      AROUSAL_MEAN,
                      AROUSAL_SD)

from os import path
from parser_csv import (fetch_english_anew_words,
                        fetch_english_adverb_words)
import codecs
import json
import sys
from hindi_stemmer import hindi_stemmer

def get_all_html_files(path):
    return glob(path + "*.txt")

def is_valid_hindi_word(word):
    if word.isalpha():
        return False
    result = list()
    # split on space
    word = word.split()
    for val in word:
        result.extend(val.split("-"))
    for i in result:
        if i.isalpha():
            return False
    return True

def extract_synonyms_shadhakosh_txt(file_lists):
    """
    Parses the given html and returns all the synonyms of the given word.
    The result is the dictionary of the english anew word to hindi synonyms.
    """
    word_synonym=dict() 
    for file_path in file_lists:
        soup=BeautifulSoup(codecs.open(file_path,encoding="utf-8"), "lxml")
        lis = soup.find_all("li")
        synonyms = list()
        for li in lis:
            li_soup = BeautifulSoup(str(li), "lxml")
            if li_soup.find(attrs={"class": "fa fa-volume-up fa-lg in au1"}):
                val = li_soup.find('a',attrs={'class':'in l'}).getText()
                if val:
                    synonyms.append(val)
        file_name = path.basename(file_path)
        anew_word = file_name.split("_")[0]
        word_synonym[anew_word]=synonyms
    return word_synonym


def map_anew_with_hindi_synonymns(anew_data, word_synonym_dict):
    hindi_anew_emotion = dict()
    for key, value in word_synonym_dict.items():
        if key not in anew_data:
            print (key)
            raise Exception("Something wrong... Check the synonyms words dict with anew word")
        for synonym in word_synonym_dict[key]:
            emotion_list = [0, 0, 0, 0]
            emotion_list[VALENCE_MEAN_INDEX] = anew_data[key][VALENCE_MEAN]
            emotion_list[VALENCE_SD_INDEX] = anew_data[key][VALENCE_SD]
            emotion_list[AROUSAL_MEAN_INDEX] = anew_data[key][AROUSAL_MEAN]
            emotion_list[AROUSAL_SD_INDEX] = anew_data[key][AROUSAL_SD]
            hindi_anew_emotion[hindi_stemmer(synonym)] = emotion_list
    return hindi_anew_emotion

def map_adverb_with_hindi_synonymns(word_synonym_dict):
    hindi_adverb_emotion = dict()
    for key, value in word_synonym_dict.items():
        emotion_list = [1.2, 1.2, 1.2, 1.2]
        for synonym in word_synonym_dict[key]:
            hindi_adverb_emotion[hindi_stemmer(synonym)] = emotion_list
    return hindi_adverb_emotion

def write_to_file_as_json(data, file_name):
    with codecs.open(file_name, "wb", encoding="utf-8") as file_pointer:
        json.dump(data, file_pointer, ensure_ascii=False)

def main(args):
    category = None
    path = ANEW_HINDI_PATH
    for arg in args:
        if '--category' in arg:
            # Category can be "anew_hindi" or "adverb_hindi"
            category = arg.split('=')[1]
            if not (category == "anew_hindi" or category == "adverb_hindi"):
                raise Exception("Category can be 'anew_hindi' or 'adverb_hindi' only")
        else:
            raise Exception("Please give: python3 parser_shadhakosh.py --category=anew_hindi (or)\
                    python3 parser_shadhakosh.py --category=adverb_hindi")
    
    if category == "anew_hindi":
        path = ANEW_HINDI_PATH
        file_list = get_all_html_files(path)
        word_synonym_dict = extract_synonyms_shadhakosh_txt(file_list)
        anew_data = fetch_english_anew_words()
        anhw_synonymns_emotions_dict = map_anew_with_hindi_synonymns(anew_data, word_synonym_dict)
        write_to_file_as_json(word_synonym_dict,  MODEL_PATH + "check_anew_data.txt")
        write_to_file_as_json(anhw_synonymns_emotions_dict, MODEL_PATH + "anhw_model.txt")

    elif category == "adverb_hindi":
        path = ADVERB_HINDI_PATH
        file_list = get_all_html_files(path)
        word_synonym_dict = extract_synonyms_shadhakosh_txt(file_list)
        adverb_synonymns_emotions_dict = map_adverb_with_hindi_synonymns(word_synonym_dict)
        write_to_file_as_json(word_synonym_dict,  MODEL_PATH + "check_adverb_data.txt")
        write_to_file_as_json(adverb_synonymns_emotions_dict, MODEL_PATH + "adverb_model.txt")
    else:
        raise Exception("Please give: python3 parser_shadhakosh.py --category=anew_hindi (or)\
                    python3 parser_shadhakosh.py --category=adverb_hindi")

if __name__ == "__main__":
    main(sys.argv[1:])
