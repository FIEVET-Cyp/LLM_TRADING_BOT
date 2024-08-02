
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from openai import OpenAI


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

api_open_ai = api_keys.get("API_OPEN_AI")

client = OpenAI(
  organization=api_keys.get('ORGANIZATION'),
  project=api_keys.get("PROJECT"),
  api_key = api_keys.get("API_KEY")
)





def fetch_articles(api_key, user_id, category, language):
    url = "https://algogene.com/rest/v1/realtime_news"
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'api_key': api_key,
        'user': user_id,
        'category': category,
        'lang': language
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Extraire et imprimer uniquement le texte de l'article
        article_text = data.get('res', {}).get('text', 'No text available')
        print(article_text)
        return article_text  # Retourne également l'ensemble des données au cas où vous en auriez besoin ailleurs
    else:
        print("a")
        return response.status_code, response.text

  # Utilisez le code ISO 639-1 pour la langue
def query_openai_gpt4(prompt):
    # Configuration de la requête à l'API
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response = chunk.choices[0].delta.content
    
    
    # Récupération de la réponse générée par GPT-4 Turbo
    return response
    

article_text = fetch_articles(api_key, user_id, category, language)
if article_text:
    query = "based on this article, is it a good idea to invest in cryptos? Answer with a number between -10 and 10."
    prompt = article_text + "###" + query
    # Get the response from ChatGPT
    openai_response = query_openai_gpt4(prompt)
    print("Response from OpenAI:", openai_response)

time.sleep(60)