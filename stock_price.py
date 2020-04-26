from bs4 import BeautifulSoup
import requests_html
import json
import csv


# main function to fetch the ticker prices
def fetch_price_ticker(ticker_list):
    ticker_price_dictionary = {}
    for ticker in ticker_list:
        # form the URL to fetch ticker price
        url = 'https://in.finance.yahoo.com/quote/' + ticker.upper()
        session = requests_html.HTMLSession()
        response = session.get(url)
        content = BeautifulSoup(response.content, 'lxml')
        try:
            # fetching price from the page content
            price = str(content).split('data-reactid="32"')[4].split('</span>')[0].replace('>', '')
        except IndexError:
            price = 0.00
        price = price or "0"
        try:
            price = float(price.replace(',', ''))
        except ValueError:
            price = 0.00
        if price > 0:
            ticker_price_dictionary[ticker.upper()] = price

    # beautify the result
    beautify_dictionary = json.dumps(ticker_price_dictionary, indent=3)
    return beautify_dictionary


# function to fetch any ticker price user enter
def find_stock_price(c):
    ticker_list = []
    user_requested_ticker_list = []
    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_NONE,
                         skipinitialspace=True)
    with open('stocks_list.csv') as f:
        reader = csv.reader(f, dialect='myDialect')
        for row in reader:
            ticker_list.append(row)
    f.close()

    # check if the ticker is not present in list or if there is any typo (if yes then throw error)
    for i in ticker_list:
        if c.lower() in i[1] or c.lower() in i[0]:
            user_requested_ticker_list.append(i[0])
    if len(user_requested_ticker_list) == 0:
        return "Ops! Please use precise yahoo finance index for better and faster results."

    return fetch_price_ticker(user_requested_ticker_list)


# function to fetch your ticker prices
def my_ticker_price():
    ticker_list = []
    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_NONE,
                         skipinitialspace=True)
    with open('my_tickers.csv') as f:
        reader = csv.reader(f, dialect='myDialect')
        for row in reader:
            ticker_list.append(row[0])
    f.close()

    return fetch_price_ticker(ticker_list)


if __name__ == "__main__":
    print("1. Find any stock price \n2. Show my stocks prices")
    option = int(input("Select 1 or 2 : "))
    if option == 1:
        stock_name = input("Please type the name of the stock : ")
        print(find_stock_price(stock_name))
    else:
        print(my_ticker_price())
