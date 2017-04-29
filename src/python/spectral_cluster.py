import json
import codecs
import numpy as np
#import plotly.plotly as py
#import matplotlib.pyplot as plt
import math
import numpy as np

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
					  LYRICS,
					  LYRICS_SENTENCE_MODEL_DATA)

def write_to_file_as_json(data, file_name):
	with codecs.open(file_name, "wb", encoding="utf-8") as file_pointer:
		json.dump(data, file_pointer, ensure_ascii=False)

def read_json(path):
    with codecs.open(path, "r", "utf-8") as file_pointer:
        return json.load(file_pointer)

def update_value_column_wise(column_number, zero_np, data):
	i=0
	for j in data:
		zero_np[i,column_number] = float(j)
		i = i+1
	return zero_np


def convert_to_np_columns(valence, arousal):
	filtered_valence = list()
	filtered_arousal = list()
	filter = 1.7
	for i, value in enumerate(range(len(valence))):
		if (valence[i] < filter and valence[i] > (-1 * filter)) \
			or (arousal[i] < filter and arousal[i] > (-1 * filter)):
			continue
		else:
			filtered_valence.append(valence[i])
			filtered_arousal.append(arousal[i])

	song_np = np.zeros(shape=(len(valence),2))
	song_np = update_value_column_wise(0, song_np, filtered_valence)
	song_np = update_value_column_wise(1, song_np, filtered_arousal)
	return song_np


def spectral_cluster(valence, arousal):
	song_np = convert_to_np_columns(valence, arousal)
	#print (song_np)
	return song_np

def find_lyrics_score_quadrant(cluster_score):
	cluster_score_score_axis = dict()
	for key, value in cluster_score.items():
		if value[0] >= 0 and value[1] >= 0:
			cluster_score_score_axis[key] = 1
		if value[0] < 0 and value[1] > 0:
			cluster_score_score_axis[key] = 2
		if value[0] < 0 and value[1] < 0:
			cluster_score_score_axis[key] = 3
		if value[0] >= 0 and value[1] <= 0:
			cluster_score_score_axis[key] = 4
		print (str(key) + "|" + str(cluster_score_score_axis[key]))
	return cluster_score_score_axis

def find_adjacency_matrix(song, valence, arousal):
	sigma = 2
	adjacency = np.zeros(shape=(len(song),len(song)))
	for i in range(0,len(song)):
		for j in range(0,len(song)):
			distance=math.exp(-1*((valence[i]-valence[j])**2+abs(arousal[i]-arousal[j])**2)**(1/2.0)/(2*(sigma**2)))
			adjacency[i,j]=distance
	return adjacency

def find_degree_matrix(song, adjacency):
	degree=np.zeros(shape=(len(song),len(song)))
	for i in range(0,len(song)):
		sum = 0
		for j in range(0,len(song)):
			sum = sum + adjacency[i,j]
		degree[i,i]=sum
	return degree

def find_max_valence_arousal(V1, A1, V2, A2 ):
	max_valence = 0
	max_arousal = 0 
	if len(V1) > len(V2):
		max_valence = np.sum(V1)/(len(V1) * 1.0)
		max_arousal = np.sum(A1)/(len(A1) * 1.0)
	else:
		max_valence = np.sum(V2)/(len(V2) * 1.0)
		max_arousal = np.sum(A2)/(len(A2) * 1.0)
	return (max_valence, max_arousal)

def finding_cluster_values(laplacian, adjacency, degree, valence, arousal):
	eig_val,eig_vec = np.linalg.eigh(laplacian)
	temp = eig_vec[:,1]
	V1=[]
	A1=[]
	V2=[]
	A2=[]
	
	for i in range(0,len(temp)):
		if temp[i]<0:
			V1.append(valence[i])
			A1.append(arousal[i])
		elif temp[i]>0:
			V2.append(valence[i])
			A2.append(arousal[i])
	
	max=-100000
	for i in range(2,len(eig_val)):
		diff=abs(eig_val[i-1]-eig_val[i])
		if diff>max:
			max=diff	
			k=i-1
	return (V1, A1, V2, A2)

def spectral_binary_cluster_centriod():
	lyrics_stenctence_score = read_json(LYRICS_SENTENCE_MODEL_DATA)
	cluster_centroid = dict()
	for key, value in lyrics_stenctence_score.items():
		if not value:
			continue
		if len(value[VALENCE_MEAN]) == 1:
			cluster_centroid[key] = [value[VALENCE_MEAN][0], value[AROUSAL_MEAN][0]]
			continue
		
		song = spectral_cluster(value[VALENCE_MEAN], value[AROUSAL_MEAN])
		valence = song[0:,0]
		arousal = song[0:,1]

		adjacency = find_adjacency_matrix(song, valence, arousal)
		degree = find_degree_matrix(song, adjacency)

		laplacian = degree-adjacency
		(V1, A1, V2, A2) = finding_cluster_values(laplacian, adjacency, degree, valence, arousal)


		(max_valence, max_arousal) = find_max_valence_arousal(V1, A1, V2, A2)
		cluster_centroid[key] = [max_valence, max_arousal] 
	cluster_axis = find_lyrics_score_quadrant(cluster_centroid)
	write_to_file_as_json(cluster_axis,  MODEL_PATH + "lyrics_score_axis_model.txt")

spectral_binary_cluster_centriod()
