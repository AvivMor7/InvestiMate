import requests
from bs4 import BeautifulSoup
import random
import time

SELLURL = "https://www.yad2.co.il/realestate/forsale"

def scrape_proxy_list():
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with proxy information
        proxy_table = soup.find('div', class_='table-responsive')
        
        proxies = []
        
        # Iterate through each row (tr) in the table
        for row in proxy_table.find_all('tr'):
            # Find all columns (td) in each row
            columns = row.find_all('td')
            
            # Check if columns exist (some rows might not have <td> tags)
            if columns:
                ip = columns[0].text.strip()  # First column is the IP address
                port = columns[1].text.strip()  # Second column is the port
                
                # Construct proxy in the format ip:port
                proxy = f'{ip}:{port}'
                proxies.append(proxy)
        
        return proxies
    
    except requests.exceptions.RequestException as e:
        print(f'Error fetching proxy list: {e}')
        return []

# Fetch proxy list
PROXIES = scrape_proxy_list()

# Function to get a random proxy from list
def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

# Function to check if the sell site is reachable
def check_sell(proxy):
    try:
        response = requests.get(SELLURL, proxies={"http": proxy, "https": proxy}, timeout=10)
        
        # Check if sell site is responding and if so continue to scrape
        if response.status_code == 200 and response.url[8:16] != "validate":
            return True
        else:
            return False
    
    except requests.RequestException as e:
        print(f"Error checking site reachability with proxy {proxy}: {e}")
        return False

# Function to scrape cities
def scrape_city():
    cityarr = []
    total_cities = range(1000, 10000, 10)
    num_cities = len(total_cities)
    progress_interval = num_cities // 10  # Print progress every 10%
    
    proxy = get_random_proxy()
    if not proxy:
        print("No proxies available.")
        return cityarr

    for idx, i in enumerate(total_cities):
        try:
            response = requests.get(SELLURL + "?city=" + str(i), proxies={"http": proxy, "https": proxy}, timeout=10)
            
            if response.url != SELLURL and response.url[8:16] != "validate":
                # Parse the content with BeautifulSoup
                siteData = BeautifulSoup(response.content, 'html.parser')
                # Find the <h1> tag with the city attribute
                h1_tag = siteData.find('h1', {'data-nagish': 'page-layout-feed-title'})
                if h1_tag:
                    cityarr.append((h1_tag.text[12:], i))             
            # Print progress percentage
            if idx % progress_interval == 0:
                progress = (idx + 1) / num_cities * 100
                print(f"Progress: {progress:.1f}%")
        
        except requests.RequestException as e:
            print(f"Error scraping city {i} with proxy {proxy}: {e}")
            # Switch proxy and try again
            proxy = get_random_proxy()
            if not proxy:
                print("No proxies available.")
                break
            continue
        
        time.sleep(2)
    
    return cityarr
    
# Main function to orchestrate scraping process
def main():
    proxies = scrape_proxy_list()
    if proxies:
        city_data = scrape_city()
        print("Scraped city data:", city_data)
    else:
        print("No proxies available.")

if __name__ == "__main__":
    main()
