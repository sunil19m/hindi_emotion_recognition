"""
How to run the final code:

****The code giving best result*****

cd src/python/
python3 lyrics_score_with_word_count.py ; python3 comparision_value.py; python3 spectral_cluster_avg.py; python3 comparision_value.py;

"""

python3 -m pip install beautifulsoup4
python3 -m pip install lxml


1) GetUrlsForSongs.py
	a. Generates the URLs of the lyrics 

2) parser_smirti.py
	a. Generates json file which contains lyric details

3) python3 downloader_shadhakosh.py --category=anew_hindi
	a. Downloads html file for each word in ANEW and stores in raw/downloaded_anew_hindi

4) python3 downloader_shadhakosh.py --category=adverb_hindi
	a. Downloads html file for every adverb and stores in raw/ downloaded_adverb_hindi

5) python3 parser_shadhakosh.py --category=anew_hindi
	a. Parses each of the downloaded html files and generates the valence and arousal scores for each word in ANHW. This 	is stored as raw/model_data/anhw_model.txt
	b. All the synonyms of each of the ANEW songs are stored in raw/model_data/check_anew_data.txt

6) python3 parser_shadhakosh.py --category=adverb_hindi
	a. Parses the downloaded html file of adverbs and gives a score to each word. This is stored as raw/model_data/adverb_model.txt
	b. All of the synonyms of English adverbs are stored in raw/model_data/check_adverb_data.txt

7) python3 lyrics_score_with_word_avg.py; python3 comparision_value.py;
	a. Takes all the valence & arousal points and finds the average and classify based on the quadrant it belongs to.
	b. The comparision_value.py compares the human labelled with machine generated value.

8) python3 lyrics_score_with_word_avg.py; python3 comparision_value.py;
	a. Takes all the valence & arousal points and finds the average and classify based on the quadrant it belongs to.
	b. The comparision_value.py compares the human labelled with machine generated value.
	c. The output printed is the SongID | quadrant number. The final is the result

9) python3 lyrics_score_with_sentence_avg.py; python3 comparision_value.py;
	a. Takes all the sentence valence & arousal points and finds the average and classify based on the quadrant it belongs to.
	b. The comparision_value.py compares the human labelled with machine generated value.
	c. The output printed is the SongID | quadrant number. The final is the result

10) python3 lyrics_score_with_word_count.py; python3 comparision_value.py;
11) python3 lyrics_score_with_sentence_count.py; python3 comparision_value.py;

12) python3 lyrics_score_with_word_count.py ; python3 comparision_value.py; python3 spectral_cluster_avg.py; python3 comparision_value.py;
	a. This does the weighted average of the cluster based on the word

13) python3 lyrics_score_with_sentence_count.py; python3 comparision_value.py; python3 spectral_cluster_avg.py; python3 comparision_value.py;
	a. This takes the weighted average of the cluster based on the sentence

12) python3 lyrics_score_with_word_count.py ; python3 comparision_value.py; python3 spectral_cluster.py; python3 comparision_value.py;
	a. This takes the dominant cluster based on the word

13) python3 lyrics_score_with_sentence_count.py; python3 comparision_value.py; python3 spectral_cluster.py; python3 comparision_value.py;
	a. This takes the dominant cluster based on the sentence