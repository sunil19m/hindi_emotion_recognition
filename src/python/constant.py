import os

# Change this path to your system path
BASE_PATH = "/home/sunil/nlp_project/"

# All the raw downloaded files are present here
RAW_PATH = os.path.join(BASE_PATH, "raw/")
if not os.path.exists(RAW_PATH):
    os.makedirs(RAW_PATH)

#
# The folder raw/anew/all.csv contains all 1031 words with arousal, valence
# values in excel
#
ANEW_ENGLISH_CSV_PATH = os.path.join(BASE_PATH, "raw/anew_english/all.csv")

#
# All the hindi version of the downloaded anew words along with synonyms are present
#
ANEW_HINDI_PATH = os.path.join(BASE_PATH, "raw/downloaded_anew_hindi/")
if not os.path.exists(ANEW_HINDI_PATH):
    os.makedirs(ANEW_HINDI_PATH)

#
# The folder raw/anew/all.csv contains all 1031 words with arousal, valence
# values in excel
#
ADVERB_ENGLISH_CSV_PATH = os.path.join(BASE_PATH, "raw/adverb_english/all_adverbs.csv")

#
# All the hindi version of the downloaded anew words along with synonyms are present
#
ADVERB_HINDI_PATH = os.path.join(BASE_PATH, "raw/downloaded_adverb_hindi/")
if not os.path.exists(ADVERB_HINDI_PATH):
    os.makedirs(ADVERB_HINDI_PATH)

#LYRICS_150_JSON_PATH = os.path.join(BASE_PATH, "raw/lyrics/150_hindi_song_list_test.json")
LYRICS_150_JSON_PATH = os.path.join(BASE_PATH, "raw/lyrics/150_hindi_song_list.json")

###################################################################################
#
# Model data path
#

#
# If the model_data folder doesn't exist, create one
#
MODEL_PATH = os.path.join(RAW_PATH, "model_data/")
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

# Anhw model data
ANHW_MODEL_DATA = os.path.join(RAW_PATH, "model_data/anhw_model.txt")

# Adverb model data
ADVERB_MODEL_DATA = os.path.join(RAW_PATH, "model_data/adverb_model.txt")

###################################################################################
# Emotions index constants
VALENCE_MEAN_INDEX = 0
VALENCE_SD_INDEX = 1
AROUSAL_MEAN_INDEX = 2
AROUSAL_SD_INDEX = 3

VALENCE_MEAN = "valence_mean"
VALENCE_SD = "valence_sd"
AROUSAL_MEAN = "arousal_mean"
AROUSAL_SD = "arousal_sd"


###################################################################################
# Lyrics constants
LYRICS = "lyrics"