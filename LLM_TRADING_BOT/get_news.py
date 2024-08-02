
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from openai import OpenAI
from textblob import TextBlob
import matplotlib.pyplot as plt
import json


def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

api_keys = read_api_keys('apikeys.txt')


api_key = api_keys.get("API_KEY")
user_id = api_keys.get("USER_ID")
category = "FINANCE"
language = "en"



def get_articles(date_debut,date_fin) :
    def fetch_articles(api_key, user_id, category, language, date_debut,date_fin):
        url = "https://algogene.com/rest/v1/history_news"
        headers = {'Content-Type': 'application/json'}
        params = {
            'api_key': api_key,
            'count': 100,
            'user': user_id,
            'category': category,
            'lang': language,
            'endtime': date_fin,
            'starttime' :date_debut
        }
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['res'][0]['text']:
                article_text = data['res']
                return article_text  # Return the text of the first article
            else:
                return "No articles found"
        else:
            return response.status_code, response.text


    def get_texts(articles):
        data = []
        for i in range(0,len(articles)):
            print(articles[i])
            if type(articles[i]) != int:
                data.append(articles[i]["text"])
                
        return(data)            

    article_text = fetch_articles(api_key, user_id, category, language,date_debut,date_fin)
    if article_text :
        articles = get_texts(article_text)
        return articles
    return []


days = 350  
iterations_per_day = 1
interval = timedelta(days=1)
start_date = datetime(2023, 4, 26)
dates = []
data = {}
for i in range(days * iterations_per_day):
    current_date = start_date + i * interval
    dates.append(current_date)
    print(current_date)
    if i >=1 :
        liste_article = get_articles(str(dates[len(dates)-2]),str(current_date))
        data[str(current_date)] = liste_article

    time.sleep(6)
with open('article_data.json', 'w') as file:
    json.dump(data, file, indent=4)