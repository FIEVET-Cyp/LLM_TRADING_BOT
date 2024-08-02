
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from openai import OpenAI
from textblob import TextBlob
import matplotlib.pyplot as plt



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


def get_score_from_date(date_debut,date_fin) :
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


    def analyser_sentiment_article(articles):
        sentiments = [0]
        for i in range(0,len(articles)):
            print(articles[i])
            if type(articles[i]) != int:
                article = articles[i]["text"]
                analysis = TextBlob(article)
                
                sentiment = analysis.sentiment.polarity 
                sentiments.append(sentiment)
        return(min(sentiments),max(sentiments))            

    article_text = fetch_articles(api_key, user_id, category, language,date_debut,date_fin)
    if article_text :
        blob = analyser_sentiment_article(article_text)
        return blob
    return (0,0)


def fetch_bitcoin_price(date,previous_btc):
    try:
        timestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        timestamp = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

    
    # Prepare the URL and parameters for the API request
    url = 'https://algogene.com/rest/v1/history_price'
    params = {
        'api_key': api_key,
        'count': 1,
        'instrument': 'BTCUSD',  # Assuming the instrument code for Bitcoin is 'BTCUSD'
        'interval': 'D',  # Daily interval
        'timestamp': timestamp,
        'user': user_id
    }
    
    # Set the appropriate headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the request to the API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        if data and 'res' in data and data['res']:
            # Assuming the response format includes a list of results under 'res'
            price_info = data['res'][0]
            return {
                'date': date,
                'open_price': price_info.get('o'),
                'close_price': price_info.get('c'),
                'high_price': price_info.get('h'),
                'low_price': price_info.get('l'),
                'volume': price_info.get('v')
            }
        else:
            print("its gonna fail")
            return "No data available for this date."
    else:
        print("gonna fail also")
        return {"close_price": previous_btc}



money = 100000
money_default = 100000
btc = 0 
btc_default = 0
days = 350  
iterations_per_day = 1
interval = timedelta(days=1)
start_date = datetime(2023, 4, 26)
dates = []
nb_buy = 0
nb_sell = 0
portfolio = [100000]
default_portfolio = [100000]
previous_btc = 0
for i in range(days * iterations_per_day):
    current_date = start_date + i * interval
    dates.append(current_date)
    print(current_date)
    if i >=1 :
        mini,maxi = get_score_from_date(str(dates[len(dates)-2]),str(current_date))
        prix_btc = fetch_bitcoin_price(str(current_date),previous_btc)["close_price"]
        previous_btc = prix_btc

        if money >1000 :
            money_default-= 1000
            btc_default+= 1000/prix_btc
        else :
            btc_default+= money/prix_btc
            money=0


        if mini<-0.2 and btc != 0:
            nb_sell+=1
            #sell
            sell = (1000/prix_btc)
            if btc <sell :
                btc=0
                money +=btc * prix_btc
            else :
                btc = btc - sell
                money += sell*prix_btc
        elif maxi > 0.2:
            nb_buy+=1
            #buy
            buy = (1000/prix_btc)
            if money<1000 :
                money = 0
                btc+=money/prix_btc
            else :
                money -= 1000
                btc +=1000/prix_btc
        print(money,btc)
        portfolio.append(money + btc*prix_btc)
        default_portfolio.append(money_default+btc_default*prix_btc)

    time.sleep(6)
plt.figure(figsize=(10, 6))
plt.plot(dates, portfolio, label='Portfolio with algo', color='blue')
plt.plot(dates, default_portfolio, label='default portfolio', color='red')
plt.title('Comparaison of the Portfolios on a year')
plt.xlabel('Date')
plt.ylabel('Value of Portfolio ($)')
plt.legend()
plt.grid(True)
plt.show()


print("strat",money + btc*prix_btc)
print('default',money_default + btc_default*prix_btc)
print("nb_buy",nb_buy)
print("nb_sell",nb_sell)