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
					  AROUSAL_SD,
					  LYRICS_150_JSON_PATH,
					  ANHW_MODEL_DATA,
					  LYRICS)

from os import path
from parser_csv import (fetch_english_anew_words,
                        fetch_english_adverb_words)
import codecs
import json
import sys
from hindi_stemmer import hindi_stemmer

def read_json(path):
	with codecs.open(path, "r", "utf-8") as file_pointer:
		return json.load(file_pointer)

def modify_anhw_score(word_emotion_anhw, prev_adverb_score):
	return [float(a)*float(b) for a,b in zip(word_emotion_anhw, prev_adverb_score)]

def write_to_file_as_json(data, file_name):
	with codecs.open(file_name, "wb", encoding="utf-8") as file_pointer:
		json.dump(data, file_pointer, ensure_ascii=False)

def find_sentence_valence_arousal(sentence_emotion_dict):
	unique_keys = len(sentence_emotion_dict)
	valence_mean = 0
	arousal_mean = 0
	for key, value in sentence_emotion_dict.items():
		valence_mean = valence_mean + value[VALENCE_MEAN_INDEX]
		arousal_mean = arousal_mean + value[AROUSAL_MEAN_INDEX]
	return (valence_mean/unique_keys, arousal_mean/unique_keys)

def find_sentence_emotion_score(sentence, anhw_model, adverb_model):
	sentence_score = dict()
	words = sentence.split()
	word_len = len(words)
	i = 0
	prev_adverb_score = None
	prev_anhw_score = None
	is_word_found = False
	anhw_words_lyrics = dict()
	prev_word = ""
	while (i < len(words) - 1):
		j = i + 1
		while(j < i+4  and j < word_len):
			new_word = words[i:j]
			is_word_found = False
			new_word = ' '.join(new_word)
			prev_word = new_word
			if new_word in anhw_model:
				if not prev_adverb_score:
					if prev_anhw_score:
						sentence_score[new_word] = prev_anhw_score
						anhw_words_lyrics[new_word] = prev_anhw_score
					try:
						prev_anhw_score = [float(i) for i in anhw_model[new_word]]
					except:
						print (new_word)
						print (anhw_model[new_word])
						raise Exception("stop")
					#print ("Found 1", new_word)
				else:
					anhw_score = modify_anhw_score(anhw_model[new_word], prev_adverb_score)
					sentence_score[new_word] = anhw_score
					prev_adverb_score = None
					prev_anhw_score = None
					#print ("Found 2 ", new_word)
				i = j - 1
				is_word_found = True
				break
			if new_word in adverb_model:
				if not prev_anhw_score:
					prev_adverb_score = [float(i) for i in adverb_model[new_word]]
					#print ("Found 3 ", new_word)
				else:
					anhw_score = modify_anhw_score(prev_anhw_score, adverb_model[new_word])
					sentence_score[new_word] = anhw_score
					prev_adverb_score = None
					prev_anhw_score = None
					#print ("Found 4 ", new_word)
				i = j - 1
				is_word_found = True
				break
			j = j + 1
		if not is_word_found:
			if prev_anhw_score:
				sentence_score[prev_word] = prev_anhw_score
			prev_adverb_score = None
			prev_anhw_score = None
		i = i + 1
	if prev_anhw_score:
		sentence_score[prev_word] = prev_anhw_score
	return sentence_score

def get_lyrical_score(anhw_model, adverb_model, json_lyrics_data):
	lyrics_emotion = dict()
	for id, value in json_lyrics_data.items():
		lyrics_emotion[id] = dict()
		lyrics_data = json_lyrics_data[id][LYRICS]
		lyrics_split = lyrics_data.split("\n")
		sentence_emotion = list()
		write_to_file_as_json(lyrics_data,  MODEL_PATH + "check_lyrics.txt")
		for sentence in lyrics_split:
			stemmed_sentence = hindi_stemmer(sentence)
			sentence_emotion_dict = find_sentence_emotion_score(stemmed_sentence, anhw_model, adverb_model)
			if sentence_emotion_dict:
				(sentence_valence, sentence_arousal) = find_sentence_valence_arousal(sentence_emotion_dict)
				if VALENCE_MEAN not in lyrics_emotion[id]:
					lyrics_emotion[id][VALENCE_MEAN] = list()
					lyrics_emotion[id][AROUSAL_MEAN] = list()
				lyrics_emotion[id][VALENCE_MEAN].append(sentence_valence)
				lyrics_emotion[id][AROUSAL_MEAN].append(sentence_arousal)
			#print ("===========================================")
		#print ("*********************************************************************")
	return lyrics_emotion

def main():
	anhw_model = read_json(ANHW_MODEL_DATA)
	adverb_model = read_json(ADVERB_MODEL_DATA)
	json_lyrics_data = read_json(LYRICS_150_JSON_PATH)
	lyrics_score = get_lyrical_score(anhw_model, adverb_model, json_lyrics_data)
	write_to_file_as_json(lyrics_score,  MODEL_PATH + "lyrics_model.txt")

if __name__ == "__main__":
    main()
