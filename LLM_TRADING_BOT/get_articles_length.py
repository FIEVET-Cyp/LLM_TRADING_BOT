import time
from datetime import datetime, timedelta
import json

fichier_json = 'article_data.json'

with open(fichier_json, 'r') as file:
    articles = json.load(file)
total = 0
for keys in articles :
    total+=len(articles[keys])
print(total)