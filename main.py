import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "MMYTCBIFWN1UKB6K"
news_api_key = "9cf91e1e85974843acfe11ca79c03816"

twilio_api_key = "1d24658b9f114126756515c61bd6dda9"
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']

# parametres for stock page api
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

# stock api response
stock_response = requests.get(url=f"{STOCK_ENDPOINT}", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

list_of_closings = [stock_data[i]["4. close"] for i in stock_data]  # get list of daily closing prices
yest_closing = float(list_of_closings[0])  # yesterday closing price
pre_yest_closing = float(list_of_closings[1])  # day before yesterday closing price

num_diff = abs(yest_closing - pre_yest_closing)  # absolute difference between yest and pre yest prices
print(num_diff)

perc_diff = (num_diff / yest_closing) * 100  # percentage difference between yest and pre yest prices
print(perc_diff)

if perc_diff > 4:
    print("Get news")

    # news api parametres
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": news_api_key,
        "searchIn": "title"
    }

    # news api response
    news_response = requests.get(url=f"{NEWS_ENDPOINT}", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    list_of_three_art = [news_data[i] for i in range(3)]  # list of fist three articles
    # print(list_of_three_art)
    # print(len(list_of_three_art))

    # list of the articles - titla and description
    formatted_articles = [f"{STOCK_NAME}: Headline: {article['title']}. \n{article['description']}" for article in list_of_three_art]
    # print(formatted_articles)

    # send message by Twilio
    client = Client(twilio_account_sid, twilio_auth_token)

    for mess_num in range(3):
        message = client.messages \
            .create(
            body=formatted_articles[mess_num],
            from_='+17623395958',
            to='+420775653622'
        )

