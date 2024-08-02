import time
from datetime import datetime, timedelta
import json

date_score = 'date_score.json'
article_data = 'article_data.json'

with open(date_score, 'r') as file:
    date_score = json.load(file)
with open(article_data, 'r') as file:
    article_data = json.load(file)

interval = timedelta(days=1)
start_date = datetime(2023, 4, 26)

articles_score = [[],[]]

articles_score[0]
for key in date_score:
    if key in article_data:
        articles_score[0].append(article_data[key])
        articles_score[1].append(date_score[key])

articles_score_bis=[[],[]]
for i in range(0,len(articles_score[0])):
    for j in range(0,len(articles_score[0][i])):
        articles_score_bis[0].append(articles_score[0][i][j])
        articles_score_bis[1].append(articles_score[0][i])

