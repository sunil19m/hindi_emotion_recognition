import csv
import os
from urllib.request import urlopen
import codecs
from glob import glob
from constant import (BASE_PATH,
                      ANEW_ENGLISH_CSV_PATH,
                      ANEW_HINDI_PATH,
                      ADVERB_ENGLISH_CSV_PATH,
                      ADVERB_HINDI_PATH)


def fetch_english_anew_words():
    """
    Returns the dictionary of the english anew 1031 words
    along with the arousal, valence values
    """
    anew_data = dict()
    with open(ANEW_ENGLISH_CSV_PATH, "r") as file_pointer:
        line = csv.reader(file_pointer, delimiter=',')
        next(line, None)
        for row in line:
            if row[0] not in anew_data:
                anew_data[row[0]] = dict()
            anew_data[row[0]]["word"] = row[0]
            anew_data[row[0]]["word_num"] = row[1]
            anew_data[row[0]]["valence_mean"] = row[2]
            anew_data[row[0]]["valence_sd"] = row[3]
            anew_data[row[0]]["arousal_mean"] = row[4]
            anew_data[row[0]]["arousal_sd"] = row[5]
            anew_data[row[0]]["dominance_mean"] = row[6]
            anew_data[row[0]]["dominance_sd"] = row[7]
            anew_data[row[0]]["word_frequency"] = row[8]
    return anew_data

def fetch_english_adverb_words():
    """
    Returns the dictionary of the english anew 1031 words
    along with the arousal, valence values
    """
    adverb_data = dict()
    with open(ADVERB_ENGLISH_CSV_PATH, "r") as file_pointer:
        line = csv.reader(file_pointer, delimiter=',')
        next(line, None)
        for row in line:
            if row[0] not in adverb_data:
                adverb_data[row[0]] = dict()
            adverb_data[row[0]]["adverb"] = row[0]
    return adverb_data