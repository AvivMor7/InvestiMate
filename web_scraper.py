import requests
from bs4 import BeautifulSoup
import time
from cities import *
from proxies import *
from urllib.parse import unquote
from fetch_html import *
import asyncio
from db_backup import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com'
}

DEFAULTURL = "https://www.madlan.co.il/"
SELLURL = "https://www.madlan.co.il/for-sale"
RENTURL = "https://www.madlan.co.il/for-rent"

def check_site():
    response = requests.get(DEFAULTURL, headers=HEADERS, timeout=(10))
    #check to see if sell site is responding and if so continue to scrape
    if(response.status_code == 200): return True
    else: return False

#t is type: what type to scrape, "s" for sell OR "r" for rent
def scrape_num_pages(city, t):
    if(t == "s"):
        response = requests.get(SELLURL + "/" + city.heb_name, headers=HEADERS)
    elif(t == "r"):
        response = requests.get(RENTURL + "/" + city.heb_name, headers=HEADERS)
    else: return "ERROR! UNKNOWN TYPE TO SCRAPE! USE ONLY s FOR SELL OR r FOR RENT!"
    #get html content and parse it
    html_content = asyncio.run(fetch_htmls(response.url))[0]
    soup = BeautifulSoup(html_content, "html.parser")
    #retrive the tag that specifies the number of pages for the city
    try: strCityPages = soup.find_all('div', class_='css-ixartp e3vrfmg5')[-1]
    except: return 1
    #check if sucseeded
    if(strCityPages):
        num_pages = int(strCityPages.text.strip())
        print(f"found {num_pages} pages for this city!")
        return num_pages
    else:
        print("Div tag with class 'css-ixartp e3vrfmg5' not found.") 


#t is type: what type to scrape, "s" for sell OR "r" for rent
def city_url_list(city, num_pages, t):
    arr = []
    for i in range(1, num_pages + 1):
        if(t == "s"):
            arr.append(SELLURL + "/" + city.heb_name + "?page=" + str(i))
        elif(t == "r"):
            arr.append(RENTURL + "/" + city.heb_name + "?page=" + str(i))
        else: return "ERROR! UNKNOWN TYPE TO SCRAPE! USE ONLY s FOR SELL OR r FOR RENT!"
        
    return arr

#t is type: what type to scrape, "s" for sell OR "r" for rent
def scrape_city(city, t):
    sum = 0
    count = 0
    arr = []
    #adding a 1 second delay so the site does not flag the requests
    time.sleep(1)
    numCityPages = scrape_num_pages(city, t)
    if(numCityPages):
        print(10*"-" + city.eng_name.upper() + " CITY!" + 10*"-")
        #get urls of all city pages and scrape their html
        url_arr = city_url_list(city, numCityPages, t)
        html_contents = asyncio.run(fetch_htmls(url_arr))
        #go through each page of the city and extract prices of apartments
        for i in range(1, numCityPages + 1):
            #find all prices and insert to an array of strings
            soup = BeautifulSoup(html_contents[i-1], "html.parser")
            prices_arr = soup.find_all('div', class_="css-hqth87 e13xhum61")
            #for each price string make it an int and sum it
            for j in prices_arr:
                #removing all the other elements from the price
                price_text = j.text.replace('‏', '').replace(',', '').replace('₪', '').strip()
                #this is because some people post their sell apartment for rent! UGHHHH!!!
                if(int(price_text) < 500000):
                    sum += int(price_text)
                    count += 1
            #delay so that the site does not flag us
            time.sleep(1)
            
        if (count != 0):
            return int(sum/count)
        else:
            print(20*"-" + "ERROR! NO DATA SCRAPED!" + 20*"-")   
            
    else:
        print(20*"-" + "ERROR! CANT SCRAPE NUMBER OF PAGES FOR THIS CITY!" + 20*"-")

def sell():
    if(check_site()):
        cities = load_cities_from_db()
        for city in cities:
            if(city.avg_sell == 0):
                avg_sell = scrape_city(city, "s")
                city.avg_sell = avg_sell
                save_cities_to_db(city)
                print(30*"-")
    else: print("ERROR! SITE NOT ACCESSIBLE!")
    
def rent():
    if(check_site()):
        cities = load_cities_from_db()
        for city in cities:
            if(city.avg_rent == 0):
                avg_rent = scrape_city(city, "r")
                city.avg_rent = avg_rent
                save_cities_to_db(city)
                print(30*"-")
    else: print("ERROR! SITE NOT ACCESSIBLE!")         
      
def main():
    backup_db_to_txt()
    sell()
    
if __name__ == "__main__":
    import sys
    import io

    # Redirect stdout to support UTF-8 encoding
    original_stdout = sys.stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    try:
        main()
    finally:
        # Restore original stdout
        sys.stdout = original_stdout