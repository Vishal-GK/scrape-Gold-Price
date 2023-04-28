from bs4 import BeautifulSoup
import requests
from datetime import date
import pandas as pd
from lxml import html

session = requests.Session()
today = date.today()

def indian_gold_data():
    response = session.get("https://www.kitco.com/gold-price-today-india/")
    soup = BeautifulSoup(response.text, 'lxml')

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
    With_gst_price = round((1.18 * float(Without_gst_price))/1.03)
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
    print(f'With gst prise: {Without_gst_price}')
    With_gst_price = round(Without_gst_price/1.03)
    print(f'Final gst price: {With_gst_price}')


def usa_gold_price():
    response = session.get('https://www.kitco.com/gold-price-today-usa/')
    tree = html.fromstring(response.text,'lxml')
    rows = []

    for i in tree.xpath('//div[@class="table-price--body-table--overview-detail"]/table/tr')[1:3]:
        rows.append(i.xpath('td/text()')[:2])

    print(f'24 KT gold price: {rows[1][1]}')

    kt_22 = round((float(rows[1][1])*22)/24,2)
    print(f'24 KT gold price: {kt_22}')
    rows.append(['22 KT Gold price per gram',kt_22])

    kt_18 = round((float(rows[1][1])*18)/24,2)
    print(f'18 KT gold price: {kt_18}')
    rows.append(['18 KT Gold price per gram',kt_18])

    kt_14 = round((float(rows[1][1])*14)/24,2)
    print(f'14 KT gold price: {kt_14}')
    rows.append(['14 KT Gold price per gram',kt_14])

    kt_10 = round((float(rows[1][1])*10)/24,2)
    print(f'10 KT gold price: {kt_10}')
    rows.append(['10 KT Gold price per gram',kt_10])


get_input = input("Enter Region: ")

if get_input == 'Tamilnadu':tamilnadu_gold_data()
elif get_input == 'USA':usa_gold_price()
else:indian_gold_data()
