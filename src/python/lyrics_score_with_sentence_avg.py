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

CENTER_SCORE = 5.0

def read_json(path):
	with codecs.open(path, "r", "utf-8") as file_pointer:
		return json.load(file_pointer)

def modify_anhw_score(word_emotion_anhw, prev_adverb_score):
	return [float(a) * float(b) for a,b in zip(word_emotion_anhw, prev_adverb_score)]

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
	#print ("===================================================")
	sentence_score = dict()
	words = sentence.split()
	word_len = len(words)
	i = 0
	prev_adverb_score = None
	prev_anhw_score = None
	is_word_found = False
	prev_word = ""
	while (i < len(words)):
		j = i + 1
		while(j < i+4  and j <= word_len):
			new_word = words[i:j]
			is_word_found = False
			new_word = ' '.join(new_word)
			prev_word = new_word
			if new_word in anhw_model:
				if not prev_adverb_score:
					#print ("Found 1", new_word)
					#print (new_word)
					sentence_score[new_word] = [(float(i) - CENTER_SCORE) for i in anhw_model[new_word]]
					#print (sentence_score[new_word])
					prev_anhw_score = (new_word, sentence_score[new_word])
				else:
					#print (anhw_model[new_word], prev_adverb_score)
					modified_score = [(float(i) - CENTER_SCORE) for i in anhw_model[new_word]]
					anhw_score = modify_anhw_score(modified_score, prev_adverb_score)
					#print (new_word)
					sentence_score[new_word] = anhw_score
					prev_adverb_score = None
					prev_anhw_score = None
					#print ("Found 2 ", new_word)
				i = j - 1
				is_word_found = True
				#print (new_word, anhw_model[new_word])
				break
			if new_word in adverb_model:
				if not prev_anhw_score:
					prev_adverb_score = [float(i) for i in adverb_model[new_word]]
					#print ("Found 3 ", new_word)
				else:
					#print (prev_anhw_score, adverb_model[new_word])
					anhw_score = modify_anhw_score(prev_anhw_score[1], adverb_model[new_word])
					#print (anhw_score)
					sentence_score[prev_anhw_score[0]] = anhw_score
					prev_adverb_score = None
					prev_anhw_score = None
					#print ("Found 4 ", new_word)
				i = j - 1
				is_word_found = True
				break
			j = j + 1
		i = i + 1

	#for key, value in sentence_score.items():
	#	print (key, value[0], value[2])

	#print(sentence_score)
	return sentence_score

def get_lyrical_score(anhw_model, adverb_model, json_lyrics_data):
	lyrics_emotion = dict()
	for id, value in json_lyrics_data.items():
		lyrics_emotion[id] = dict()
		lyrics_data = json_lyrics_data[id][LYRICS]
		lyrics_split = lyrics_data.split("\n")
		sentence_emotion = list()
		write_to_file_as_json(lyrics_data,  MODEL_PATH + "check_lyrics.txt")
		#sentence_emotion_dict = dict()
		stemmed_data = list()
		for sentence in lyrics_split:
			stemmed_sentence = hindi_stemmer(sentence)
			stemmed_data.append(stemmed_sentence)
			sentence_emotion_dict = find_sentence_emotion_score(stemmed_sentence, anhw_model, adverb_model)
			
			if sentence_emotion_dict:
				(sentence_valence, sentence_arousal) = find_sentence_valence_arousal(sentence_emotion_dict)
				#print ("-----")
				#print (sentence_valence, sentence_arousal)
				if VALENCE_MEAN not in lyrics_emotion[id]:
					lyrics_emotion[id][VALENCE_MEAN] = list()
					lyrics_emotion[id][AROUSAL_MEAN] = list()
				lyrics_emotion[id][VALENCE_MEAN].append(sentence_valence)
				lyrics_emotion[id][AROUSAL_MEAN].append(sentence_arousal)
			#else:
			#	print ("No value")
			#print ("===========================================")
		#print ("*********************************************************************")
		write_to_file_as_json(stemmed_data,  MODEL_PATH + "check_lyrics_stemmed.txt")
	return lyrics_emotion

def find_lyrics_score_quadrant(lyrics_score):
	lyrics_score_axis = dict()
	for key, value in lyrics_score.items():
		if value[0] >= 0 and value[1] >= 0:
			lyrics_score_axis[key] = 1
		if value[0] < 0 and value[1] > 0:
			lyrics_score_axis[key] = 2
		if value[0] < 0 and value[1] < 0:
			lyrics_score_axis[key] = 3
		if value[0] >= 0 and value[1] <= 0:
			lyrics_score_axis[key] = 4
		print (str(key) + "|" + str(lyrics_score_axis[key]))
	return lyrics_score_axis

def lyrics_score(lyrics_sentence_score):
	lyrics_score = dict()
	for key, value in lyrics_sentence_score.items():
		if value:
			valence_sum = 0
			for valence in value["valence_mean"]:
				valence_sum = valence_sum + valence
			valence_avg = valence_sum/len(value["valence_mean"])

			arousal_sum = 0
			for arousal in value["arousal_mean"]:
				arousal_sum = arousal_sum + arousal
			arousal_avg = arousal_sum/len(value["arousal_mean"])
			lyrics_score[key] = (valence_avg, arousal_avg)
	return lyrics_score


def main():
	anhw_model = read_json(ANHW_MODEL_DATA)
	adverb_model = read_json(ADVERB_MODEL_DATA)
	json_lyrics_data = read_json(LYRICS_150_JSON_PATH)

	"""
	json_data = dict()
	json_data["19"] = json_lyrics_data["19"]
	lyrics_sentence_score = get_lyrical_score(anhw_model, adverb_model, json_data)
	"""
	print ("Song ID | Quadrant Number")
	lyrics_sentence_score = get_lyrical_score(anhw_model, adverb_model, json_lyrics_data)
	lyrics_one_score = lyrics_score(lyrics_sentence_score)
	lyrics_score_axis = find_lyrics_score_quadrant(lyrics_one_score)
	write_to_file_as_json(lyrics_sentence_score,  MODEL_PATH + "lyrics_sentence_score_model.txt")
	write_to_file_as_json(lyrics_one_score,  MODEL_PATH + "lyrics_one_score_model.txt")
	write_to_file_as_json(lyrics_score_axis,  MODEL_PATH + "lyrics_score_axis_model.txt")

if __name__ == "__main__":
    main()
