import asyncio
from playwright.async_api import async_playwright
import random

PROXIES = None

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
    # Add more User-Agent strings as needed
]

async def fetch_htmls(urls):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  #change to true if you want it to run in background
                proxy={'server': random.choice(PROXIES)} if PROXIES else None,
                args=['--disable-blink-features=AutomationControlled','--window-size=800,600']
            )

            if isinstance(urls, str):
                urls = [urls]  #convert single URL to list for uniform processing

            html_contents = []
            
            if (len(urls) > 40):
                for i, url in enumerate(urls):
                    user_agent = random.choice(USER_AGENTS)
                    context = await browser.new_context(user_agent=random.choice(user_agent))
                    page = await context.new_page()
                    content = await fetch_html(page, url)
                    html_contents.append(content)
                    # Print advancement in city scraping
                    if(i>1):
                        progress = (i + 1) / len(urls) * 100
                        print(f"{progress:.2f}% DONE OF SCRAPING THIS CITY!")
                    # Optional delay between requests to avoid detection, big cities somtimes fail
                    await asyncio.sleep(random.uniform(1, 10))

            else:
                user_agent = random.choice(USER_AGENTS)
                context = await browser.new_context(user_agent=random.choice(user_agent))
                page = await context.new_page()
                for i, url in enumerate(urls):
                    content = await fetch_html(page, url)
                    html_contents.append(content)
                    # Print advancement in city scraping
                    if(i>1):
                        progress = (i + 1) / len(urls) * 100
                        print(f"{progress:.2f}% DONE OF SCRAPING THIS CITY!")
                    await asyncio.sleep(random.uniform(1, 2))

            await context.close()
            await browser.close()

            return html_contents

    except Exception as e:
        print(f"Failed to run: {e}")
        return [None] * len(urls) if isinstance(urls, list) else None

async def fetch_html(page, url):
    try:
        await page.goto(url, wait_until='networkidle')

        # Find the px-captcha element and handle it
        """ await handle_captcha(page) """

        content = await page.content()

        return content

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None
    
""" async def handle_captcha(page):
    try:
        # Wait for the CAPTCHA button containing "Press & Hold" to appear on the page
        print("Waiting for CAPTCHA button to appear...")
        element = await page.wait_for_selector('div[aria-label="Press &amp; Hold"]', timeout=20000)

        if element:
            print("CAPTCHA button found. Attempting to handle CAPTCHA...")

            # Scroll into view if necessary
            await element.scroll_into_view_if_needed()

            # Get the bounding box of the element
            box = await element.bounding_box()
            if box:
                print(f"Button bounding box: {box}")

                # Simulate mouse hover and press & hold action
                await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                await page.mouse.down()
                print("Pressing and holding the button...")

                # Hold the button for 10 seconds (adjust as necessary)
                await asyncio.sleep(10)

                # Release the button
                await page.mouse.up()
                print("Released the button after holding.")

                # Optional: Wait for the page to refresh after solving CAPTCHA
                await page.wait_for_navigation(wait_until='networkidle')
            else:
                print("Bounding box for the button not found.")
        else:
            print("CAPTCHA button element not found.")
    
    except Exception as e:
        print(f"Failed to handle CAPTCHA: {e}") """
