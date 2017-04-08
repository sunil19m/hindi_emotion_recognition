import csv
import os
#from urllib.request import urlopen
import urllib
import codecs
from glob import glob
from constant import (BASE_PATH,
                      ANEW_ENGLISH_CSV_PATH,
                      ANEW_HINDI_PATH,
                      ADVERB_ENGLISH_CSV_PATH,
                      ADVERB_HINDI_PATH,
                      RAW_PATH)
from parser_csv import (fetch_english_anew_words,
                        fetch_english_adverb_words)
from time import sleep
import re
import sys


def get_hindi_url(anew_data, downloaded_path, category_name):
    """
    1. Reads the english anew words.
    2. Finds out all the words that are not downloaded
    3. Generates the list of hindi words to be downloaded, by eliminating
        all the words that are already downloaded.
    4. The url is of the form 
        http://www.shabdkosh.com/hi/translate?e=marriage&l=hi
    """    
    generate_url = list()
    for key in anew_data.keys():
        generate_url.append(key)

    downloaded_files = glob(downloaded_path + "*.txt")
    generate_files = {downloaded_path + x +"_hindi.txt": x for x in generate_url}
    to_download_set = list(set(generate_files.keys()) - set(downloaded_files))
    
    exception_url = list()
    try:
        with open(RAW_PATH + category_name + '_sorry_found.txt' , "rt") as fp:
            exception_url = re.split("\n", fp.read())
    except:
        pass

    to_download_list = list()
    for val in to_download_set:
        url = "http://www.shabdkosh.com/hi/translate?e="+ generate_files[val] +"&l=hi"
        if url in exception_url:
            continue
        to_download_list.append([url, generate_files[val]])
    return to_download_list

def download_from_shadhakosh(to_download_list, output_path, category_name):
    """
    The shadhakosh website blocks the request, if many request are made in a min.
    1. It reqires the request made as though its coming from browser
    2. Some sleep should be made for each subsequent calls.
    3. This also checks if the "Sorry no information found", so that we know when they server blocks.
    4. If we are getting more than 10 requests with "Sorry" words, then it means we are blocked.
    """
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://thewebsite.com",
        "Connection": "keep-alive" 
    }

    sorry_word = re.compile("Sorry")

    count = 0
    for url in to_download_list:
        try:
            print(url[0])
            request = urllib.request.Request(url[0], headers=request_headers)
            response = urllib.request.urlopen(request)
            contents = response.read()
            if sorry_word.search(str(contents)):            
                with open(RAW_PATH + category_name + '_sorry_found.txt','a') as f:
                    f.write('\n'+ url[0])
                sleep(30)
                count = count + 1
                if count > 100:
                    break
                continue
            count = 0
            with codecs.open(output_path + url[1]+"_hindi.txt", "wb", encoding="utf-8") as file_pointer:
                file_pointer.write(contents.decode('utf-8'))
            sleep(30)
        except urllib.error.HTTPError as e:
            print(e.code)
        except urllib.error.HTTPError as e:
            print(e.args)

def main(args):
    category = "anew_hindi"
    path = ANEW_HINDI_PATH
    for arg in args:
        if '--category' in arg:
            # Category can be "anew_hindi" or "adverb_hindi"
            category = arg.split('=')[1]
            print(category)
            if not (category == "anew_hindi" or category == "adverb_hindi"):
                raise Exception("Category can be 'anew_hindi' or 'adverb_hindi' only")
    
    if category == "anew_hindi":
        anew_data = fetch_english_anew_words()
        path = ANEW_HINDI_PATH
    elif category == "adverb_hindi":
        anew_data = fetch_english_adverb_words()
        path = ADVERB_HINDI_PATH
    url_to_download = get_hindi_url(anew_data, path, category)
    download_from_shadhakosh(url_to_download, path, category)

if __name__ == "__main__":
    main(sys.argv[1:])