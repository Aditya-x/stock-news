# importing important libraries
import gspread
from bs4 import BeautifulSoup
import requests
import pandas as pd

# connecting Googlesheets 
sa = gspread.service_account("creds.json")
sh = sa.open("MyfinancePro")
wks = sh.worksheet("Investment")

# Getting Company name
a = wks.acell('C6').value
b = wks.acell('C8').value

# scrapping news from Google search results
def extract(page):
    url = f'https://www.google.com/search?q={page}+news&sxsrf=AOaemvLPjuEkV2ffpO0bDdWHSAh5pC6ZBA:1642788402038&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjGvZPZt8P1AhVZ83MBHZE4A74Q_AUoAXoECAEQAw&biw=1536&bih=792&dpr=1.25'
    header = {'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'} # Temporary user agent
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup
# Cleaning and extracting meaningful information from scrapped html

def transform(soup):
    gcard = soup.find_all('g-card', class_="ftSUBd")
    for item in gcard:
        news_url = item.find("div", class_="CEMjEf NUnG9d").text  # News Site name
        #print(news_url)
        url1 = item.find('a').get('href') # news article link
        # print(url)
        title = item.find("div", class_="mCBkyc y355M JQe2Ld nDgy9d").text.strip()
        # print(title)
        news_list = {
            'Source': news_url,
            'News': title,
            'Article_url': url1
        }
        news.append(news_list)
    
# finally Printing the news inside Google sheets 
def stocknews(company, newscell, linkcell):
    c = extract(company)
    transform(c)
    df  = pd.DataFrame(news)
    newss = df.News[0]
    source = df.Source[0]
    link = df.Article_url[0]
    wks.update(newscell, f"{newss} - {source}")
    wks.update(linkcell, link)

news = []
stocknews(a,"G1", "H1")
news = []
stocknews(b, "G2", "H2")
