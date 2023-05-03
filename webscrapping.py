import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Accept-Language': 'en-US, en;q=0.5' }

search_query = 'laptop'.replace(' ','+')
base_url = f'https://www.amazon.com/s?k={search_query}'

item = []
for i in range(1,5):
    print('Processing {0}...'.format(base_url+ '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser') #same hunxa ya sama jun ma ne

    results = soup.find_all('div', {'class' :'s-result-item', 'data-component-type':'s-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i',{'class':'a-icon'}).text
            rating_count = result.find_all('span',{'aria-label':True})[1].text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span',{'class':'a-price-fraction'}).text
            price = price1+price2
            product_url = 'https://amazon.com' + result.h2.a['href']
            # print(rating_count, product_url)
            item.append([product_name, rating, rating_count, price,product_url])
        except AttributeError:
            continue
    sleep(10)    

df = pd.DataFrame(item, columns=['product','rating','rating count', 'price','product art'])
print(df)
df.to_excel(f'{search_query}.xlsx')  