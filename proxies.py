import requests
import random

def scrape_proxy_list():
    url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=speed&sort_type=asc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    proxies = []

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Iterate through each proxy entry in the JSON response
        for proxy in data['data']:
            ip = proxy['ip']
            port = proxy['port']
            protocol = proxy['protocols'][0].lower()
            
            # Construct proxy in the format ip:port
            proxy_str = f'{protocol}://{ip}:{port}'
            
            # Append to the proxies list
            proxies.append(proxy_str)
        
        return proxies
    
    except requests.exceptions.RequestException as e:
        print(f'Error fetching proxy list: {e}')
        return []

# Fetch proxy list as a list
PROXIES = scrape_proxy_list()

# Function to get a random proxy from the list
def get_random_proxy():
    if PROXIES:
        return random.choice(PROXIES).strip()
    else:
        return None

# Example usage
if __name__ == "__main__":
    random_proxy = get_random_proxy()
    print(f"Random Proxy: {random_proxy}")
