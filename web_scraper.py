import requests
from bs4 import BeautifulSoup
import time
from cities import *


SELLURL = "https://www.yad2.co.il/realestate/forsale"

def check_sell():
    response = requests.get(SELLURL)
    #check to see if sell site is responding and if so continue to scrape
    if(response.status_code == 200 and response.url[8:16] != "validate"): return True
    else: return False

def scrape_city():
    cityArr = []
    for i in range(1000, 10000, 10):
        response = requests.get(SELLURL + "?city=" + str(i))
        print(response.url)
        if(response.url != SELLURL and response.url[8:16] != "validate"):
            # Parse the content with BeautifulSoup
            siteData = BeautifulSoup(response.content, 'html.parser')
            # Find the <h1> tag with the city attribute
            h1_tag = siteData.find('h1', {'data-nagish': 'page-layout-feed-title'})
            if(h1_tag):
                cityArr.append((h1_tag.text[12:],i))
        else: print(20*"-" + "city not found! continueing" + 20*"-")
        #add a 2 second time delay between each request
        time.sleep(2)
    return cityArr

def main():
        cities = loadCities()
        for city in cities:
            print(city)
        if(check_sell == True):
            cities = scrape_city()

        else: print(20*"-" + "SITE NOT REACHABLE" + 20*"-")
        
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