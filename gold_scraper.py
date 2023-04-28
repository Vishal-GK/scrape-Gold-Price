from bs4 import BeautifulSoup
import requests,math
from datetime import date
import pandas as pd

today = date.today()

def indian_gold_data():
    data = requests.get("https://www.kitco.com/gold-price-today-india/")
    soup = BeautifulSoup(data.text, 'html.parser')

    date = soup.find('div',class_='table-price--body-table').p.text.strip()
    price_table = soup.find('div',class_='table-price--body-table').find('div',class_='table-price--body-table--overview-detail').table
    # for i in price_table.find_all('td'):
        # print(i.text.strip())

    col = []
    for i in price_table.find_all('th'):
        col.append(i.text.strip())

    rows = []
    for i in price_table.find_all('tr')[1:]:
        cols = i.find_all('td')
        cols = [col.text.strip() for col in cols]
        rows.append(cols)

    df = pd.DataFrame(rows, columns=col)
    Without_gst_price = df['Gold Price Today'][1].replace(',','')
    print(f'Without gst prise: {Without_gst_price}')
    With_gst_price = math.ceil((1.18 * float(Without_gst_price))/1.03)
    print(f'With gst price: {With_gst_price}')


def tamilnadu_gold_data():
    url = "https://www.goodreturns.in/gold-rates/"

    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text,'lxml')
    gold_data_list = soup.find_all('div',class_='gold_silver_table right-align-content')[1].find_all('tr')
    rows = []
    for gold_data in gold_data_list[1:]:
        rows.append(gold_data.text.strip().replace('\n\n\n','\n').split('\n'))

    df = pd.DataFrame(rows, columns=['Gram','24K Today','24K Yesterday','Price Change'])
    Without_gst_price = float(df['24K Today'][0].lstrip('₹').replace(',','').strip())
    print(f'Without gst prise: {Without_gst_price}')
    With_gst_price = math.ceil(Without_gst_price/1.03)
    print(f'With gst price: {With_gst_price}')



get_input = input("Enter Region: ")
if get_input == 'Tamilnadu':
    tamilnadu_gold_data()
else:
    indian_gold_data()
