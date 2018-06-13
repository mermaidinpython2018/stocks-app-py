#File: stocks-app
#Author: mermaidinpython2018

import csv
from dotenv import load_dotenv, find_dotenv
import json
import os
import pdb
import requests
from time import time, strftime, localtime
import sys
#from IPython import embed
# For Homebrew-installed Python 3.x on Mac OS: pip3 install python-dotenv

def parse_response(response_text):

    #pdb.set_trace()

    #response_text can be either a raw JSON string or an already-converted dictionary
    if isinstance(response_text, str): # if not yet converted, then:
        response_text = json.loads(response_text) # convert string to dictionary

    results = []
    time_series_daily = response_text["Time Series (Daily)"] #> a nested dictionary
    for trading_date in time_series_daily: # FYI: can loop through a dictionary's top-level keys/attributes
        #pdb.set_trace()

        prices = time_series_daily[trading_date] #> {'1. open': '101.0924', '2. high': '101.9500', '3. low': '100.5400', '4. close': '101.6300', '5. volume': '22165128'}
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        results.append(result)
    return results

def write_prices_to_file(prices=[], filename="data/prices.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices:
            row = {
                "timestamp": d["date"], # change attribute name to match project requirements
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)

def check_symbol(symbol):

    ##see: https://www.alphavantage.co/documentation/#daily
    ## TODO: assemble the request url to get daily data for the given stock symbol
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    print("ISSUING A REQUEST")

    ##ISSUE "GET" REQUEST
    ## TODO: issue a "GET" request to the specified url, and store the response in a variable
    response = requests.get(request_url)

    ##VALIDATE RESPONSE AND HANDLE ERRORS
    if "Error Message" in response.text:
        print("REQUEST ERROR, PLEASE TRY AGAIN. CHECK YOUR STOCK SYMBOL.")
        quit("Stopping the program")


##TODO: parse the JSON response(as long as there are no errors)
    daily_prices = parse_response(response.text)

    ##write to csv
    write_prices_to_file(prices=daily_prices, filename="data/prices.csv")

    #selected stock symbol
    print(symbol)

    #date &time WHEN PROGRAM WAS EXECUTED
    print("Run at:" + strftime("%Y-%m-%d %H:%M:%S", localtime()))

    #DATE WHEN DATA WAS LAST REFRESHED
    print("Latest Data from:" + daily_prices[0]["date"])

##each symbol latest closing price, its recent average high price, and its recent average low price
##PERFORM CALCULATIONS
# TODO (HINT: use the daily_prices variable, and don't worry about the CSV file anymore :-)
    print("Recent Closing Price:" + daily_prices[0]["close"])

    high_prices = []
    for daily in daily_prices:
        high_prices.append(float(daily["high"]))
    print("Recent Average High Price:$",round(sum(high_prices)/len(high_prices), 2))

    low_prices = []
    for daily in daily_prices:
        low_prices.append(float(daily["low"]))
    avg_low_price = round(sum(low_prices)/len(low_prices), 2)
    print("Recent Average Low Price:$", avg_low_price)

    ##PRODUCE FINAL RECOMMENDATIO
    print("Recommendation: ")
    if float(daily_prices[0]["close"]) < avg_low_price * 0.2:
        print("Buy!" + " " + "Because the stock's latest closing price is less than 20% above its recent average low!")
    else:
        print("Don't Buy!" + " " + "Because the stock's latest closing price is more than 20% above its recent average low!")


if __name__ == '__main__': #only execute if file invoked from the command-line, not when imported into other files, like tests

    load_dotenv(find_dotenv()) #loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

    #see: https://www.alphavantage.co/support/#api-key
    api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
    if api_key is None:
        print("OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'.")
        sys.exit()

    ##Capture user inputs(symbol)
    symbol = input("Please input a stock symbol, (e.g. 'NFLX':)")

    #while True:
    if symbol.isnumeric() == True:
        print("Wrong message, please check your stock symbol!")
        sys.exit()
    else: #validate if the company existing
        check_symbol(symbol)
