import time
from datetime import datetime, timedelta
import json

fichier_json = 'btc_data.json'

with open(fichier_json, 'r') as file:
    btc_data = json.load(file)

interval = timedelta(days=1)
start_date = datetime(2023, 4, 26)


def next_date(date):
    date= date + interval
    return date


weight = [100,70,30,10]

def calcule_score(d,date):
    score = 0
    prix = d[str(date)]
    print("prix",prix)
    for i in range(0,4):
        date = next_date(date)
        print(date)
        try:
            score += weight[i]*((d[str(date)]/prix)-1)
            print(score)
        except:
            score = 0
    return score

days = 350
dates = []
data = {}
iterations_per_day = 1
previous_btc = 0
for i in range(days * iterations_per_day):
    current_date = start_date + i * interval
    dates.append(current_date)
    print(current_date)
    if i >=1 :
        score = calcule_score(btc_data,current_date)
        print(score)
        data[str(current_date)]=score
with open('date_score.json', 'w') as file:
    json.dump(data, file, indent=4)